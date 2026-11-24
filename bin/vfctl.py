#!/usr/bin/env python3
"""vfctl: drives the Video Factory app on this Mac (http://localhost:3030) from Claude Code.

The app does the editing (its own Claude per project, raea renders). This script only talks to its local
API: create a project, start a job, relay the chat, wait for the preview, export. Python stdlib only.

  vfctl.py status                     is Video Factory here, running and licensed? (JSON)
  vfctl.py launch                     start the app if it is installed but not running
  vfctl.py styles                     the styles this copy has (JSON)
  vfctl.py list                       the projects, newest first (JSON)
  vfctl.py new <style> [--media f…] [--script text|@file]
  vfctl.py run <id> start|continue|apply [--speed 1.1]   start the next job and wait for it
  vfctl.py say <id> "<message>"       a change request to the project's editor, then wait
  vfctl.py wait <id> [--since N]      re-attach to a job still running
  vfctl.py answer <id> <request_id> allow|deny [--answers '{"question": "answer"}']
  vfctl.py export <id> [--quality 1080|1440]
  vfctl.py open <id>                  the project in the app's window
"""
import argparse
import json
import os
import platform
import subprocess
import sys
import time
import urllib.error
import urllib.request

PORT = int(os.environ.get('VF_PORT', '3030'))
BASE = f'http://127.0.0.1:{PORT}'
HOME = os.environ.get('VF_HOME') or os.path.expanduser('~/VideoFactory')
LABEL = os.environ.get('VF_LABEL', 'com.videofactory.app')
SITE = 'https://velocitylab.whop.site/?utm_source=claude-plugin&utm_medium=plugin&utm_campaign=video-factory'
INSTALL = 'curl -fsSL https://velocitylab.whop.site/vf/install.sh | bash -s -- <YOUR LICENSE KEY>'

PITCH = {
    'not_installed': (
        'Video Factory is not installed on this Mac. It is the app that turns raw takes, a script or an idea '
        'into finished reels and carousels (rough cut, captions, b-roll, music, export), edited by Claude on '
        f'your own Mac. It comes with the Velocity Lab membership: {SITE}\n'
        f'Already a member? Install it with your license key (Whop -> your orders -> Velocity Lab -> Software):\n  {INSTALL}'),
    'unsupported': (
        'Video Factory runs on Macs with Apple Silicon (M1 or later, macOS 14+): this computer cannot run it. '
        f'What it makes: {SITE}'),
    'no_key': f'Video Factory is installed but has no license key. Add it in the app (it asks on open), or get one: {SITE}',
    'unknown_key': f'Video Factory does not recognise this license key. Check it in Whop -> your orders, or get one: {SITE}',
    'membership_inactive': f'The Velocity Lab membership behind this license is not active, so Video Factory is locked. Renew: {SITE}',
    'bound_to_another_machine': 'This license key is already used on another Mac (one key = one Mac). Contact Velocity Lab support on Whop.',
    'offline': 'Video Factory could not check its license (offline for more than 7 days). Connect to the internet and retry.',
}


def die(msg, code=1):
    print(msg, file=sys.stderr)
    sys.exit(code)


def call(path, body=None, timeout=30):
    req = urllib.request.Request(BASE + path, method='POST' if body is not None else 'GET',
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read() or b'{}')
    except urllib.error.HTTPError as e:
        try:
            msg = json.loads(e.read()).get('error') or str(e)
        except ValueError:
            msg = str(e)
        if e.code == 402:
            die('Video Factory is locked (license). Run `vfctl.py status`.')
        die(f'Video Factory said: {msg}')
    except (urllib.error.URLError, OSError):
        die('Video Factory is not answering on localhost. Run `vfctl.py status`.')


def out(obj):
    print(json.dumps(obj, indent=1, ensure_ascii=False))


# ── status ────────────────────────────────────────────────────────────────
def status():
    try:
        with urllib.request.urlopen(BASE + '/api/license', timeout=3) as r:
            lic = json.loads(r.read())
        if lic.get('ok'):
            return {'state': 'ready', 'url': f'http://localhost:{PORT}'}
        reason = lic.get('reason') or 'no_key'
        return {'state': 'locked', 'reason': reason, 'message': PITCH.get(reason, PITCH['no_key'])}
    except (urllib.error.URLError, OSError, ValueError):
        pass
    if sys.platform != 'darwin' or platform.machine() != 'arm64':
        return {'state': 'unsupported', 'message': PITCH['unsupported']}
    if os.path.isdir(os.path.join(HOME, 'app-raea')):
        return {'state': 'stopped', 'message': 'Video Factory is installed but not running: `vfctl.py launch` starts it.'}
    return {'state': 'not_installed', 'message': PITCH['not_installed']}


def launch():
    uid = os.getuid()
    r = subprocess.run(['launchctl', 'kickstart', '-k', f'gui/{uid}/{LABEL}'], capture_output=True)
    if r.returncode != 0:
        app = os.path.expanduser('~/Applications/Video Factory.app')
        if not os.path.isdir(app):
            die('Video Factory is not installed (no LaunchAgent, no ~/Applications/Video Factory.app).')
        subprocess.run(['open', app])
    for _ in range(40):
        if status()['state'] in ('ready', 'locked'):
            return status()
        time.sleep(0.5)
    die(f'The app did not start. Its log: ~/Library/Logs/VideoFactory/server.log')


# ── where the projects live (for the file paths we hand back) ─────────────
def projects_dir():
    try:
        pid = subprocess.run(['lsof', '-nP', f'-iTCP:{PORT}', '-sTCP:LISTEN', '-t'],
                             capture_output=True, text=True).stdout.split()[0]
        cmd = subprocess.run(['ps', '-o', 'command=', '-p', pid], capture_output=True, text=True).stdout
        end = cmd.find('/app-raea/server.py')       # paths may hold spaces: start at the last " /" before it
        if end > 0:
            app = cmd[cmd.rfind(' /', 0, end) + 1:end + len('/app-raea')]
            if os.path.isdir(app):
                return os.path.join(app, 'projects')
    except (IndexError, OSError):
        pass
    return os.path.join(HOME, 'app-raea', 'projects')


# ── jobs ──────────────────────────────────────────────────────────────────
def events(pid, since, timeout):
    """The project's chat events after `since`, live (the app's SSE stream)."""
    url = f'{BASE}/api/p/{pid}/chat/stream?since={since}'
    with urllib.request.urlopen(url, timeout=timeout) as r:
        for raw in r:
            line = raw.decode('utf-8', 'replace').strip()
            if line.startswith('data: '):
                yield json.loads(line[6:])
            elif line.startswith(':'):                # the app's keep-alive ping, every ~15 s
                yield {}


def last_marker(pid):
    """The seq of the latest message or job sent to the project's editor (what we wait on)."""
    marker, deadline = 0, time.time() + 3
    try:
        for ev in events(pid, 0, 3):
            if ev.get('kind') in ('user', 'job'):
                marker = ev['seq']
            if time.time() > deadline:
                break
    except (OSError, ValueError):
        pass
    return marker


def wait(pid, since=None, limit=540):
    """Print what the editor says until its turn ends, then wait for the preview render."""
    since = last_marker(pid) if since is None else since
    t0, done, seen = time.time(), False, since
    pending = {}
    try:
        for ev in events(pid, since, 30):
            kind, seen = ev.get('kind'), max(seen, ev.get('seq', 0))
            if kind == 'assistant' and ev.get('text'):
                print(f"\n[editor] {ev['text']}")
            elif kind == 'tool':
                print(f"  · {ev.get('tool')}", flush=True)
            elif kind == 'error':
                print(f"\n[error] {ev.get('text')}")
            elif kind in ('question', 'permission'):
                pending[ev['request_id']] = ev
            elif kind == 'resolved':
                pending.pop(ev.get('request_id'), None)
            elif kind == 'busy' and not ev.get('busy') and ev.get('seq', 0) > since:
                done = True
                break
            if pending and kind in ('question', 'permission'):
                break
            if time.time() - t0 > limit:
                break
    except OSError:
        pass
    if pending:
        print('\nNEEDS_ANSWER')
        out(list(pending.values()))
        print(f'(answer with `vfctl.py answer {pid} <request_id> ...`, then `vfctl.py wait {pid} --since {seen}`)')
        sys.exit(3)
    if not done:
        print(f'\nSTILL_WORKING: run `vfctl.py wait {pid} --since {seen}` to keep following it.')
        sys.exit(4)
    time.sleep(2)                                         # the app starts the preview render as the turn ends
    for _ in range(120):
        st = call(f'/api/p/{pid}/state')
        if (st.get('previewing') or {}).get('state') != 'rendering':
            break
        time.sleep(2)
    summary(pid, st)


def summary(pid, st=None):
    st = st or call(f'/api/p/{pid}/state')
    d = os.path.join(projects_dir(), pid)
    p = st.get('project') or {}
    res = {'id': pid, 'step': p.get('step'), 'label': p.get('label'),
           'open': f'http://localhost:{PORT}/#/p/{pid}'}
    for key, rel in (('roughcut', 'media/roughcut.mp4'), ('preview', 'build/preview.mp4'), ('script', 'media/script.txt')):
        f = os.path.join(d, rel)
        if os.path.isfile(f) and os.path.getsize(f):
            res[key] = f
    if st.get('storyboard'):
        res['storyboard'] = os.path.join(d, 'storyboard.json')
    if (st.get('previewing') or {}).get('state') == 'error':
        res['preview_error'] = st['previewing'].get('error')
    if st.get('export'):
        res['export'] = st['export']
    print('\nDONE')
    out(res)


def main():
    ap = argparse.ArgumentParser(description='Drive Video Factory from Claude Code.')
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('status')
    sub.add_parser('launch')
    sub.add_parser('styles')
    sub.add_parser('list')
    n = sub.add_parser('new')
    n.add_argument('style')
    n.add_argument('--media', nargs='+', default=[])
    n.add_argument('--script')
    r = sub.add_parser('run')
    r.add_argument('id')
    r.add_argument('action', choices=['start', 'continue', 'apply'])
    r.add_argument('--speed', type=float)
    s = sub.add_parser('say')
    s.add_argument('id')
    s.add_argument('text')
    w = sub.add_parser('wait')
    w.add_argument('id')
    w.add_argument('--since', type=int)
    a = sub.add_parser('answer')
    a.add_argument('id')
    a.add_argument('request_id')
    a.add_argument('choice', choices=['allow', 'deny'])
    a.add_argument('--answers')
    e = sub.add_parser('export')
    e.add_argument('id')
    e.add_argument('--quality', type=int, default=1080, choices=[1080, 1440])
    o = sub.add_parser('open')
    o.add_argument('id')
    args = ap.parse_args()

    if args.cmd == 'status':
        return out(status())
    if args.cmd == 'launch':
        return out(launch())
    if args.cmd == 'styles':
        return out([{k: s.get(k) for k in ('id', 'name', 'kind', 'input', 'blurb')}
                    for s in call('/api/styles')['styles'] if s.get('ready')])
    if args.cmd == 'list':
        return out([{k: p.get(k) for k in ('id', 'title', 'style', 'kind', 'step')}
                    for p in call('/api/projects')['projects'][:20]])
    if args.cmd == 'new':
        p = call('/api/projects', {'style': args.style})
        pid = p['id']
        media = [os.path.abspath(os.path.expanduser(m)) for m in args.media]
        missing = [m for m in media if not os.path.isfile(m)]
        if missing:
            die(f'Not found: {", ".join(missing)} (project {pid} was created without media)')
        if media:
            call(f'/api/p/{pid}/media', {'media': media})
        if args.script:
            text = args.script
            if text.startswith('@'):
                with open(os.path.expanduser(text[1:]), encoding='utf-8') as f:
                    text = f.read()
            call(f'/api/p/{pid}/script', {'text': text})
        return summary(pid)
    if args.cmd == 'run':
        if args.speed:
            call(f'/api/p/{args.id}/speed', {'speed': args.speed})
        call(f'/api/p/{args.id}/{args.action}', {})
        return wait(args.id)
    if args.cmd == 'say':
        call(f'/api/p/{args.id}/chat', {'text': args.text})
        return wait(args.id)
    if args.cmd == 'wait':
        return wait(args.id, args.since)
    if args.cmd == 'answer':
        ok = call(f'/api/p/{args.id}/chat/respond', {'request_id': args.request_id, 'allow': args.choice == 'allow',
                                                    'answers': json.loads(args.answers) if args.answers else None})
        return out(ok)
    if args.cmd == 'export':
        print('Exporting. Without an archive folder set in the app, a Finder window asks where to save: pick one.', flush=True)
        call(f'/api/p/{args.id}/export', {'quality': args.quality}, timeout=600)
        for _ in range(450):
            ex = call(f'/api/p/{args.id}/state').get('export') or {}
            if ex.get('state') in ('done', 'error', None):
                break
            time.sleep(2)
        return out(ex or {'state': 'cancelled', 'note': 'no folder picked'})
    if args.cmd == 'open':
        url = f'http://localhost:{PORT}/#/p/{args.id}'
        chrome = '/Applications/Google Chrome.app'
        subprocess.run(['open', '-na', 'Google Chrome', '--args', f'--app={url}'] if os.path.isdir(chrome) else ['open', url])
        return out({'open': url})


if __name__ == '__main__':
    main()

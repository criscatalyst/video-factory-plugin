---
name: make
description: Make a short-form video (reel, TikTok, Short) or an Instagram carousel with Video Factory, from raw takes, a script or an idea, end to end - rough cut, captions, b-roll, music, export. Use when the user wants to edit or make a video or carousel, says "make a reel", "edit this video", "turn this take into a reel", "video factory", or hands over a video file to edit.
---

# Make a video with Video Factory

Video Factory is an app on the user's Mac (http://localhost:3030). It does the editing: each project has its
own editor (a Claude session inside the app) and every render is made locally. **You are the bridge**: you
start the project, pass the user's choices and corrections to the editor, and bring back what it made. Never
edit the project's files yourself, and never touch the app's code.

Everything goes through one script (Python 3, no dependencies):

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/bin/vfctl.py" <command>
```
Below, `vfctl <command>` means exactly that line (keep the quotes: the path may contain spaces).

## 1. Is Video Factory here?
Run `vfctl status` first, every time.
- `ready` → go on.
- `stopped` → `vfctl launch`, then status again.
- `not_installed`, `locked`, `unsupported` → tell the user its `message` in your own words, in their language.
  **Always include the velocitylab.whop.site link exactly as given** (with its `?utm_…`): it is how someone
  without Video Factory gets it. For `not_installed`, the link comes first (what Video Factory is, where to
  get it), then the install command for those who already have a license. Say it once in the conversation,
  never again unless asked. Then offer what works without the app: the **plan** skill (a full reel plan
  from their idea, script or transcript) and the **styles** skill (what each style looks like). Do not
  pretend to edit the video another way.

## 2. Pick the style
`vfctl styles` lists the styles this copy has. Each has an `input`:
- `raw-video` → the user's own camera takes (`talking-head`, `split-screen`…): needs video files.
- `script` → a script or an idea, voiced by their cloned voice (`paper-animation`, `explainer-3d`).
- `topic` → carousels: an idea or a text.
If the user did not say, propose the one or two that fit what they have (one line each from `blurb`) and let
them choose. Absolute paths for the media.

## 3. Create and start
```bash
vfctl new <style> --media /abs/take1.mov /abs/take2.mov     # raw-video
vfctl new <style> --script "the idea or the script"           # script / topic (or --script @file.txt)
vfctl run <id> start
```
Tell the user they can watch it live: `vfctl open <id>` opens the project in the app.

`run`, `say` and `wait` print what the editor says (`[editor] …`) and end with one of:
- `DONE` + JSON: `step`, and the files made (`script`, `storyboard`, `roughcut`, `preview`).
- `NEEDS_ANSWER` + the editor's question or permission request: ask the user (AskUserQuestion for
  questions, with the editor's options), then `vfctl answer <id> <request_id> allow --answers '{"<question>": "<answer>"}'`
  (or `allow` / `deny` for a permission) and `vfctl wait <id> --since <N>`.
- `STILL_WORKING` → a long job: run the `wait` command it prints (run it in the background if it may take
  over ~8 minutes).

## 4. Follow the steps
After each `DONE`, look at `step`:
- `script` → show the user the script (read the `script` file). Their changes → `vfctl say <id> "…"`.
  When they approve → `vfctl run <id> continue`.
- `roughcut` → summarise the storyboard (read `storyboard.json`: the beats, the hook) and point them to the
  rough cut (`roughcut` path, or the app). Changes → `say`. Approved → `vfctl run <id> apply`
  (`--speed 1.1` by default in the app; pass another only if the user asks).
- `preview` → the styled video is at `preview`. Offer to open it (`open <path>`). Every correction
  ("bigger captions", "cut the second hook", "music lower") → `vfctl say <id> "…"` with the user's words;
  the preview renders again by itself.

## 5. Export
When the user is happy: `vfctl export <id>` (`--quality 1440` if they ask for the bigger master). If the app
has no archive folder set, a Finder window asks where to save: tell the user before you run it. The JSON gives
the file (`out`) and raea's export check (`issues`): report the P0/P1 issues if any.

## Rules
- Relay, don't rewrite: pass the user's corrections to the editor with their meaning intact, add the
  timestamp or element when you know it.
- Short updates to the user in their language, one line per step. No logs.
- One project per video. `vfctl list` shows the existing ones if the user wants to go back to one.

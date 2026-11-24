# Video Factory for Claude Code

Make reels, TikToks, Shorts and Instagram carousels by talking to Claude.
Give it your raw takes, a script or an idea: Claude runs the edit in **Video Factory** on your Mac
(rough cut, captions, b-roll, music) and hands you the finished video.

## Install

In Claude Code:

```
/plugin marketplace add criscatalyst/video-factory-plugin
/plugin install video-factory@criscatalyst
```

Then just ask: *"make a reel from ~/Desktop/take.mov"*, *"plan a reel about my new offer"*,
*"show me the video styles"*.

## What's inside

| Skill | What it does | Needs the app |
|---|---|---|
| `make` | From takes, a script or an idea to an exported reel or carousel. You approve the script and the rough cut, ask for changes in plain words, export. | Yes |
| `plan` | Three hooks, the beats (what is said, what is on screen), b-roll list, CTA and caption. | No |
| `styles` | Every style with a preview you can open. | No |

## Video Factory

The plugin drives the Video Factory app, which runs locally on your Mac (Apple Silicon, macOS 14+) and needs a
Claude Pro or Max subscription. Video Factory comes with the Velocity Lab membership:
**[velocitylab.whop.site](https://velocitylab.whop.site/?utm_source=github&utm_medium=readme&utm_campaign=video-factory)**.

Already a member? Install the app with your license key (Whop → your orders → Velocity Lab → Software):

```bash
curl -fsSL https://velocitylab.whop.site/vf/install.sh | bash -s -- <YOUR LICENSE KEY>
```

## How it works

`bin/vfctl.py` (Python 3, no dependencies) talks to the app on `localhost:3030`: it creates the project, starts
each step, relays the editor's messages and questions, waits for the preview and runs the export. Nothing leaves
your Mac except what the app itself does (license check, Claude).

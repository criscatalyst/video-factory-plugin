---
name: make
description: Make a short-form video (reel, TikTok, Short) or an Instagram carousel with Video Factory, from the user's own camera takes (reels) or an idea (carousels), end to end - rough cut, captions, b-roll, music, export. Use when the user wants to edit or make a video or carousel, says "make a reel", "edit this video", "turn this take into a reel", "video factory", or hands over a video file to edit.
---

# Make a video with Video Factory

Video Factory is an app on the user's Mac (http://localhost:3030). It does the editing: each project has its
own editor (a Claude session inside the app) and every render is made locally. **You are the bridge**: you
start the project, relay the user's choices and corrections to the editor, and bring back what it made. Never
edit the project's files yourself, and never touch the app's code.

Everything goes through `vfctl`, a script that ships with the app (Python 3, no dependencies).

## 1. Is Video Factory here?
First, every time: read `${CLAUDE_PLUGIN_ROOT}/skills/make/check.md` and follow it. It tells you whether the
app is ready, where `vfctl` is, and what to tell the user when it isn't there. Go on only when it is ready.

## 2. Pick the style
`vfctl styles` lists the styles this copy has. Each has an `input`; this plugin uses only two kinds:
- `raw-video` → reels from the user's own camera takes (`talking-head`, `split-screen`…): needs video files.
- `topic` → carousels: an idea or a text.
Leave out every other style (`input` `script`): those are made in the Video Factory app itself, not
through this plugin. If the user asks for one, say so and offer a `raw-video` style or a carousel.
If the user did not say, propose the one or two that fit what they have (one line each from `blurb`) and let
them choose. Absolute paths for the media.

## 3. Create and start
```bash
vfctl new <style> --media /abs/take1.mov /abs/take2.mov     # raw-video
vfctl new <style> --script "the idea or the text"             # topic (or --script @file.txt)
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
- `script` → (carousels) show the user the text of the slides (read the `script` file). Their changes →
  `vfctl say <id> "…"`. When they approve → `vfctl run <id> continue`.
- `roughcut` → summarise the storyboard (read `storyboard.json`: the beats, the hook) and point them to the
  rough cut (`roughcut` path, or the app). Changes → `say`. Approved → `vfctl run <id> apply`
  (`--speed 1.1` by default in the app; use another only if the user asks).
- `preview` → the styled video is at `preview`. Offer to open it (`open <path>`). Every correction
  ("bigger captions", "cut the second hook", "music lower") → `vfctl say <id> "…"` with the user's words;
  the preview renders again by itself.

## 5. Export
When the user is happy: `vfctl export <id>` (`--quality 1440` if they ask for the bigger master). If the app
has no archive folder set, a Finder window asks where to save: tell the user before you run it. The JSON gives
the file (`out`) and raea's export check (`issues`): report the P0/P1 issues if any.

## Rules
- Relay, don't rewrite: send the user's corrections to the editor with their meaning intact, add the
  timestamp or element when you know it.
- Short updates to the user in their language, one line per step. No logs.
- One project per video. `vfctl list` shows the existing ones if the user wants to go back to one.

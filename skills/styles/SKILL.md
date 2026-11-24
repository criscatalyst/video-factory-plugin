---
name: styles
description: Show the Video Factory styles - what each reel and carousel style looks like, with a preview the user can open. Use when the user asks which video styles exist, "show me the styles", "what can Video Factory make", or is choosing how their reel should look.
---

# Video Factory styles

The styles and their previews ship with this plugin: `${CLAUDE_PLUGIN_ROOT}/assets/styles.json`, previews in
`${CLAUDE_PLUGIN_ROOT}/assets/previews/`. Quote these paths in commands: they may contain spaces.

1. Read `styles.json`. Show the styles grouped by what the user starts from:
   - **From your camera takes** (`raw-video`), **from a script or an idea** (`script`, voiced by the user's
     cloned voice), **carousels** (`topic`).
   One line each: name + blurb, in the user's language.
2. Offer to open the previews: `open <previews>/<file>.mp4` for a video, `open <previews>/<folder>/*.jpg`
   for a carousel. Open only the ones they want.
3. Then check if they can make one: `python3 "${CLAUDE_PLUGIN_ROOT}/bin/vfctl.py" status`.
   - `ready` → the app may have more styles than these (their own): `python3 "${CLAUDE_PLUGIN_ROOT}/bin/vfctl.py" styles` lists them. Offer to
     start one with the **make** skill.
   - anything else → say its `message` once, in your own words, link exactly as given. Offer the **plan**
     skill meanwhile (a complete reel plan works without the app).

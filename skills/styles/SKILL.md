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
2. Offer to open the previews: `open "<previews>/<file>.gif"` for a video (it plays in Preview or the
   browser), `open "<previews>/<folder>/"*.jpg` for a carousel. Open only the ones they want.
3. Then check whether they can make one: follow `${CLAUDE_PLUGIN_ROOT}/skills/make/check.md`.
   - ready → their app may have more styles than these (their own): `vfctl styles` lists them. Offer to
     start one with the **make** skill.
   - anything else → tell them what `check.md` says, once, link exactly as written. Offer the **plan**
     skill meanwhile (a complete reel plan works without the app).

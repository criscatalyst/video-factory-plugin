# Video Factory for Claude Code

Make reels, TikToks, Shorts and Instagram carousels by talking to Claude.
Give it your raw takes: Claude runs the edit in **Video Factory** on your Mac (rough cut, captions,
b-roll, music) and hands you the finished video. Give it an idea: you get a carousel.

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
| `make` | From your takes to an exported reel, or from an idea to a carousel. You approve the rough cut (or the slides' text), ask for changes in plain words, export. | Yes |
| `plan` | Three hooks, the beats (what is said, what is on screen), b-roll list, CTA and caption. | No |
| `styles` | Every style with a preview you can open. | No |

## Video Factory

The plugin drives the Video Factory app, which runs locally on your Mac (Apple Silicon, macOS 14+) and needs a
Claude Pro or Max subscription. Video Factory comes with the Velocity Lab membership:
**[velocitylab.whop.site](https://velocitylab.whop.site/?utm_source=github&utm_medium=readme&utm_campaign=video-factory)**.

Already a member? The Setup post in the Velocity Lab area on Whop installs the app in a few minutes.

## Promotion notice

Video Factory is a paid product of this plugin's author (Cris Catalyst), sold with the Velocity Lab membership.
When the app isn't installed or its membership isn't active, the `make`, `plan` and `styles` skills say so
once per conversation and include one link to the membership
(`velocitylab.whop.site`, with `utm_source=claude-plugin` so we can count visits from the plugin). There are no
other ads or affiliate links.

## How it works

The plugin is instructions only. It talks to the app on `localhost:3030` through `vfctl`, a small script that
ships with Video Factory: it creates the project, starts each step, relays the editor's messages and questions,
waits for the preview and runs the export. Nothing leaves your Mac except what the app itself does (its
membership check, Claude).

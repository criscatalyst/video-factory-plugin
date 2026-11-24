# Privacy Policy: Video Factory plugin for Claude

Last updated: 24 November 2026

This policy covers the **Video Factory plugin** (this repository). The plugin is a set of instructions for
Claude: it contains no code that runs on its own, no tracking and no analytics.

## What the plugin handles
- **Nothing is collected by the plugin's author.** The plugin sends no data to Cris Catalyst, Velocity Lab or
  any other server of ours.
- **On your Mac only.** When you ask Claude to make a video, the plugin tells Claude to talk to the Video
  Factory app running on your own computer (`http://localhost:3030`): the paths of the files you choose, your
  script or idea, and your corrections go to that local app.
- **Previews and plans.** The style previews ship inside the plugin. Reel plans are written by Claude in your
  conversation; the plugin stores nothing.

## The Video Factory app (separate software)
The app is installed separately, with a Velocity Lab membership. On your Mac it keeps your projects and
renders locally. It contacts the internet only to check your membership (your license key and a hash of your
Mac's hardware ID; the ID itself never leaves the Mac) and to run Claude through your own Claude
Code account, under Anthropic's terms.

## Retention
The plugin retains nothing. Your projects stay on your Mac until you delete them.

## Contact
Questions: open an issue at https://github.com/criscatalyst/video-factory-plugin/issues

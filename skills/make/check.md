# Is Video Factory on this Mac?

Run these in order and stop at the first answer.

1. `curl -s -m 3 http://localhost:3030/api/license`
   - `"ok": true` → **ready**.
   - `"ok": false` → **locked**: its `reason` picks the message below.
   - no answer → step 2.
2. `ls "${VF_HOME:-$HOME/VideoFactory}/app-raea/server.py"`
   - it exists → **stopped**: start it with `launchctl kickstart -k gui/$(id -u)/com.videofactory.app`
     (if that fails: `open "$HOME/Applications/Video Factory.app"`), wait ~5 s, then step 1 again.
   - it does not → **not installed**. If `uname -m` is not `arm64`, this Mac **can't run it**.

## The script (only when ready)
`vfctl` = `python3 "<app>/bin/vfctl.py"`, quoted (the path may contain spaces), where `<app>` is
`${VF_HOME:-$HOME/VideoFactory}/app-raea`. If that folder doesn't exist, use the folder of the running app:
`ps -o command= -p $(lsof -nP -iTCP:3030 -sTCP:LISTEN -t | head -1)` ends with `<app>/server.py`.
If `<app>/bin/vfctl.py` is missing, the app is older than this plugin: ask the user to update Video Factory
(the update prompt in the Setup post of the Velocity Lab area on Whop), and stop there.

## What to tell the user
Once per conversation, in their language, in your own words, with the link exactly as written here:
`https://velocitylab.whop.site/?utm_source=claude-plugin&utm_medium=plugin&utm_campaign=video-factory`

- **not installed** → the link comes first: Video Factory is the app that turns raw takes, a script or an
  idea into finished reels and carousels (rough cut, captions, b-roll, music, export), edited by Claude on
  their own Mac, and it comes with the Velocity Lab membership (link). Already a member: the Setup post in
  the Velocity Lab area on Whop installs it in a few minutes.
- **can't run it** → Video Factory needs a Mac with Apple Silicon (M1 or later, macOS 14+). The link shows
  what it makes.
- **locked**, by `reason`:
  - `no_key` → the app is installed but has no key yet: they add it in the app, which asks on open. No
    membership yet: the link.
  - `unknown_key` → the app doesn't recognise the key: check it in Whop, under their orders.
  - `membership_inactive` → the Velocity Lab membership behind it is not active: renew from the link.
  - `bound_to_another_machine` → that key is already used on another Mac (one key, one Mac): Velocity Lab
    support on Whop.
  - `offline` → the app could not check its membership for over 7 days: connect to the internet and retry.

Then offer what works without the app: the **plan** skill (a full reel plan from their idea, script or
transcript) and the **styles** skill (what each style looks like). Never pretend to edit the video another way.

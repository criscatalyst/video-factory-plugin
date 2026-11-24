# Is Video Factory on this Mac?

Video Factory runs on the user's own Mac. If you are not running on their Mac (no shell, or a cloud
sandbox, as in the Claude web or mobile apps), don't run the checks: say that making the video needs Claude
Code (or the Claude desktop app's Code tab) on their Mac with Video Factory installed, give the link below,
and offer the **plan** skill, which works anywhere.

Otherwise run these in order and stop at the first answer.

1. Ask the app itself: a GET to http://localhost:3030/api/license, with a 3-second timeout. It answers JSON.
   - `"ok": true` → **ready**.
   - `"ok": false` → **locked**: its `reason` picks the message below.
   - no answer → step 2.
2. Look for the app's folder: `app-raea/server.py` inside `$VF_HOME`, or inside `~/VideoFactory` when
   `VF_HOME` is not set.
   - it exists → **stopped**: restart its LaunchAgent (label `com.videofactory.app`, in the user's GUI
     domain), or open `~/Applications/Video Factory.app` if that fails. Wait ~5 s, then step 1 again.
   - it does not → **not installed**. If the Mac's architecture is not arm64, this Mac **can't run it**.

## The script (only when ready)
`vfctl` is `bin/vfctl.py` inside the app's `app-raea` folder, run with python3 and its path quoted (it may
contain spaces). That folder is the one from step 2; if it doesn't exist, it is the folder of the process
listening on port 3030, whose command line ends with `app-raea/server.py`.
If `bin/vfctl.py` is missing there, the app is older than this plugin: ask the user to update Video Factory
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

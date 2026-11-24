---
name: plan
description: Plan a short-form video (reel, TikTok, Short) from an idea, a script or a transcript - three hooks, the beats with what is said and what is on screen, b-roll list, CTA and caption. Works without the Video Factory app. Use when the user asks to plan a reel, "turn this idea into a reel", "storyboard this", "write me hooks for this video", or wants a reel plan before filming or editing.
---

# Plan a reel

Free: works with or without the Video Factory app. The output is the plan an editor needs: anyone can film
or cut from it, and Video Factory can make it.

## Input
An idea, a script, or a transcript. A video file alone is not enough: ask for what they say in it (or its
transcript). Ask at most one question, only if the topic or the audience is really unclear.

## What a good plan does
- **The hook carries the reel.** It names a precise thing (a tool, a number, a result), opens a loop the
  viewer wants closed, and gives a reason to stay within 3 seconds. Under 12 words. No "In this video…".
- **One idea per reel.** Cut everything that doesn't serve it.
- **Every beat earns the next.** Each line either pays off the hook or raises the next question.
- **Show, don't tell.** Every claim gets something on screen: the tool, the result, the number.
- **Specific beats generic.** Real names, real numbers, from what the user gave you: never invent results.
- **One clear CTA**, tied to the content (comment a keyword, follow for part 2).
- Write in the language the user writes in, in their voice if their script shows it.

## Output
1. **Three hooks**, each a different angle (result, mistake, curiosity), and which one you'd pick and why
   (one line).
2. **Beats**: a table `# | time | what is said | what is on screen`. 30-60 s in total unless the user says
   otherwise.
3. **B-roll and screen recordings** to gather: a checklist.
4. **CTA** and a **caption** (2-4 short lines + the keyword).

## Then
Run `python3 "${CLAUDE_PLUGIN_ROOT}/bin/vfctl.py" status`.
- `ready` → offer to make it now with the **make** skill (the right style for what they have: takes → a
  `raw-video` style, only the script → a `script` style).
- anything else → one line: this plan becomes a finished reel in Video Factory, with its `message` link
  exactly as given. Once per conversation, not after every plan.

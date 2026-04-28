# BB Reminder

A tiny Chrome extension for bug bounty hunters (and anyone else) who want to set quick follow-up reminders on web pages — without leaving the page or filling out a calendar form.

Right-click selected text → pick a delay → a pre-filled Google Calendar event opens in a new tab. Hit **Save** and you're done. The Calendar app on your phone handles the actual notification.

No backend. No API key. No OAuth. Just the public Google Calendar URL template.

## Why

Bug bounty reports get closed, dismissed, or stall. To remember to follow up, you have to manually create a calendar event with the report URL, a note, and a date. This extension turns that into two clicks.

## Install

1. Clone or download this repo.
2. Open `chrome://extensions`.
3. Toggle **Developer mode** (top-right).
4. Click **Load unpacked** and pick the `bb-reminder` folder.

## Use

1. On any page (e.g. an H1 or Bugcrowd report), select some text — the report title, ID, or any context you want as the event title.
2. Right-click → **Remind me…** → pick a preset:
   - in 1 day
   - in 3 days
   - in 1 week
   - in 2 weeks
   - in 1 month
3. A new tab opens with Google Calendar's event template pre-filled:
   - **Title:** `Follow-up: <selected text>`
   - **Description:** `Source: <page URL>`
   - **Time:** current time + chosen delay, 5-minute event
4. Edit anything you want, then click **Save**.

The mobile Google Calendar app will notify you at the scheduled time.

## How it works

The extension registers a context-menu submenu in `background.js`. When you click a preset, it computes a start/end time and opens:

```
https://calendar.google.com/calendar/render?action=TEMPLATE
  &text=<title>
  &dates=<start>/<end>
  &details=<source URL>
```

That's the entire integration. No permissions beyond `contextMenus`.

## Roadmap

- Custom presets (configurable via options page)
- "Remind at specific date/time" option
- Auto-detect bug bounty platform from URL (H1, Bugcrowd, Intigriti, YesWeHack) and prefix the title accordingly
- Optional dashboard popup listing upcoming follow-ups (would require switching from URL template to Calendar API + OAuth)

## License

MIT

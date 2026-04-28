const PRESETS = [
  { id: "1d", label: "in 1 day", days: 1 },
  { id: "3d", label: "in 3 days", days: 3 },
  { id: "1w", label: "in 1 week", days: 7 },
  { id: "2w", label: "in 2 weeks", days: 14 },
  { id: "1m", label: "in 1 month", days: 30 },
];

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "bb-remind",
    title: "Remind me…",
    contexts: ["selection", "page", "link"],
  });
  for (const p of PRESETS) {
    chrome.contextMenus.create({
      id: p.id,
      parentId: "bb-remind",
      title: `Remind ${p.label}`,
      contexts: ["selection", "page", "link"],
    });
  }
});

function fmt(d) {
  const pad = (n) => String(n).padStart(2, "0");
  return (
    d.getUTCFullYear() +
    pad(d.getUTCMonth() + 1) +
    pad(d.getUTCDate()) +
    "T" +
    pad(d.getUTCHours()) +
    pad(d.getUTCMinutes()) +
    pad(d.getUTCSeconds()) +
    "Z"
  );
}

chrome.contextMenus.onClicked.addListener((info, tab) => {
  const preset = PRESETS.find((p) => p.id === info.menuItemId);
  if (!preset) return;

  const start = new Date(Date.now() + preset.days * 86400000);
  const end = new Date(start.getTime() + 5 * 60 * 1000);

  const title = (info.selectionText || tab?.title || "Follow-up").trim();
  const sourceUrl = info.linkUrl || tab?.url || "";
  const details = sourceUrl ? `Source: ${sourceUrl}` : "";

  const url =
    "https://calendar.google.com/calendar/render?action=TEMPLATE" +
    "&text=" + encodeURIComponent("Follow-up: " + title) +
    "&dates=" + fmt(start) + "/" + fmt(end) +
    "&details=" + encodeURIComponent(details);

  chrome.tabs.create({ url });
});

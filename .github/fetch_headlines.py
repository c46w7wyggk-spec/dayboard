import json, urllib.request, xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone
FEEDS = [("NPR","https://feeds.npr.org/1014/rss.xml"),
         ("Fox News","https://moxie.foxnews.com/google-publisher/politics.xml"),
         ("The Hill","https://thehill.com/news/feed/")]
items = []
for name, url in FEEDS:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 dayboard"})
        root = ET.fromstring(urllib.request.urlopen(req, timeout=20).read())
        for it in root.iter("item"):
            t = (it.findtext("title") or "").strip()
            d = it.findtext("pubDate")
            if not t or not d: continue
            items.append({"src": name, "title": t, "pub": parsedate_to_datetime(d).astimezone(timezone.utc).isoformat()})
    except Exception as e:
        print("failed", name, e)
json.dump({"updated": datetime.now(timezone.utc).isoformat(), "items": items}, open("headlines.json","w"))
print(len(items), "items")

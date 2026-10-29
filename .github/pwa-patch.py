# חד-פעמי: מוסיף ל-index.html את קישור ה-manifest ואת רישום ה-service worker (PWA). נמחק אחרי הריצה.
import hashlib, sys
p = "index.html"
s = open(p, encoding="utf-8", newline="").read()
HEAD_ANCHOR = "<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">"
HEAD_ADD = "<link rel=\"apple-touch-icon\" sizes=\"180x180\" href=\"apple-touch-icon.png\">\n<link rel=\"manifest\" href=\"manifest.webmanifest\">\n<meta name=\"mobile-web-app-capable\" content=\"yes\">\n<meta name=\"apple-mobile-web-app-capable\" content=\"yes\">\n<meta name=\"apple-mobile-web-app-title\" content=\"בר השגה\">\n<meta name=\"apple-mobile-web-app-status-bar-style\" content=\"default\">\n"
BODY_ANCHOR = "</body>\n</html>"
BODY_ADD = "<script>\n/* PWA: התקנה בטלפון ועבודה בלי אינטרנט (sw.js) */\nif(\"serviceWorker\" in navigator&&/^https?:$/.test(location.protocol)){window.addEventListener(\"load\",function(){navigator.serviceWorker.register(\"sw.js\").catch(function(){})})}\n</script>\n"
assert s.count(HEAD_ANCHOR) == 1 and s.count(BODY_ANCHOR) == 1
s = s.replace(HEAD_ANCHOR, HEAD_ADD + HEAD_ANCHOR).replace(BODY_ANCHOR, BODY_ADD + BODY_ANCHOR)
b = s.encode("utf-8")
h = hashlib.sha256(b).hexdigest()
print(h)
if h != "b696b1129fa1c26ea415c00d972889de4f372805c57e297429f91b4afa62aa57":
    sys.exit("unexpected result hash " + h)
open(p, "wb").write(b)

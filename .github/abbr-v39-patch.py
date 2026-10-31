# -*- coding: utf-8 -*-
# one-time patch: "ראשי תיבות" tab, version 39 (Menucha's answers + Otzar 770 database), מ״ן in the beginners' chart, sw.js cache bump
import hashlib, json
R = json.loads(open(".github/abbr-v39-repl.json", encoding="utf-8").read())
b = open("index.html", "rb").read()
assert hashlib.sha256(b).hexdigest() == "37261e9dd68d6fe5b0327175f18dd85a20ab88c87ed8e6754e27ec616eb44312", "index.html is not the expected version"
h = b.decode("utf-8")
s = h.index("const ABBR=[")
e = h.index("];", s) + 2
assert h.count("const ABBR=[") == 1
h = h[:s] + R["abbr"] + h[e:]
for a, r in R["pairs"]:
    assert h.count(a) == 1, a[:40]
    h = h.replace(a, r)
out = h.encode("utf-8")
assert hashlib.sha256(out).hexdigest() == "2b215ea1bf385c37bd4b730ea6942571a1a94a69785c5683269a99b47eb65a60", "patched index.html hash mismatch"
open("index.html", "wb").write(out)
sw = open("sw.js", encoding="utf-8").read()
old = 'const VERSION = "bar-hasaga-v38-abbr-tanya1";'
assert sw.count(old) == 1
open("sw.js", "w", encoding="utf-8").write(sw.replace(old, 'const VERSION = "bar-hasaga-v39-abbr-menucha1";'))
print("ok")

# -*- coding: utf-8 -*-
# one-time patch: "ראשי תיבות" tab, version 42 (second scan round, Otzar 770 database), sw.js cache bump
import hashlib, json
R = json.loads(open(".github/abbr-v42-repl.json", encoding="utf-8").read())
b = open("index.html", "rb").read()
assert hashlib.sha256(b).hexdigest() == "3f1191c56a205ba74b9904237604340bf24e5f630aec6b5689fb87b6a51e76ca", "index.html is not the expected version"
h = b.decode("utf-8")
s = h.index("const ABBR=[")
e = h.index("];", s) + 2
assert h.count("const ABBR=[") == 1
h = h[:s] + R["abbr"] + h[e:]
for a, r in R["pairs"]:
    assert h.count(a) == 1, a[:40]
    h = h.replace(a, r)
out = h.encode("utf-8")
assert hashlib.sha256(out).hexdigest() == "5d64b599f354c8add6769a102962c603ecfa256f64e440c34a73bd5de19877c4", "patched index.html hash mismatch"
open("index.html", "wb").write(out)
sw = open("sw.js", encoding="utf-8").read()
old = 'const VERSION = "bar-hasaga-v41-abbr-more";'
assert sw.count(old) == 1
open("sw.js", "w", encoding="utf-8").write(sw.replace(old, 'const VERSION = "bar-hasaga-v42-abbr-round2";'))
print("ok")

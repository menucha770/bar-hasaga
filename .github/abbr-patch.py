# -*- coding: utf-8 -*-
# one-time patch: adds the "ראשי תיבות" tab to index.html and bumps the sw.js cache version
import hashlib, json, sys
REPL = json.loads(open(".github/abbr-repl.json", encoding="utf-8").read())
b = open("index.html", "rb").read()
assert hashlib.sha256(b).hexdigest() == "b696b1129fa1c26ea415c00d972889de4f372805c57e297429f91b4afa62aa57", "index.html is not the expected version"
h = b.decode("utf-8")
for a, r in REPL:
    assert h.count(a) == 1, a[:40]
    h = h.replace(a, r)
out = h.encode("utf-8")
assert hashlib.sha256(out).hexdigest() == "624578dfe685aad41337ba65845200d3d629f8ed5d0805bf6272d9f06f59a463", "patched index.html hash mismatch"
open("index.html", "wb").write(out)
sw = open("sw.js", encoding="utf-8").read()
old = 'const VERSION = "bar-hasaga-v36-pwa1";'
assert sw.count(old) == 1
open("sw.js", "w", encoding="utf-8").write(sw.replace(old, 'const VERSION = "bar-hasaga-v37-abbr1";'))
print("ok")

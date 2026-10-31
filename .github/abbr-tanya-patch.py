# -*- coding: utf-8 -*-
# one-time patch: updates the "ראשי תיבות" tab according to the Tanya's abbreviation table and bumps the sw.js cache version
import hashlib, json
R = json.loads(open(".github/abbr-tanya-repl.json", encoding="utf-8").read())
b = open("index.html", "rb").read()
assert hashlib.sha256(b).hexdigest() == "624578dfe685aad41337ba65845200d3d629f8ed5d0805bf6272d9f06f59a463", "index.html is not the expected version"
h = b.decode("utf-8")
s = h.index("const ABBR=[")
e = h.index("];", s) + 2
assert h.count("const ABBR=[") == 1
assert hashlib.sha256(h[s:e].encode("utf-8")).hexdigest() == "e9a301fb803973539259cee090ad9d2b72b533517f7cb026fb4d4ea08e6bb5fd"
h = h[:s] + R["abbr"] + h[e:]
for a, r in R["pairs"]:
    assert h.count(a) == 1, a[:40]
    h = h.replace(a, r)
out = h.encode("utf-8")
assert hashlib.sha256(out).hexdigest() == "37261e9dd68d6fe5b0327175f18dd85a20ab88c87ed8e6754e27ec616eb44312", "patched index.html hash mismatch"
open("index.html", "wb").write(out)
sw = open("sw.js", encoding="utf-8").read()
old = 'const VERSION = "bar-hasaga-v37-abbr1";'
assert sw.count(old) == 1
open("sw.js", "w", encoding="utf-8").write(sw.replace(old, 'const VERSION = "bar-hasaga-v38-abbr-tanya1";'))
print("ok")

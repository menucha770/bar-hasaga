# -*- coding: utf-8 -*-
# one-time patch v40: remove the source label "פיענוח מנוחה גליס" from the abbreviations tab (entries stay), sw.js cache bump
import hashlib
b = open("index.html", "rb").read()
assert hashlib.sha256(b).hexdigest() == "2b215ea1bf385c37bd4b730ea6942571a1a94a69785c5683269a99b47eb65a60", "index.html is not the expected version"
h = b.decode("utf-8")
pairs = [
    (" 33 פוענחו בידי מנוחה גליס.", ""),
    (" מה שמנוחה גליס פיענחה כתוב לידו ״פיענוח מנוחה גליס״; מה שנלקח", " מה שנלקח"),
]
for a, r in pairs:
    assert h.count(a) == 1, a
    h = h.replace(a, r)
old = '"s":"פיענוח מנוחה גליס · '
assert h.count(old) == 33, h.count(old)
h = h.replace(old, '"s":"')
assert "מנוחה גליס" not in h
out = h.encode("utf-8")
assert hashlib.sha256(out).hexdigest() == "364e9ed7ed529ab8797073862926d4a4a5fa180969274ed3e44efc77588763a6", "patched index.html hash mismatch"
open("index.html", "wb").write(out)
sw = open("sw.js", encoding="utf-8").read()
old = 'const VERSION = "bar-hasaga-v39-abbr-menucha1";'
assert sw.count(old) == 1
open("sw.js", "w", encoding="utf-8").write(sw.replace(old, 'const VERSION = "bar-hasaga-v40-abbr-nolabel";'))
print("ok")

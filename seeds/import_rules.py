"""Usage: python import_rules.py "<campaign name>" <rules.json> [data-file]
Replaces that campaign's Rules tab with the cards in rules.json and bumps the data revision,
so any Grimoire window that is still open (and now out of date) refuses to overwrite it."""
import json, os, sys
name, rules_path = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
data = sys.argv[3] if len(sys.argv) > 3 else os.path.join(here, "..", "data", "grimoire.json")
with open(data, encoding="utf-8") as f:
    d = json.load(f)
with open(rules_path, encoding="utf-8") as f:
    rules = json.load(f)
c = next(c for c in d["campaigns"] if c["name"] == name)
c["rules"] = rules
d["rev"] = int(d.get("rev", 0)) + 1
tmp = data + ".tmp"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False)
os.replace(tmp, data)
print("imported", len(rules), "rules into", name, "-> rev", d["rev"])

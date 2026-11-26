import csv
import json
from pathlib import Path

import networkx as nx
from verify import sat, witness

rows = list(csv.DictReader(Path("gp2_palette.csv").open()))
checks = []
for row in rows:
    m = int(row["m"])
    g = nx.Graph()
    g.add_edges_from((i, (i + 1) % m) for i in range(m))
    g.add_edges_from((i, m + i) for i in range(m))
    g.add_edges_from((m + i, m + (i + 2) % m) for i in range(m))
    check = sat(g, 3)
    assert check["satisfiable"] == (row["status3"] == "1")
    if row["outer"]:
        witness(g, [int(c) for c in row["outer"] + row["inner"]], 3 if row["status3"] == "1" else 4)
    checks.append({"m": m, "three_color_sat": check["satisfiable"]})
Path("gp2_verification.json").write_text(json.dumps(checks, indent=2) + "\n")
print("Independently checked", len(checks), "three-color SAT decisions and every supplied witness.")

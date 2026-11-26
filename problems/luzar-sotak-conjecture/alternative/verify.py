"""Independent Python/NetworkX witness checks and a separate SAT encoding.

Run after ./targeted and ./structured. python-sat and networkx are required.
The SAT encoding represents each vertex color by a one-hot row and neighbor
equalities by auxiliary variables. Exactly one equal pair among three neighbors
is equivalent to exactly two distinct neighbor colors.
"""
import csv
import itertools
import json
from pathlib import Path

import networkx as nx
from pysat.solvers import Solver


def decode(s):
    return nx.from_graph6_bytes(s.encode("ascii"))


def structural(g):
    assert nx.is_connected(g)
    assert all(d == 3 for _, d in g.degree())
    assert not nx.is_bipartite(g)
    assert not list(nx.bridges(g))
    assert sum(nx.triangles(g).values()) == 0


def witness(g, colors, k):
    assert len(colors) == len(g)
    assert all(0 <= c < k for c in colors)
    assert all(colors[u] != colors[v] for u, v in g.edges())
    assert all(len({colors[u] for u in g[v]}) == 2 for v in g)


def sat(g, k):
    n = len(g)
    x = lambda v, c: 1 + v * k + c
    pairs = sorted({tuple(sorted(pair)) for v in g for pair in itertools.combinations(g[v], 2)})
    eq = {pair: n * k + i + 1 for i, pair in enumerate(pairs)}
    clauses = []
    for v in g:
        clauses.append([x(v, c) for c in range(k)])
        clauses.extend([-x(v, a), -x(v, b)] for a, b in itertools.combinations(range(k), 2))
    for u, v in g.edges():
        clauses.extend([-x(u, c), -x(v, c)] for c in range(k))
    for (u, v), e in eq.items():
        for c in range(k):
            clauses.append([-x(u, c), -x(v, c), e])
            clauses.append([-e, -x(u, c), x(v, c)])
            clauses.append([-e, -x(v, c), x(u, c)])
    for v in g:
        equalities = [eq[tuple(sorted(pair))] for pair in itertools.combinations(g[v], 2)]
        clauses.append(equalities)
        clauses.extend([-a, -b] for a, b in itertools.combinations(equalities, 2))
    clauses.append([x(0, 0)])
    clauses.append([x(next(iter(g[0])), 1)])
    with Solver(name="cadical195", bootstrap_with=clauses) as solver:
        found = solver.solve()
        if found:
            positives = {v for v in solver.get_model() if v > 0}
            colors = [next(c for c in range(k) if x(v, c) in positives) for v in g]
            witness(g, colors, k)
        return {"k": k, "satisfiable": found, "variables": n * k + len(eq), "clauses": len(clauses), "statistics": solver.accum_stats()}


def main():
    totals = {"sample_witnesses": 0, "structured_witnesses": 0, "negative_sat_checks": []}
    samples = list(csv.DictReader(Path("samples.tsv").open(), delimiter="\t"))
    assert len(samples) == 7000
    for row in samples:
        g = decode(row["graph6"])
        structural(g)
        assert row["status4"] == "1"
        witness(g, list(map(int, row["witness4"])), 4)
        totals["sample_witnesses"] += 1
    structured = list(csv.DictReader(Path("structured.tsv").open(), delimiter="\t"))
    for row in structured:
        g = decode(row["graph6"])
        structural(g)
        if row["status4"] == "1":
            witness(g, [int(x) for x in row["witness"].split(",") if x], 4)
            totals["structured_witnesses"] += 1
        else:
            assert row["status4"] == row["status5"] == row["status_unbounded"] == "0"
            checks = [sat(g, k) for k in [4, 5, len(g)]]
            assert all(not check["satisfiable"] for check in checks)
            totals["negative_sat_checks"].append({"family": row["family"], "m": int(row["m"]), "k": int(row["k"]), "checks": checks})
    Path("verification.json").write_text(json.dumps(totals, indent=2) + "\n")
    print(json.dumps(totals, indent=2))


if __name__ == "__main__":
    main()

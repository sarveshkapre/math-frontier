"""Independent finite checks for the two-port replacement argument.

Uses only Python's standard library. This validates witness tables and the
local set lemma; the accompanying review supplies the general graph argument.
"""

from itertools import product
import json


PATTERNS = ["0011", "0012", "0110", "0112", "0120", "0122", "0123"]
GAP_ORDER = "pquvabstrw"
GAP_EDGES = "pu pv qu qv ua vb ab as bt sr sw tr tw rw xp yq".split()
GAP_WITNESSES = [
    "0012210012", "0012210012", "0122012201", "0133013301",
    "0133013301", "0133013301", "0144014401",
]
UNIVERSAL_ORDER = "pqabcd"
UNIVERSAL_EDGES = "pc pd qa qb ac ad bc bd xp yq".split()
UNIVERSAL_WITNESSES = [
    "002233", "001122", "010213", "010213", "010233", "010233", "010312",
]


def verify_table(order, edges, witnesses, limits):
    neighborhoods = {v: [] for v in order + "xy"}
    for u, v in edges:
        neighborhoods[u].append(v)
        neighborhoods[v].append(u)
    assert all(len(neighborhoods[v]) == 3 for v in order)
    assert len(neighborhoods["x"]) == len(neighborhoods["y"]) == 1
    for pattern, witness, limit in zip(PATTERNS, witnesses, limits):
        coloring = dict(zip(order, map(int, witness)))
        coloring.update(x=int(pattern[2]), y=int(pattern[3]))
        assert tuple(coloring[v] for v in "pqxy") == tuple(map(int, pattern))
        assert all(coloring[u] != coloring[v] for u, v in edges)
        assert all(len({coloring[u] for u in neighborhoods[v]}) == 2 for v in order)
        assert len(set(coloring.values())) <= limit


def allowed(k, center, a, b):
    return {z for z in range(k) if z != center and len({a, b, z}) == 2}


def check_local_lemma(k):
    checked = 0
    for p, q, a, b, c, d in product(range(k), repeat=6):
        if p == q or p in (a, b) or q in (c, d):
            continue
        s = allowed(k, p, a, b)
        t = allowed(k, q, c, d)
        if not s or not t:
            continue
        checked += 1
        assert any(len({p, q, x, y}) <= 3 for x in s for y in t)
    return checked


def main():
    verify_table(GAP_ORDER, GAP_EDGES, GAP_WITNESSES, [4] * 6 + [5])
    verify_table(UNIVERSAL_ORDER, UNIVERSAL_EDGES, UNIVERSAL_WITNESSES, [4] * 7)
    local_counts = {k: check_local_lemma(k) for k in (3, 4, 5)}
    # This is a LOCAL obstruction to extending the set argument to six colors;
    # it is not a constructed global cubic gadget or a conjecture counterexample.
    s, t = allowed(6, 0, 2, 3), allowed(6, 1, 4, 5)
    assert s == {2, 3} and t == {4, 5}
    assert all(len({0, 1, x, y}) == 4 for x in s for y in t)
    result = {
        "gap_witnesses_verified": 7,
        "universal_witnesses_verified": 7,
        "local_cases_checked_by_palette": local_counts,
        "six_color_local_obstruction": {"first_allowed": sorted(s), "second_allowed": sorted(t)},
        "global_counterexample_found": False,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

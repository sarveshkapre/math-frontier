"""Check exact finite witnesses in two_pole_reduction.md (standard library only)."""
from itertools import product


def normalize(values):
    names = {}
    return tuple(names.setdefault(v, len(names)) for v in values)


PATTERNS = ("0011", "0012", "0110", "0112", "0120", "0122", "0123")
actual_patterns = {
    "".join(map(str, normalize(values)))
    for values in product(range(4), repeat=4)
    if values[0] != values[2] and values[1] != values[3]
}
assert actual_patterns == set(PATTERNS)

H_ORDER = "pquvabstrw"
H_EDGES = "pu pv qu qv ua vb ab as bt sr sw tr tw rw px qy".split()
H_COLORS = (
    "0012210012", "0012210012", "0122012201", "0133013301",
    "0133013301", "0133013301", "0144014401",
)
U_ORDER = "pqabcd"
U_EDGES = "pc pd aq ac ad bq bc bd px qy".split()
U_COLORS = (
    "002233", "001122", "010213", "010213", "010233", "010233", "010312",
)


def verify_table(order, edges, rows, limits):
    adjacency = {v: set() for v in order + "xy"}
    assert len(set(tuple(sorted(e)) for e in edges)) == len(edges)
    for a, b in edges:
        assert a != b
        adjacency[a].add(b)
        adjacency[b].add(a)
    assert all(len(adjacency[v]) == 3 for v in order)
    assert len(adjacency["x"]) == len(adjacency["y"]) == 1
    for boundary, row, limit in zip(PATTERNS, rows, limits):
        c = dict(zip(order, map(int, row)))
        fixed = dict(zip("pqxy", map(int, boundary)))
        assert all(v not in c or c[v] == color for v, color in fixed.items())
        c.update(fixed)
        assert len(set(c.values())) <= limit
        assert all(c[a] != c[b] for a, b in edges)
        assert all(len({c[u] for u in adjacency[v]}) == 2 for v in order)


verify_table(H_ORDER, H_EDGES, H_COLORS, (4,) * 6 + (5,))
verify_table(U_ORDER, U_EDGES, U_COLORS, (4,) * 7)


def allowed(palette, attachment, neighbor_a, neighbor_b):
    """Definition itself, independently of the two case formulas in the proof."""
    return {
        leaf for leaf in palette
        if leaf != attachment and len({neighbor_a, neighbor_b, leaf}) == 2
    }


cases = {}
for k in (3, 4, 5):
    palette = set(range(k))
    checked = 0
    for p, q, a, b, c, d in product(range(k), repeat=6):
        if p in (a, b) or q in (c, d):
            continue
        sx = allowed(palette, p, a, b)
        sy = allowed(palette, q, c, d)
        assert sx and sy
        assert any(len({p, q, x, y}) <= 3 for x in sx for y in sy)
        checked += 1
    cases[k] = checked

print("All seven legal boundary equality patterns accounted for.")
print("Verified 7 H extensions (6 with <=4 colors; final one with 5).")
print("Verified all 7 U extensions with <=4 colors.")
print("Verified leaf recoloring for all local cases:", cases)

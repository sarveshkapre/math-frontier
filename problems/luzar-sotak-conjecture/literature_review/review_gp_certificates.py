"""Independent set-based audit of the GP(n,2) proof certificates.

This verifier does not import either certificate generator or its verifier.
It uses literal vertex-neighborhood sets for GP(7,2), and direct five-column
windows for the three-color transfer certificate. Standard library only.
"""

from itertools import product, combinations
from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]


def check_seed(outer, inner):
    n = len(outer)
    color = list(map(int, outer + inner))
    assert len(inner) == n
    for i in range(n):
        for center, neighbors in (
            (i, {(i - 1) % n, (i + 1) % n, n + i}),
            (n + i, {i, n + (i - 2) % n, n + (i + 2) % n}),
        ):
            assert len(neighbors) == 3
            palette = {color[j] for j in neighbors}
            assert color[center] not in palette and len(palette) == 2


def check_insertion():
    seeds = [("01012", "12300"), ("01021012", "12210320"),
             ("0102302312", "1220033120")]
    for a, b in seeds:
        check_seed(a, b)
    expected = [("1", "2"), ("2", "0"), ("0", "1"), ("1", "2")]
    for a, b in seeds[1:]:
        columns = list(zip(a, b))
        assert columns[-2:] + columns[:2] == expected
        check_seed(a + "012", b + "120")
    check_seed("012012", "120120")


def check_transfer():
    cert = json.loads((ROOT / "alternative/gp2_three_color_certificate.json").read_text())
    alphabet = list(product(range(3), repeat=2))
    alphabet = [p for p in alphabet if p[0] != p[1]]
    assert alphabet == list(map(tuple, cert["alphabet"]))

    def valid4(cols):
        a, b = zip(*cols)
        return (all(a[i] != a[i+1] for i in range(3))
                and b[0] != b[2] and b[1] != b[3]
                and all(len({a[i-1], a[i+1], b[i]}) == 2 for i in (1, 2)))

    expected_states = {"".join(map(str, ix))
                       for ix in product(range(6), repeat=4)
                       if valid4([alphabet[i] for i in ix])}
    assert expected_states == set(cert["states"])
    arcs = 0
    for ix in product(range(6), repeat=5):
        cols = [alphabet[i] for i in ix]
        a, b = zip(*cols)
        if not all(a[i] != a[i+1] for i in range(4)):
            continue
        if not all(b[i] != b[i+2] for i in range(3)):
            continue
        if not all(len({a[i-1], a[i+1], b[i]}) == 2 for i in (1, 2, 3)):
            continue
        if len({b[0], b[4], a[2]}) != 2:
            continue
        source, target = "".join(map(str, ix[:4])), "".join(map(str, ix[1:]))
        r, p = cert["states"][source]
        s, q = cert["states"][target]
        assert s > r or s == r and (q-p) % 3 == 1
        arcs += 1
    assert len(expected_states) == 108 and arcs == 180
    return len(expected_states), arcs


def check_exact_cover():
    cert = json.loads((ROOT / "theory/gp7_exact_cover_certificate.json").read_text())
    neighbors = []
    for i in range(7):
        neighbors.append({(i-1) % 7, (i+1) % 7, i+7})
    for i in range(7):
        neighbors.append({i, 7+(i-2) % 7, 7+(i+2) % 7})
    rows = []
    for size in range(1, 15):
        for elements in combinations(range(14), size):
            group = frozenset(elements)
            if any(group & neighbors[v] for v in group):
                continue
            counts = [len(group & ns) for ns in neighbors]
            if 3 in counts:
                continue
            rows.append(group | {v+14 for v, count in enumerate(counts) if count == 2})
    assert len(rows) == 322
    states = {frozenset(i for i in range(28) if mask & (1 << i)): element
              for mask, element in cert["states"]}
    assert len(states) == len(cert["states"])
    assert frozenset(range(28)) in states and frozenset() not in states
    arcs = 0
    for remaining, chosen in states.items():
        assert chosen in remaining
        for row in rows:
            if chosen in row and row <= remaining:
                child = remaining - row
                assert child < remaining and child in states
                arcs += 1
    return len(rows), len(states), arcs


if __name__ == "__main__":
    check_insertion()
    states, arcs = check_transfer()
    rows, proof_states, proof_arcs = check_exact_cover()
    print(json.dumps({"upper_bound_seed_and_join_checks": "PASS",
                      "three_color_transfer_states": states,
                      "three_color_transfer_arcs": arcs,
                      "gp7_color_class_rows": rows,
                      "gp7_unsat_certificate_states": proof_states,
                      "gp7_unsat_certificate_arcs": proof_arcs}, indent=2))

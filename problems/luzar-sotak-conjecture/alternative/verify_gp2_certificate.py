"""Standard-library-only verifier for the all-n GP(n,2) lower bound.

No SAT solver, graph library, SCC algorithm, or precomputed transition list is
trusted. Every state and every possible one-column extension is reconstructed.
"""
import itertools
import json
import sys
from pathlib import Path


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("gp2_three_color_certificate.json")
    certificate = json.loads(path.read_text())
    pairs = [(a, b) for a in range(3) for b in range(3) if a != b]
    assert certificate["alphabet"] == [list(p) for p in pairs]
    states = {}
    for indices in itertools.product(range(6), repeat=4):
        outer = [pairs[i][0] for i in indices]
        inner = [pairs[i][1] for i in indices]
        if any(outer[i] == outer[i + 1] for i in range(3)):
            continue
        if inner[0] == inner[2] or inner[1] == inner[3]:
            continue
        if len({outer[0], outer[2], inner[1]}) != 2:
            continue
        if len({outer[1], outer[3], inner[2]}) != 2:
            continue
        states["".join(str(i) for i in indices)] = (indices, outer, inner)
    table = certificate["states"]
    assert set(table) == set(states)
    for rank, phase in table.values():
        assert type(rank) is int and rank >= 0
        assert type(phase) is int and 0 <= phase < 3
    transitions = 0
    for key, (indices, outer, inner) in states.items():
        for appended, (new_outer, new_inner) in enumerate(pairs):
            target_key = key[1:] + str(appended)
            if target_key not in states:
                continue
            if len({inner[0], new_inner, outer[2]}) != 2:
                continue
            # The two-state validity conditions already ensure that this
            # inner center differs from all three of its neighbors.
            assert inner[2] != inner[0]
            assert inner[2] != new_inner
            assert inner[2] != outer[2]
            transitions += 1
            rank, phase = table[key]
            next_rank, next_phase = table[target_key]
            assert next_rank > rank or (next_rank == rank and next_phase == (phase + 1) % 3), (key, target_key)
    assert len(states) == certificate["state_count"] == 108
    assert transitions == certificate["transition_count"] == 180
    print("VERIFIED: 108 states, 180 transitions; every transition raises rank or advances phase modulo 3.")
    print("Consequently every closed walk has length divisible by 3.")


if __name__ == "__main__":
    main()

"""Standalone certificate that GP(7,2) has no 2-homogeneous coloring.

A possible color class S is independent and contains no entire neighborhood.
Let M(S) be the vertices with exactly two neighbors in S. A coloring exists
iff the sets S union (14 + M(S)) exactly cover a universe of 28 elements:
the first copy partitions vertices into colors; the second assigns each
vertex its unique repeated neighbor color. This tests every palette size.

The generated UNSAT certificate is a DAG of remaining-element masks, each
with a chosen element. Every possible row covering that element leads to
another certified smaller state, or there are no such rows. Verification
uses this exhaustive branch rule and does not invoke a SAT solver.
"""
import argparse
import json
from pathlib import Path

N = 14
FULL = (1 << (2*N)) - 1


def rows():
    adj = [0] * N
    for i in range(7):
        for u, v in [(i, (i+1) % 7), (i, i+7), (i+7, (i+2) % 7+7)]:
            adj[u] |= 1 << v
            adj[v] |= 1 << u
    ans = []
    for mask in range(1, 1 << N):
        if any(mask >> v & 1 and mask & adj[v] for v in range(N)):
            continue
        counts = [(mask & a).bit_count() for a in adj]
        if 3 in counts:
            continue
        marks = sum(1 << v for v, c in enumerate(counts) if c == 2)
        ans.append(mask | (marks << N))
    return ans


def generate(path):
    options = rows()
    by_element = [[r for r in options if r >> v & 1] for v in range(2*N)]
    certificate = {}
    calls = 0

    def infeasible(rem):
        nonlocal calls
        calls += 1
        if not rem:
            return False
        if rem in certificate:
            return True
        best = None
        chosen = None
        for v in range(2*N):
            if rem >> v & 1:
                eligible = [r for r in by_element[v] if r & rem == r]
                if best is None or len(eligible) < len(best):
                    chosen, best = v, eligible
                if not best:
                    break
        for r in best:
            if not infeasible(rem ^ r):
                return False
        certificate[rem] = chosen
        return True

    assert infeasible(FULL)
    payload = {'graph': 'GP(7,2)', 'vertices': N, 'universe': 2*N,
               'color_class_rows': len(options), 'search_calls': calls,
               'states': [[mask, v] for mask, v in sorted(certificate.items())]}
    path.write_text(json.dumps(payload, indent=2)+'\n')
    return verify(path)


def verify(path):
    data = json.loads(path.read_text())
    assert data['graph'] == 'GP(7,2)' and data['vertices'] == N and data['universe'] == 2*N
    options = rows()
    assert len(options) == data['color_class_rows'] == 322
    states = dict(data['states'])
    assert len(states) == len(data['states']) and FULL in states and 0 not in states
    transitions = 0
    for rem, v in states.items():
        assert 0 < rem <= FULL and 0 <= v < 2*N and rem >> v & 1
        for row in options:
            if row >> v & 1 and row & rem == row:
                child = rem ^ row
                assert child in states
                assert child.bit_count() < rem.bit_count()
                transitions += 1
    return {'status': 'VERIFIED_UNCOLORABLE_WITH_ANY_PALETTE',
            'possible_color_classes': len(options),
            'certificate_states': len(states), 'certificate_transitions': transitions}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate', action='store_true')
    parser.add_argument('certificate', type=Path)
    args = parser.parse_args()
    result = generate(args.certificate) if args.generate else verify(args.certificate)
    print(json.dumps(result, indent=2))

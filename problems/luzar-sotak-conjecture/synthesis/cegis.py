"""Counterexample-guided synthesis of cubic 2-homogeneous coloring instances.

Master chooses graph edges with a planted, independently verified five-color
witness. An exact SAT oracle returns a four-coloring or proves none exists.
Each returned coloring becomes a constraint excluding every graph it colors.
The runs are bounded explorations, never exhaustive claims after timeout.
"""
import argparse
import itertools as it
import json
import random
import time
from pathlib import Path

import networkx as nx
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver


def check_coloring(n, edges, c):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        if c[u] == c[v]:
            return False
        adj[u].append(v)
        adj[v].append(u)
    return all(len(a) == 3 and len({c[u] for u in a}) == 2 for a in adj)


def color_oracle(n, edges, k=4, proof=False):
    pool = IDPool()
    x = [[pool.id(('color', v, a)) for a in range(k)] for v in range(n)]
    clauses = []
    adj = [[] for _ in range(n)]
    for row in x:
        clauses.append(row)
        clauses.extend([-a, -b] for a, b in it.combinations(row, 2))
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
        clauses.extend([-x[u][a], -x[v][a]] for a in range(k))
    bad = [t for t in it.product(range(k), repeat=3) if len(set(t)) != 2]
    for v in range(n):
        a, b, c = adj[v]
        clauses.extend([-x[a][p], -x[b][q], -x[c][r]] for p, q, r in bad)
    clauses += [[x[0][0]], [x[adj[0][0]][1]]]
    with Solver(name='glucose4', bootstrap_with=clauses, with_proof=proof) as sat:
        feasible = sat.solve()
        stats = sat.accum_stats()
        if not feasible:
            return None, stats, sat.get_proof() if proof else None
        pos = {a for a in sat.get_model() if a > 0}
        colors = [next(a for a in range(k) if x[v][a] in pos) for v in range(n)]
        assert check_coloring(n, edges, colors)
        return colors, stats, None


class Master:
    def __init__(self, sizes, triangle_free, seed):
        self.planted = [a for a, count in enumerate(sizes) for _ in range(count)]
        self.n = len(self.planted)
        self.pool = IDPool()
        self.sat = Solver(name='cadical195')
        self.edge = {(u, v): self.pool.id(('edge', u, v))
                     for u, v in it.combinations(range(self.n), 2)
                     if self.planted[u] != self.planted[v]}
        self.iteration = 0
        self.adj = [[] for _ in range(self.n)]
        for (u, v), e in self.edge.items():
            self.adj[u].append((v, e))
            self.adj[v].append((u, e))
        for v in range(self.n):
            self.equal([e for _, e in self.adj[v]], 3)
            ys = self.presence(v, self.planted, ('plant', v))
            self.equal(ys, 2)
        if triangle_free:
            for a, b, c in it.combinations(range(self.n), 3):
                es = [self.edge.get(e) for e in [(a, b), (a, c), (b, c)]]
                if all(es):
                    self.sat.add_clause([-e for e in es])
        # Local label symmetry: first vertex has colors 1,1,2 around it.
        # Equal class sizes make this a harmless relabeling for balanced runs;
        # unequal runs explicitly explore only this local arrangement.
        one = [v for v, c in enumerate(self.planted) if c == 1]
        two = [v for v, c in enumerate(self.planted) if c == 2]
        for v in one[:2] + two[:1]:
            self.sat.add_clause([self.edge[0, v]])
        phases = list(self.edge.values())
        rng = random.Random(seed)
        self.sat.set_phases([x if rng.randrange(2) else -x for x in phases])

    def equal(self, lits, bound):
        cnf = CardEnc.equals(lits=lits, bound=bound, vpool=self.pool,
                             encoding=EncType.seqcounter)
        self.sat.append_formula(cnf.clauses)

    def presence(self, v, coloring, tag):
        """For each color, a Boolean equivalent to having a neighbor of it."""
        ys = []
        for a in sorted(set(coloring)):
            y = self.pool.id((tag, a))
            es = [e for u, e in self.adj[v] if coloring[u] == a]
            self.sat.add_clause([-y] + es)
            self.sat.append_formula([[-e, y] for e in es])
            ys.append(y)
        return ys

    def exclude_coloring(self, coloring):
        """Exclude exactly graphs for which this fixed assignment is valid.

        A graph must contain a monochromatic edge or a vertex whose neighbor
        palette has other than two colors. For each prospective bad vertex,
        forbid each exact two-color presence pattern when that flag is true.
        """
        t = self.iteration
        self.iteration += 1
        failures = [e for (u, v), e in self.edge.items() if coloring[u] == coloring[v]]
        for v in range(self.n):
            y = self.presence(v, coloring, ('exclude', t, v))
            bad = self.pool.id(('bad', t, v))
            failures.append(bad)
            for a, b in it.combinations(range(len(y)), 2):
                self.sat.add_clause([-bad, -y[a], -y[b]] +
                                    [y[j] for j in range(len(y)) if j not in (a, b)])
        self.sat.add_clause(failures)

    def enforce_cut(self, component, minimum):
        es = [e for (u, v), e in self.edge.items()
              if (u in component) != (v in component)]
        cnf = CardEnc.atleast(lits=es, bound=minimum, vpool=self.pool,
                              encoding=EncType.seqcounter)
        self.sat.append_formula(cnf.clauses)

    def next_graph(self, conflicts=200000):
        self.sat.conf_budget(conflicts)
        status = self.sat.solve_limited()
        if status is not True:
            return status, None
        pos = {x for x in self.sat.get_model() if x > 0}
        edges = [e for e, x in self.edge.items() if x in pos]
        assert check_coloring(self.n, edges, self.planted)
        return True, edges


def run(args):
    sizes = tuple(map(int, args.sizes.split(',')))
    assert len(sizes) == 5 and min(sizes) >= 2 and sum(sizes) % 2 == 0
    start = time.monotonic()
    master = Master(sizes, args.triangle_free, args.seed)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    summary = dict(sizes=sizes, seed=args.seed, triangle_free=args.triangle_free,
                   candidates=0, cuts=0, oracle_unknown=0, status='TIME_LIMIT',
                   max_four_conflicts=0)
    recent = []
    with (out / 'trace.jsonl').open('w') as log:
        while time.monotonic() - start < args.seconds and summary['candidates'] < args.iterations:
            status, edges = master.next_graph()
            if status is None:
                summary['status'] = 'MASTER_CONFLICT_LIMIT'
                break
            if status is False:
                summary['status'] = 'RESTRICTED_FAMILY_UNSAT'
                break
            g = nx.Graph()
            g.add_nodes_from(range(master.n))
            g.add_edges_from(edges)
            if not nx.is_connected(g):
                for comp in list(nx.connected_components(g))[:-1]:
                    master.enforce_cut(comp, 2)
                    summary['cuts'] += 1
                continue
            bridges = list(nx.bridges(g))
            if bridges:
                h = g.copy()
                h.remove_edge(*bridges[0])
                master.enforce_cut(nx.node_connected_component(h, bridges[0][0]), 2)
                summary['cuts'] += 1
                continue
            colors, stats, _ = color_oracle(master.n, edges)
            summary['candidates'] += 1
            summary['max_four_conflicts'] = max(summary['max_four_conflicts'], stats['conflicts'])
            rec = dict(iteration=summary['candidates'], edges=edges, planted=master.planted,
                       coloring4=colors, oracle=stats,
                       elapsed=round(time.monotonic()-start, 3))
            log.write(json.dumps(rec) + '\n')
            log.flush()
            if colors is None:
                summary['status'] = 'CANDIDATE_COUNTEREXAMPLE'
                _, _, proof = color_oracle(master.n, edges, proof=True)
                (out/'candidate.json').write_text(json.dumps(rec, indent=2))
                (out/'unsat_proof.drat').write_text('\n'.join(proof)+'\n')
                break
            master.exclude_coloring(colors)
            # Preserve only final concrete candidates; log retains all evidence.
            recent = [rec]
            if summary['candidates'] % 100 == 0:
                print(json.dumps({**summary, 'seconds':round(time.monotonic()-start,2)}), flush=True)
        else:
            if summary['candidates'] >= args.iterations:
                summary['status'] = 'ITERATION_LIMIT'
    summary['seconds'] = round(time.monotonic()-start, 3)
    summary['master_variables'] = master.sat.nof_vars()
    summary['master_clauses'] = master.sat.nof_clauses()
    master.sat.delete()
    (out/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary), flush=True)
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sizes', default='4,4,4,4,4')
    parser.add_argument('--seed', type=int, default=20261126)
    parser.add_argument('--triangle-free', action='store_true')
    parser.add_argument('--seconds', type=float, default=120)
    parser.add_argument('--iterations', type=int, default=5000)
    parser.add_argument('--output', required=True)
    run(parser.parse_args())

"""Build a rank/phase certificate. NetworkX is used only by the builder.

The separate verifier reconstructs every transition and checks the certificate
using only the Python standard library; it does not trust this SCC calculation.
"""
import itertools
import json
from collections import deque
from pathlib import Path

import networkx as nx

PAIRS = list(itertools.permutations(range(3), 2))
states = []
for ids in itertools.product(range(6), repeat=4):
    w = [PAIRS[i] for i in ids]
    if any(w[i][0] == w[i + 1][0] for i in range(3)):
        continue
    if any(w[i][1] == w[i + 2][1] for i in range(2)):
        continue
    if any(len({w[i - 1][0], w[i + 1][0], w[i][1]}) != 2 for i in [1, 2]):
        continue
    states.append(ids)
valid = set(states)
graph = nx.DiGraph()
graph.add_nodes_from(states)
for source in states:
    for appended in range(6):
        target = source[1:] + (appended,)
        if target not in valid:
            continue
        neighbor_colors = {PAIRS[source[0]][1], PAIRS[appended][1], PAIRS[source[2]][0]}
        if len(neighbor_colors) == 2:
            graph.add_edge(source, target)

components = list(nx.strongly_connected_components(graph))
owner = {state: i for i, component in enumerate(components) for state in component}
dag = nx.DiGraph()
dag.add_nodes_from(range(len(components)))
dag.add_edges_from((owner[a], owner[b]) for a, b in graph.edges() if owner[a] != owner[b])
order = list(nx.lexicographical_topological_sort(dag, key=lambda i: min(components[i])))
rank = {component: i for i, component in enumerate(order)}
phase = {}
for component in components:
    root = min(component)
    phase[root] = 0
    queue = deque([root])
    while queue:
        source = queue.popleft()
        for target in sorted(graph[source]):
            if target not in component:
                continue
            required = (phase[source] + 1) % 3
            if target not in phase:
                phase[target] = required
                queue.append(target)
            assert phase[target] == required

certificate = {
    "description": "GP(n,2) three-color transfer graph rank/phase certificate",
    "alphabet": PAIRS,
    "state_count": len(states),
    "transition_count": len(graph.edges()),
    "states": {"".join(map(str, state)): [rank[owner[state]], phase[state]] for state in states},
}
Path("gp2_three_color_certificate.json").write_text(json.dumps(certificate, indent=2) + "\n")
print("Created certificate for", len(states), "states and", len(graph.edges()), "transitions.")

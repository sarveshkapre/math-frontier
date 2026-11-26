Counterexample-guided synthesis: completed bounded experiment
==========================================================
Run from this package root:

python3 synthesis/cegis.py --sizes 4,4,4,4,4 --triangle-free --seconds 120 \
  --output synthesis/reproduction20

Dependencies: networkx 3.7; python-sat 1.9.dev25.
Master solver: CaDiCaL 1.9.5; coloring oracle: Glucose4.

The master chooses edges for a 20-vertex graph. Vertex degrees are exactly3;
the five fixed color classes each have size4, no monochromatic edge is allowed,
and every vertex sees exactly two planted colors. This guarantees an explicit
five-color witness. Local labels fix one vertex's neighbors to colors1,1,2.
Triangles are excluded. Disconnected or bridged candidates receive cut
constraints; this experiment does not enumerate all cubic graphs.

For each candidate an independent four-color SAT encoding enforces properness
and forbids both monochromatic and all-distinct neighbor triples. If a valid
four-coloring is returned, the master receives a constraint excluding every
graph for which that particular assignment is a valid coloring. The exclusion
is a disjunction: some edge is monochromatic, or some vertex sees other than
two colors. The implementation models exact neighbor-color presence.

The recorded run produced 1,333 candidates before its time budget, all with
valid planted-five and found-four witnesses. 1,307 were nonbipartite;26 were
bipartite. None was a counterexample. The maximum oracle conflict count was18.
The elapsed time exceeded120seconds because the budget is checked between
master solver calls. A candidate's full solve is not reported incomplete.

run20/summary.json records outcome and limitations.
run20/trace.jsonl records every graph, both colorings, and SAT statistics.
run20/verification.json records independent direct checks of all witnesses and
structural conditions. The WL hash diagnostic does not deduplicate cubic
graphs; all uninitialized regular graphs have the same such hash.

This is experimental synthesis infrastructure plus a negative bounded run.
TIME_LIMIT does not imply UNSAT. The results are not evidence that the entire
20-vertex class, every five-color partition, or the conjecture was settled.

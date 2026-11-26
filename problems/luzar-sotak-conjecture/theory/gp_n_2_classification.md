# Exact 2-homogeneous color requirements for GP(n,2)

Research-session result, 2026-11-26. This result is proved here by an explicit
construction together with finite certificates. Its novelty relative to prior
literature remains unestablished.

## Theorem

For integers `n >= 5`, let `h(n)` be the least number of colors in a proper
vertex coloring of `GP(n,2)` in which every vertex has exactly two distinct
neighbor colors. Write `h(n) = infinity` if no such coloring exists.

Then

| Parameter | Exact value of h(n) |
| --- | ---: |
| `n` divisible by `3` | `3` |
| `n = 7` | `infinity` |
| Every other `n >= 5` | `4` |

The generalized Petersen graph `GP(n,2)` has vertices `u_i,v_i` indexed modulo
`n`, and edges `u_i u_(i+1)`, `u_i v_i`, and `v_i v_(i+2)`. It has `2n`
vertices. Thus the exceptional graph `GP(7,2)` has fourteen vertices.

## How the three parts fit together

**1. Three colors are sufficient when `3 | n`.** Set
`c(u_i) = i mod 3`, `c(v_i) = (i+1) mod 3`. The resulting coloring is proper
and every neighborhood has exactly two colors. Fewer than three colors are
impossible in any nonempty graph with this property: a vertex's own color must
differ from both neighbor colors.

**2. Three colors are impossible otherwise.** The finite-state proof in
`../alternative/gp2_three_color_proof.txt` encodes every possible three-coloring
using consecutive four-column windows. Its transition graph has 108 states and
180 arcs. The supplied certificate assigns each state an integer rank and a
phase modulo three. Along every allowed transition, rank either increases, or
stays constant while phase advances by one.

A cyclic coloring of `GP(n,2)` gives a closed walk of length `n`. Rank cannot
increase on a closed walk, so phase advances by one on each of its `n` steps
and must return to its start. Therefore `3 | n`. This is a proof for every
`n`, rather than a test of finitely many generalized Petersen graphs. The
verifier reconstructs all allowed states and transitions directly and checks
the certificate using only Python's standard library.

**3. Four colors suffice for every remaining `n` except `7`.** The elementary
proof in `gp_n_2_construction.md` gives explicit seed colorings at `n=5,8,10`
and a three-column insertion preserving properness and the neighborhood rule.
The two infinite formulas based on `n=8` and `n=10`, together with the
three-color periodic formula, cover every `n >= 5` other than `7`.

**4. The exception admits no coloring of any size.** The certificate
`gp7_exact_cover_certificate.json` concerns `GP(7,2)` itself. A possible color
class must be an independent set that contains no entire neighborhood. For
each possible class `S`, let `M(S)` be the set of vertices with exactly two
neighbors in `S`. A coloring with any palette is equivalent to an exact cover
by the sets `S` on one copy of the fourteen vertices and `M(S)` on a second
copy. The first copy partitions vertices into color classes; the second
assigns every vertex its unique repeated neighbor color.

There are 322 possible nonempty color-class rows. The certificate is a finite
exhaustive-branching refutation over 778 remaining-element sets, with 822
transitions. `gp7_exact_cover.py` independently regenerates every possible row
and checks every branch. A strict decrease in remaining elements justifies
induction through the certificate, proving that no exact cover exists. This
excludes every palette size, not merely four or five colors.

Combining these four assertions proves the table.

## Verification commands

From the top-level research directory:

```
python3 theory/gp_n_2_construction.py
python3 alternative/verify_gp2_certificate.py
python3 theory/gp7_exact_cover.py theory/gp7_exact_cover_certificate.json
```

The verifiers require only Python's standard library. They do not trust a SAT
solver's status or a graph library's strongly connected component routine.
These are mathematical and finite certificate proofs; they have not been
formalized in a proof assistant.

## What this establishes

The Lužar–Soták four-color assertion holds for the entire infinite family
`GP(n,2)`, because its only uncolorable member is excluded by the assertion's
admissibility hypothesis. This settles that family within this investigation.
It does not settle the conjecture for all cubic graphs. The current literature
search has not established whether this exact family classification was
previously published under homogeneous, dynamic, or another coloring
terminology; no priority claim is made.

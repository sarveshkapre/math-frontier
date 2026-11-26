# Lužar–Soták conjecture (LS-001)

**Status:** General conjecture open. No counterexample found. Partial results checked against included finite certificates and written arguments; novelty remains unestablished. Neither formal proof-assistant verification nor external peer review has been completed.

A proper 2-homogeneous coloring assigns distinct colors to adjacent vertices, and exactly two different colors appear in the neighborhood of each vertex. Lužar and Soták ask whether a cubic graph admitting such a coloring must admit one with at most four colors.

## Results (2026-11-26)

1. [Exact classification for generalized Petersen graphs GP(n,2)](theory/gp_n_2_classification.md): for n ≥ 5, three colors are necessary and sufficient if 3 divides n; GP(7,2) admits no valid coloring; four colors are necessary and sufficient otherwise. Explicit constructions and finite certificates establish the claimed classification; the theorem's originality is not confirmed.
2. [Two-port reduction](theory/two_pole_reduction.md): a conditional fifth-color obstruction in a ten-vertex fragment does not directly lead to a counterexample; the specified fragment can be replaced by a smaller fragment under the stated hypotheses.
3. [Initial exploratory census](previous/README.md): the initial work reports no counterexample through 16 vertices, and agreement with published counts. The broader bounded experiments report 8,800 graph instances, not necessarily distinct up to isomorphism; 8,798 have checked four-color witnesses and two representations of GP(7,2) are uncolorable with any palette. See [full results](RESULTS.txt) for the experimental scope and limitations.

## Reproducibility

From this directory, run `python3 verify_theorems.py`. The core certificate checks require Python 3.10+ and its standard library. Full exploratory runs may require a C++17 compiler, NetworkX and python-sat; see [experiment notes](alternative/experiment_notes.txt) and [synthesis notes](synthesis/README.txt). The original research files are preserved in their archived layout, including the checksum manifest `SHA256SUMS.txt` (which covers the pre-existing research files, not this new README).

## References and priority

- Barát et al., *Open problems of the 33rd Workshop on Cycles and Colourings*, Problem 5.1: https://arxiv.org/abs/2511.02892
- Hao, Liu and Romaniello, *On 2-Homogeneous Colourings of Cubic Bipartite Graphs*: https://arxiv.org/abs/2611.16649
- Janicová, Madaras, Soták and Lužar, *From NMNR-coloring of hypergraphs to homogenous coloring of graphs*, Ars Mathematica Contemporanea 12 (2017), 351–360.

See the [literature review](literature_review/generalized_petersen_literature.txt) and [classification review](literature_review/gp_classification_review.txt). No priority claim is made. Verify any bibliographic details against the original publications before submitting a paper.

## Next steps

Confirm the novelty of the family classification and reduction, investigate GP(n,3) for odd n, and seek more general constructive or reduction arguments. The general conjecture remains the target. New results should build on rather than overwrite this archived work.

# Lužar–Soták Problem 5.1 — exploratory research, 2026-11-26

## Status
No counterexample to the general conjecture was found. The census agrees with known connected simple cubic graph counts through order 16 (4,681 representatives). Of these, 30 admit no 2-homogeneous coloring; all the rest use at most four colors. Neither of the two papers reviewed specifies a prior exhaustive-search bound; novelty of the census or fragment has NOT been established.

## Main observation (boundary extension obstruction)
A ten-vertex two-port fragment needs five colors if its two port vertices p,q and their two external neighbors x,y have four distinct colors. See `verify_gadget.py` for its exact edge list, independent exhaustive verification of all 4^8 assignments and a five-color witness.

Proof: write the colors of p,q as A,B. The vertices u,v both touch p,q, and their remaining neighbors a,b must therefore have colors from {A,B}. The edge ab forces them to take opposite colors. The diamond with adjacent centers r,w and tips s,t forces c(s)=c(t)=T. Since s and t are adjacent to a and b respectively, T differs from A and B. At a the three neighbors are u,s,b. Since c(u) differs from A,B, c(s)=T and c(b) belongs to {A,B}, exactly two neighbor colors require c(u)=T. Similarly c(v)=T. At p and q the neighborhood condition requires T to differ from c(x) and c(y). Hence T is a fifth color. The witness in the script shows sufficiency. This is a fragment with prescribed boundary colors, NOT a cubic counterexample.

The C++ boundary census finds 27 such edge-deletion cases (not necessarily inequivalent under automorphisms) among 110,022 cases from graphs of orders 6–16. The seven possible patterns of the four boundary positions are printed in `pole_results16.txt`, with bit i representing pattern i. The gap fragment has masks (63,127): all seven patterns admit an unrestricted coloring, and the six patterns with fewer than four distinct boundary colors admit a four-color coloring.

No complementary two-port signature was found. The tested signature family is closed under the two series/parallel operations implemented in `compose.py`. Direct three-port gluing and three-port gluing with the gap fragment inserted into one joining edge found no counterexample among 8,392 vertex-deletion cases through order 14, using all port permutations and 1,472 distinct ordered signature pairs. The attempted order-16 three-port scan did not finish and is not reported. Replacing one or two edges in each of the 30 uncolorable base graphs by the gap fragment also found no counterexample (7,707 choices).

## Reproduce
Requires a C++17 compiler; Python 3 (NetworkX required only for obstructions.py).

```
g++ -O3 -std=c++17 search.cpp -o search
./search 16 > results.csv
g++ -O3 -std=c++17 poles.cpp -o poles
./poles 16 > pole_results16.txt
python compose.py
python verify_gadget.py
python obstructions.py
g++ -O3 -std=c++17 triple_gap.cpp -o triple_gap
./triple_gap 14 > triple_gap_results.txt
g++ -O3 -std=c++17 multigap.cpp -o multigap
./multigap 16 2 > multigap_results.txt
```

The census generator uses graph expansions and exact individualization/refinement canonicalization, deduplicates by graph6 codes, and matches the published known class counts. The generated representatives were independently parsed and checked for connectivity and degree 3. The palette solver exhaustively searches assignments with sound partial pruning and first-use color symmetry. The unrestricted solver branches on the three possible equal-neighbor pairs at each vertex, merges equality classes, and rejects any merged forbidden pair. All 30 unrestricted negative cases were rechecked with a separate Python implementation. This is exploratory code, not formally verified or independently peer reviewed. The 10-vertex gadget is additionally verified by a direct proof and full brute-force check.

## References
- Barát et al., *Open problems of the 33rd Workshop on Cycles and Colourings*, Problem 5.1, https://arxiv.org/abs/2511.02892
- Hao, Liu and Romaniello, *On 2-Homogeneous Colourings of Cubic Bipartite Graphs*, https://arxiv.org/abs/2611.16649
- Brinkmann, Goedgebeur and McKay, *Generation of Cubic graphs*, https://dmtcs.episciences.org/articles/551 ; graph counts https://houseofgraphs.org/Cubic

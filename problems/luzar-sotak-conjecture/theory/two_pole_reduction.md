# A two-pole recoloring lemma and a reduction for the ten-vertex fragment

Derived in this research session on 2026-11-26. These are mathematical statements
with elementary proofs and explicit finite witnesses. Their novelty relative to
the literature has not been established.

## Definitions

A *two-pole* here is a finite simple graph with two distinguished vertices of
degree one, called external leaves, and all other vertices of degree three.
Each external leaf is required to be adjacent to an internal vertex.
Each external leaf is adjacent to an internal vertex. The two leaves are
distinct; their internal neighbors may coincide. The internal
graph is allowed to be disconnected. A coloring is proper on all edges and has
exactly two distinct neighbor colors at every internal vertex. No neighborhood
condition is imposed on an external leaf.

For distinct attachment vertices, write the boundary as `(p,q,x,y)`, where
`p,q` are internal vertices, `x,y` external leaves, and `px,qy` are the two
external edges. Boundary colors must satisfy `c(p) != c(x)` and
`c(q) != c(y)`. Up to renaming colors, the seven possible equality patterns are

```
0011  0012  0110  0112  0120  0122  0123.
```

Here a pattern records colors in order `(p,q,x,y)`. Only the last has four
distinct boundary colors.

## Lemma 1: boundary repetition is unavoidable with at most four colors

**Statement.** If a two-pole admits a coloring with at most four colors, it admits
such a coloring in which the two leaves and their internal neighbors use at most
three distinct colors. All internal vertex colors can be left unchanged.

**Proof.** Enlarge the permitted palette, if necessary, to a set `C` of exactly
four colors. If the two leaves share an internal neighbor, or the two internal
neighbors have the same color, the boundary already has a repetition.

Otherwise let the attachment colors be distinct colors `P,Q`. For the leaf
attached at the vertex of color `P`, consider the colors of its attachment's
other two neighbors.

* If both have color `A`, the allowed leaf colors are exactly
  `C \ {P,A}`: properness excludes `P`, and the neighborhood condition excludes
  `A`.
* If those neighbors have distinct colors `A,B`, the allowed leaf colors are
  exactly `{A,B}`. Both differ from `P` by properness.

Thus the two leaves have allowed sets `Sx,Sy`, each of size exactly two, depending
only on the fixed internal colors. The leaf choices are independent because the
attachment vertices are distinct.

If `Q` belongs to `Sx`, choose it for `x`. If `P` belongs to `Sy`, choose it for
`y`. Either choice creates a boundary repetition. Otherwise both allowed sets
are subsets of the two-element set `C \ {P,Q}`. Since each has size two, they
are equal. Choose a common color for the two leaves. This again creates a
boundary repetition. No other internal neighborhood is changed. QED.

**Five-color version.** The same conclusion holds while preserving a bound of
five colors. Use a palette of exactly five colors. Each allowed leaf set then
has size two or three. If neither leaf can match the opposite attachment, both
sets lie in the three-element set outside `{P,Q}`. Two subsets of size at least
two must intersect. The three-color version also holds: each nonempty allowed
set avoiding `{P,Q}` is contained in the same one-element set.

**Consequence.** No independently four-colorable two-pole can have `0123` as
its only admissible four-color boundary pattern. A two-pole forcing four
distinct boundary colors in *every* valid coloring would itself admit no
coloring with at most five colors.

## The ten-vertex fragment H

Internal vertices, in table order:

```
p q u v a b s t r w
```

External leaves are `x,y`. Edges are

```
pu pv qu qv ua vb ab as bt sr sw tr tw rw px qy.
```

The following are explicit colorings. The first column fixes `(p,q,x,y)`;
the second gives all ten internal colors in the displayed order.

| Boundary | Internal colors | Palette size used |
| --- | --- | ---: |
| 0011 | 0012210012 | 3 |
| 0012 | 0012210012 | 3 |
| 0110 | 0122012201 | 3 |
| 0112 | 0133013301 | 4 |
| 0120 | 0133013301 | 4 |
| 0122 | 0133013301 | 4 |
| 0123 | 0144014401 | 5 |

Therefore H extends every legal boundary pattern with an unrestricted palette,
and every repeated boundary pattern with four colors.

For completeness, the all-distinct pattern cannot extend with four colors.
Let `c(p)=P`, `c(q)=Q`, with `P != Q`. The neighborhoods of `u,v` force
`c(a),c(b)` into `{P,Q}`. Since `ab` is an edge, they are the two different
colors. In the diamond on `s,t,r,w`, the edge `rw` and the neighborhood condition
at `r` force `c(s)=c(t)=T`. Properness at `as,bt` implies `T` differs from
`P,Q`. The neighborhoods of `a,b` then force `c(u)=c(v)=T`: each also contains
one color from `{P,Q}`, while the other two neighbors have colors outside that
set. Finally the neighborhoods at `p,q` require `T != c(x),c(y)`. Hence `T` is
different from all four boundary colors. The last table row proves that five
colors suffice.

## A universal six-vertex replacement U

Let U be `K_{3,3}` with the edge `pq` removed, and with new external leaves
`x,y` adjacent to `p,q`. Use bipartition `{p,a,b}` and `{q,c,d}`. Its edges are

```
pc pd aq ac ad bq bc bd px qy.
```

Its internal vertex order is `(p,q,a,b,c,d)`. Every boundary pattern has a
four-color extension:

| Boundary | Internal colors |
| --- | --- |
| 0011 | 002233 |
| 0012 | 001122 |
| 0110 | 010213 |
| 0112 | 010213 |
| 0120 | 010233 |
| 0122 | 010233 |
| 0123 | 010312 |

These witnesses establish universality for arbitrary actual boundary colors:
rename the displayed colors to the prescribed boundary colors and use fresh
colors only when the boundary uses fewer than four colors. If a global
four-color palette is already fixed, use its unused colors.

## Theorem 2: replacing H by U preserves the counterexample question

Let G be a connected simple cubic graph containing exactly the ten internal
vertices and internal edges of H as a fragment, joined to the rest of G by just
two edges `px,qy`. Here the outside vertices `x,y` may coincide. Let G' result
by deleting these ten internal vertices, inserting the six internal vertices
of U, and attaching its two ports to those same outside vertices.

Then:

1. G is 2-homogeneously colorable with an unrestricted palette if and only if G'
   is.
2. G has a 2-homogeneous coloring with at most four colors if and only if G' does.
3. G' is a connected simple cubic graph with exactly four fewer vertices.

**Proof.** Form the complementary two-pole R by deleting H's internal vertices
and adding two distinct new external leaves at the two vacated outside
incidences. The leaves take the place of `p,q`. R's attachment vertices can
coincide; R may be disconnected.

An unrestricted coloring of either whole graph restricts to R. Conversely, any
unrestricted coloring of R has a legal boundary pattern and can be completed
using either H's table or U's table. Thus unrestricted colorability of each
whole graph is equivalent to unrestricted colorability of R.

A four-coloring of either whole graph likewise restricts to R. Conversely, if R
has a four-coloring, U's table completes it directly to G'. To complete it with H,
first apply Lemma 1 to R so that its four boundary colors include a repetition.
The distinction between which pair are leaves and which pair are attachment
vertices does not affect the statement that a repetition occurs. H's table
then extends the boundary with the same four-color palette. Thus four-color
colorability of each whole graph is equivalent to four-color colorability of R.

Replacing a connected fragment by another connected fragment with the same two
attachment incidences preserves connectivity and cubic degrees. The replacement
has no loops or multiple edges, even if both outside incidences share a vertex,
since they meet distinct new ports. The order decreases from ten to six
internal vertices. QED.

**Minimal-counterexample consequence.** A counterexample of minimum order
cannot contain H as such a two-edge-attached fragment: its replacement G' would
be a smaller counterexample.

**Research implication.** This particular boundary obstruction cannot be
turned into a counterexample by adjoining an independently four-colorable
two-pole. If its complement already requires more than four colors, the same
counterexample property survives after replacing H by a smaller universal
fragment. H therefore adds no power to this two-piece construction strategy.
This does not prove the general Lužar–Soták conjecture and does not exclude
different fragments, more complicated interfaces, or complete counterexamples.

## Verification

`verify_two_pole_reduction.py` checks the completeness of the boundary pattern
list, all displayed colorings, and the small finite allowed-set argument for
palettes of sizes three through five. The graph and recoloring theorems above
are justified by their written proofs; the script is an additional check of
the explicit witnesses, not a proof by an incomplete graph search.

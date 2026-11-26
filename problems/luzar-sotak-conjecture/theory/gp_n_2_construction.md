# An explicit four-color construction for GP(n,2)

Derived and checked in this session on 2026-11-26. Novelty has not been
established. This proves a bound for an infinite graph family, not the general
Lužar–Soták conjecture.

## Statement

For every integer `n >= 5` with `n != 7`, the generalized Petersen graph
`GP(n,2)` has a proper vertex coloring with at most four colors such that every
vertex sees exactly two colors among its neighbors.

Use vertices `u_i,v_i`, indexed modulo `n`, and edges

```
u_i u_(i+1),  u_i v_i,  v_i v_(i+2).
```

The graph has `2n` vertices. A pair of words `A,B`, each of length `n`, specifies
the colors of `u_0,...,u_(n-1)` and `v_0,...,v_(n-1)`, respectively.

## Explicit formulas

In the table, juxtaposition means concatenation and `W^t` means repeat the word
`W` exactly `t` times.

| Parameter | Outer word A | Inner word B |
| --- | --- | --- |
| `n = 5` | `01012` | `12300` |
| `n = 3t`, `t >= 2` | `(012)^t` | `(120)^t` |
| `n = 8 + 3t`, `t >= 0` | `01021012 (012)^t` | `12210320 (120)^t` |
| `n = 10 + 3t`, `t >= 0` | `0102302312 (012)^t` | `1220033120 (120)^t` |

These cases cover exactly all `n >= 5` other than `n = 7`.

## Proof

At outer vertex `u_i`, the three neighbor colors are
`A_(i-1), A_(i+1), B_i`. At inner vertex `v_i`, they are
`B_(i-2), B_(i+2), A_i`. These formulas make the local checks explicit.

For `3 | n`, assign `A_i = i mod 3`, `B_i = (i+1) mod 3`. Every edge joins
different colors. The outer neighborhood has colors
`{i-1,i+1}` modulo three, with one repeated. The inner neighborhood has colors
`{i-1,i}` modulo three, again with one repeated. Both sets have size two.

The three nonperiodic seed rows, for `n=5,8,10`, satisfy all edge and neighborhood
conditions directly. They can be checked from the two displayed neighborhood
formulas, or by the accompanying standard-library verifier.

It remains to justify the arbitrarily many appended blocks in the rows for
`n=8+3t` and `n=10+3t`.

Regard a column as the pair `(A_i,B_i)`. Write the periodic sequence of columns
as

```
(0,1), (1,2), (2,0), (0,1), (1,2), (2,0), ...
```

Both the eight-column seed and the ten-column seed have the same four columns
at the cyclic join:

| Position relative to the join | Column |
| --- | --- |
| `-2` (penultimate seed column) | `(1,2)` |
| `-1` (last seed column) | `(2,0)` |
| `0` (first seed column) | `(0,1)` |
| `1` (second seed column) | `(1,2)` |

Insert the three columns `(0,1),(1,2),(2,0)` between the last and first seed
columns. This inserts one full period of the valid periodic sequence.

An old vertex whose neighbors cross the join receives replacement neighbors of
the same colors: outer edges cross by one column, and inner edges cross by two
columns. Only the four displayed old columns can participate in these changes.
Thus every old vertex preserves both properness and the set of neighbor colors.
Every new vertex sees exactly the colors it would see in the periodic sequence,
since the two old columns on each side agree with that sequence. It is therefore
proper and has exactly two neighbor colors.

After this insertion the last two columns and first two columns still have the
same displayed values. The insertion can consequently be repeated any number
of times. This proves both infinite rows and hence the theorem. QED.

## Scope

The construction gives an upper bound only. It does not by itself prove that
four colors are necessary when `3` does not divide `n`, nor that `GP(7,2)` admits
no coloring with a larger palette. Those separate assertions are proved by the
companion certificates described in `gp_n_2_classification.md`: a three-color
transfer certificate and an unrestricted exact-cover certificate at `n=7`.

The source `gp_n_2_construction.py` implements the exact formulas and checks the
three seed colorings, the periodic local rule, and the boundary invariant used
in the proof. It also prints optional example colorings without running any
search.

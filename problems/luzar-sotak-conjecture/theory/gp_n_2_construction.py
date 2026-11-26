"""Explicit 2-homogeneous colorings of GP(n,2), n>=5, n!=7.

This is a formula and verifier, not a coloring search. Standard library only.
Run without arguments for finite checks supporting the written induction.
Run with an allowed n to print its two coloring words.
"""
import sys


SEEDS = {
    5: ("01012", "12300"),
    8: ("01021012", "12210320"),
    10: ("0102302312", "1220033120"),
}
BLOCK = ("012", "120")


def coloring(n):
    if n < 5 or n == 7:
        raise ValueError("Formula requires n >= 5 and n != 7.")
    if n == 5:
        return SEEDS[5]
    if n % 3 == 0:
        return tuple(word * (n // 3) for word in BLOCK)
    seed_n = 8 if n % 3 == 2 else 10
    t = (n - seed_n) // 3
    assert t >= 0 and n == seed_n + 3 * t
    return tuple(seed + word * t for seed, word in zip(SEEDS[seed_n], BLOCK))


def valid(words):
    a, b = words
    if len(a) != len(b):
        return False
    n = len(a)
    if len(set(a + b)) > 4:
        return False
    for i in range(n):
        outer_neighbors = {a[(i - 1) % n], a[(i + 1) % n], b[i]}
        inner_neighbors = {b[(i - 2) % n], b[(i + 2) % n], a[i]}
        if a[i] in outer_neighbors or b[i] in inner_neighbors:
            return False
        if len(outer_neighbors) != 2 or len(inner_neighbors) != 2:
            return False
    return True


def columns(words):
    return list(zip(*words))


def verify():
    for n, words in SEEDS.items():
        assert len(words[0]) == len(words[1]) == n
        assert valid(words), (n, words)
    periodic = columns(BLOCK)
    for i in range(3):
        a, b = periodic[i]
        outer_neighbors = {periodic[(i-1) % 3][0], periodic[(i+1) % 3][0], b}
        inner_neighbors = {periodic[(i-2) % 3][1], periodic[(i+2) % 3][1], a}
        assert a not in outer_neighbors and len(outer_neighbors) == 2
        assert b not in inner_neighbors and len(inner_neighbors) == 2

    expected = [("1", "2"), ("2", "0"), ("0", "1"), ("1", "2")]
    for n in (8, 10):
        seed = SEEDS[n]
        cols = columns(seed)
        assert cols[-2:] + cols[:2] == expected
        inserted = tuple(seed_word + block_word for seed_word, block_word in zip(seed, BLOCK))
        assert valid(inserted)
        new_cols = columns(inserted)
        assert new_cols[-2:] + new_cols[:2] == expected

    print("Verified seeds n=5,8,10, the 3-column periodic rule,")
    print("and the preserved four-column boundary for indefinite insertion.")
    print("The written induction proves the formula for every n>=5 other than7.")


if __name__ == "__main__":
    verify()
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
        words = coloring(n)
        assert valid(words)
        print("n =", n)
        print("outer:", words[0])
        print("inner:", words[1])

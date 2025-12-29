import random
import math
from typing import List, Tuple


Fraction = Tuple[int, int]


def extend_fractions(fractions: List[Fraction], k: int) -> List[Fraction]:
    """
    Forlænger alle brøker med faktoren k.
    (n/d -> (k·n)/(k·d))
    """
    if k < 1:
        raise ValueError("Forlængelsesfaktor k skal være >= 1")

    return [(n * k, d * k) for n, d in fractions]


def _all_fractions_up_to(max_denominator: int) -> List[Fraction]:
    """
    Genererer ALLE brøker 0 < n/d < 1 med d <= max_denominator
    (inkl. ækvivalente)
    """
    if max_denominator < 2:
        raise ValueError("max_denominator skal være >= 2")

    fracs = []
    for d in range(2, max_denominator + 1):
        for n in range(1, d):
            fracs.append((n, d))
    return fracs


def _reduce_fraction(frac: Fraction) -> Fraction:
    n, d = frac
    g = math.gcd(n, d)
    return (n // g, d // g)


def generate_random_fractions(
    count: int,
    max_denominator: int,
    allow_equivalent: bool
) -> List[Fraction]:
    """
    Genererer tilfældige brøker mellem 0 og 1.

    Parameters
    ----------
    count : antal brøker
    max_denominator : maksimal nævner
    allow_equivalent : hvis False fjernes ækvivalente brøker

    Returns
    -------
    List[(n, d)]
    """

    if count < 1:
        raise ValueError("count skal være >= 1")

    all_fracs = _all_fractions_up_to(max_denominator)

    if allow_equivalent:
        if count > len(all_fracs):
            raise ValueError("For mange brøker i forhold til max nævner")
        return random.sample(all_fracs, count)

    # Fjern ækvivalente brøker
    reduced_map = {}
    for frac in all_fracs:
        reduced = _reduce_fraction(frac)
        # behold én repræsentant pr. værdi
        if reduced not in reduced_map:
            reduced_map[reduced] = frac

    unique_fracs = list(reduced_map.values())

    if count > len(unique_fracs):
        raise ValueError("For mange unikke brøker i forhold til max nævner")

    return random.sample(unique_fracs, count)


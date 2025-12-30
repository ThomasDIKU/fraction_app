import random
import math
from typing import List, Tuple


Fraction = Tuple[int, int]


# -------------------------------------------------
# Hjælpefunktioner (interne)
# -------------------------------------------------
def _reduce_fraction(frac: Fraction) -> Fraction:
    n, d = frac
    g = math.gcd(n, d)
    return (n // g, d // g)


def _all_fractions_up_to(max_denominator: int) -> List[Fraction]:
    """
    Genererer ALLE brøker 0 < n/d < 1 med d <= max_denominator
    (inkl. ækvivalente)
    """
    if max_denominator < 2:
        raise ValueError("max_denominator skal være >= 2")

    fractions: List[Fraction] = []
    for d in range(2, max_denominator + 1):
        for n in range(1, d):
            fractions.append((n, d))

    return fractions


# -------------------------------------------------
# Offentligt API
# -------------------------------------------------
def extend_fractions(fractions: List[Fraction], factor: int) -> List[Fraction]:
    """
    Forlænger alle brøker med faktoren factor.
    (n/d -> (factor·n)/(factor·d))
    """
    if factor < 1:
        raise ValueError("Forlængelsesfaktor skal være >= 1")

    return [(n * factor, d * factor) for n, d in fractions]


def generate_random_fractions(
    count: int,
    max_denominator: int,
    allow_equivalent: bool,
    rng: random.Random | None = None
) -> List[Fraction]:
    """
    Genererer tilfældige brøker mellem 0 og 1.

    Parameters
    ----------
    count : int
        Antal brøker
    max_denominator : int
        Maksimal nævner
    allow_equivalent : bool
        Hvis False fjernes ækvivalente brøker
    rng : random.Random | None
        Valgfri random-generator (til determinisme)

    Returns
    -------
    List[(n, d)]
    """

    if count < 1:
        raise ValueError("count skal være >= 1")

    rng = rng or random

    all_fracs = _all_fractions_up_to(max_denominator)

    if allow_equivalent:
        if count > len(all_fracs):
            raise ValueError("For mange brøker i forhold til max nævner")
        return rng.sample(all_fracs, count)

    # Fjern ækvivalente brøker
    reduced_map = {}
    for frac in all_fracs:
        reduced = _reduce_fraction(frac)
        if reduced not in reduced_map:
            reduced_map[reduced] = frac

    unique_fracs = list(reduced_map.values())

    if count > len(unique_fracs):
        raise ValueError("For mange unikke brøker i forhold til max nævner")

    return rng.sample(unique_fracs, count)

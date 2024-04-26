#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script defines a function to simplify boolean algebra expressions,
inspired by Karnaugh Map.
"""

from utils import (
    Term,
    find_essential_prime_implicants,
    find_prime_implicants,
)


class Minterms(object):
    """ Minterms stores expressions for 1s and "don't care". """

    def __init__(
        self, minterms=None, not_cares=None,
    ):
        if minterms is None:
            minterms = []
        if not_cares is None:
            not_cares = []

        self.minterms = minterms
        self.not_cares = not_cares

    def simplify(self):
        prime_implicants = find_prime_implicants(self.minterms, self.not_cares)
        result = find_essential_prime_implicants(prime_implicants, self.minterms)
        return result


def make_karnaugh(str_terms: list[str], terms_not_care: list[str]):
    if not len(str_terms):
        return None

    t_minterms = [Term(term) for term in sorted(str_terms)]
    not_cares = [Term(term) for term in sorted(terms_not_care)]

    minterms = Minterms(t_minterms, not_cares)
    return minterms.simplify()


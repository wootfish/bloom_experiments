#!/usr/bin/env python3

import random
import zlib
import bz2
import matplotlib.pyplot as plt

"""
Script for measuring properties of sparse Bloom filters under compression.
"""

def gen_rand_bloom_bytes(filter_size, num_funcs, num_inserts):
    assert filter_size % 8 == 0

    num_bytes = filter_size // 8
    bloom = [0] * num_bytes
    for _ in range(num_inserts * num_funcs):
        r1 = random.randint(0, num_bytes-1)
        r2 = random.randint(0, 7)
        bloom[r1] |= 1 << r2

    return bytes(bloom)

if __name__ == "__main__":
    filter_size = 2**17
    functions = 3

    members_vs_size_x = []
    members_vs_size_y_bz2 = []
    members_vs_size_y_zlib = []

    sample_size = 10

    for num_elems in range(0, 5000, 50):
        if num_elems % 100 == 0: print(".", end="", flush=True)

        samples_bz2 = []
        samples_zlib = []

        for _ in range(sample_size):
            bloom = gen_rand_bloom_bytes(filter_size, functions, num_elems)
            samples_bz2.append(len(bz2.compress(bloom)))
            samples_zlib.append(len(zlib.compress(bloom)))

        members_vs_size_x.append(num_elems)
        members_vs_size_y_bz2.append(sum(samples_bz2) / len(samples_bz2))
        members_vs_size_y_zlib.append(sum(samples_zlib) / len(samples_zlib))

    plt.plot(members_vs_size_x, members_vs_size_y_bz2)
    plt.plot(members_vs_size_x, members_vs_size_y_zlib)
    plt.show()

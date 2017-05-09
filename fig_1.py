#!/usr/bin/env python3

import random
import zlib
import bz2
import matplotlib.pyplot as plt
import numpy as np
import itertools

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
    size_cap = 10000
    filter_size = 2**16
    functions = 5

    x_vals = []
    y_vals = {"bz2":[], "zlib":[]}

    sample_size = 10

    for num_elems in range(0, size_cap+1, 50):
        x_vals.append(num_elems)
        print(".", end="", flush=True)

        samples_bz2 = []
        samples_zlib = []

        for _ in range(sample_size):
            bloom = gen_rand_bloom_bytes(filter_size, functions, num_elems)
            samples_bz2.append(len(bz2.compress(bloom)))
            samples_zlib.append(len(zlib.compress(bloom)))

        y_vals["bz2"].append(sum(samples_bz2) / len(samples_bz2))
        y_vals["zlib"].append(sum(samples_zlib) / len(samples_zlib))

    plt.plot(x_vals, y_vals["bz2"], "y-", label="k=5, bz2")
    plt.plot(x_vals, y_vals["zlib"], "g-", label="k=5, gzip")

    plt.plot([0, x_vals[-1]], [(2**16)/8, (2**16)/8], "b--", label="uncompressed")

    plt.grid(True)
    plt.legend()

    plt.title("Filter Behavior Under Compression")
    plt.ylabel("Compressed size (in bytes)")
    plt.xlabel("Number of keys in filter")

    plt.show()

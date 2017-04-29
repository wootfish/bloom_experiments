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
    size_cap = 50000
    filter_size = 2**16

    x_vals = []
    y_vals = {1 : {"bz2":[],
                   "zlib":[]},
              2 : {"bz2":[],
                   "zlib":[]},
              3 : {"bz2":[],
                   "zlib":[]},
              4 : {"bz2":[],
                   "zlib":[]}}

    sample_size = 10

    for num_elems in itertools.chain(range(0, 100*25, 50), range(100*25, size_cap, 500)):
        x_vals.append(num_elems)
        print(".", end="", flush=True)

        for functions in (1,2,3,4):
            samples_bz2 = []
            samples_zlib = []

            for _ in range(sample_size):
                bloom = gen_rand_bloom_bytes(filter_size, functions, num_elems)
                samples_bz2.append(len(bz2.compress(bloom)))
                samples_zlib.append(len(zlib.compress(bloom)))

            y_vals[functions]["bz2"].append(sum(samples_bz2) / len(samples_bz2))
            y_vals[functions]["zlib"].append(sum(samples_zlib) / len(samples_zlib))

    # left column
    plt.subplot(2,2,1)

    plt.plot(x_vals[:25], y_vals[1]["bz2"][:25], "r-", label="k=1, bzip2")
    plt.plot(x_vals[:25], y_vals[1]["zlib"][:25], "r--", label="k=1, gzip")

    plt.plot(x_vals[:25], y_vals[2]["bz2"][:25], "y-", label="k=2, bzip2")
    plt.plot(x_vals[:25], y_vals[2]["zlib"][:25], "y--", label="k=2, gzip")

    plt.plot(x_vals[:25], y_vals[3]["bz2"][:25], "g-", label="k=3, bzip2")
    plt.plot(x_vals[:25], y_vals[3]["zlib"][:25], "g--", label="k=3, gzip")

    plt.plot(x_vals[:25], y_vals[4]["bz2"][:25], "b-", label="k=4, bzip2")
    plt.plot(x_vals[:25], y_vals[4]["zlib"][:25], "b--", label="k=4, gzip")

    #plt.plot([0, x_vals[24]], [(2**16)/8, (2**16)/8], "k-", label="raw")

    plt.grid(True)
    plt.legend()

    plt.title("Bloom Filter Characteristics (Few Elements)")
    plt.ylabel("Compressed size (in bytes)")

    plt.subplot(2,2,3)
    x_range = np.arange(0.0, 2500, 10)
    y_vals_1 = (1 - np.exp(-1*x_range/filter_size))
    y_vals_2 = (1 - np.exp(-1*x_range*2/filter_size)) ** 2
    y_vals_3 = (1 - np.exp(-1*x_range*3/filter_size)) ** 3
    y_vals_4 = (1 - np.exp(-1*x_range*4/filter_size)) ** 4
    plt.plot(x_range, y_vals_1, 'r-', label="k=1")
    plt.plot(x_range, y_vals_2, 'y-', label="k=2")
    plt.plot(x_range, y_vals_3, 'g-', label="k=3")
    plt.plot(x_range, y_vals_4, 'b-', label="k=4")

    plt.legend()
    
    plt.xlabel("Number of elements")
    plt.ylabel("False positive probability")
    plt.grid(True)


    # right column
    plt.subplot(2,2,2)

    plt.plot(x_vals, y_vals[1]["bz2"], "r-")
    plt.plot(x_vals, y_vals[1]["zlib"], "r--")

    plt.plot(x_vals, y_vals[2]["bz2"], "y-")
    plt.plot(x_vals, y_vals[2]["zlib"], "y--")

    plt.plot(x_vals, y_vals[3]["bz2"], "g-")
    plt.plot(x_vals, y_vals[3]["zlib"], "g--")

    plt.plot(x_vals, y_vals[4]["bz2"], "b-")
    plt.plot(x_vals, y_vals[4]["zlib"], "b--")

    #plt.plot([0, size_cap], [2**13, 2**13], "k-")

    plt.title("Bloom Filter Characteristics (Many Elements)")
    plt.ylabel("Compressed size (in bytes)")
    plt.grid(True)

    plt.subplot(2,2,4)
    x_range = np.arange(0.0, size_cap, 20)
    y_vals_1 = (1 - np.exp(-1*x_range/filter_size))
    y_vals_2 = (1 - np.exp(-1*x_range*2/filter_size)) ** 2
    y_vals_3 = (1 - np.exp(-1*x_range*3/filter_size)) ** 3
    y_vals_4 = (1 - np.exp(-1*x_range*4/filter_size)) ** 4
    plt.plot(x_range, y_vals_1, 'r-')
    plt.plot(x_range, y_vals_2, 'y-')
    plt.plot(x_range, y_vals_3, 'g-')
    plt.plot(x_range, y_vals_4, 'b-')
    
    plt.xlabel("Number of elements")
    plt.ylabel("False positive probability")
    plt.grid(True)

    plt.show()

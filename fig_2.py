#!/usr/bin/env python3

import random
import zlib
import bz2
import matplotlib.pyplot as plt
import numpy as np
import itertools

if __name__ == "__main__":
    size_cap = 10000
    filter_size = 2**16

    x_range = np.arange(0.0, size_cap, 10)
    y_vals_4 = (1 - np.exp(-1*x_range*4/filter_size)) ** 4
    y_vals_5 = (1 - np.exp(-1*x_range*5/filter_size)) ** 5
    y_vals_6 = (1 - np.exp(-1*x_range*6/filter_size)) ** 6

    plt.plot(x_range, y_vals_4, 'b-', label="k=4")
    plt.plot(x_range, y_vals_5, 'g-', label="k=5")
    plt.plot(x_range, y_vals_6, 'y-', label="k=6")

    plt.legend()
    
    plt.xlabel("Number of elements")
    plt.ylabel("False positive probability")
    plt.grid(True)

    plt.show()

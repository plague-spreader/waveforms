#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

def load_data_as_float32(filename):
    with open(filename, mode="rb") as f:
        return np.frombuffer(f.read(), dtype=np.float32)

t = load_data_as_float32("time_axis")
x = load_data_as_float32("audio.raw")

plt.plot(t, x)
plt.grid(True)
plt.show()

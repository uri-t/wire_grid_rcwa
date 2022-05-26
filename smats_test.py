import numpy as np
from layer import Layer

ys = np.arange(0, 20.0, 0.1)
eps_f = lambda freq: 1 + ys

L = Layer(10, 5, ys, eps_f)

with np.printoptions(precision=4, linewidth=110):
    print(L.S_mats(1)['S11'])

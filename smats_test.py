import numpy as np
from slab import Slab
from material import Material
from layer import Layer

ys = np.arange(0, 20.0, 0.1)
eps_f = lambda freq, ys: 1 + ys

L = Layer(10, eps_f)
nh = 5
with np.printoptions(precision=4, linewidth=110):
    print(L.S_mats(1, ys, nh)['S11'])


print("===============================")


mat = Material(eps=[1, 2], freq = [0, 2])

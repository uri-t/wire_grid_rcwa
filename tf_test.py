from structure import Structure
from slab import Slab
from wires import Wires
import numpy as np
from material import Material

ys = np.arange(0, 20.1, 0.1)
nh = 5

print(ys)

wire_mat = Material(eps = [4, 4], freq = [1, 2])
fill_mat = Material(eps = [3, 3], freq = [1, 2])
subs_mat = Material(eps = [1.95**2, 1.95**2], freq = [1, 2])

s = Structure(ys = ys,
              nh = nh,
              layers = [Wires(wire_mat = wire_mat,
                              fill_mat = fill_mat,
                              wire_fill_frac = 0.8,
                              period = 20,
                              d = 0.5),
                        Slab(subs_mat, 0)])

print(s.tf(1.5))

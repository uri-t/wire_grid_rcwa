from structure import Structure
from slab import Slab
from wires import Wires
import numpy as np
from material import Material
from extractor import Extractor
import warnings

warnings.filterwarnings(action="error", category=np.ComplexWarning)

ys = np.arange(0, 10.1, 0.1)
nh = 51

e0 = 8.854e-12; #F/m = (C/V)/m

freq = np.arange(0.3, 2.25, 0.05)

sig_wires = 1e5
sig_fill = 10

wire_eps = 16 + 1j*sig_wires/(e0*2*np.pi*freq*1e12)
fill_eps_onn = 4 + 1j*sig_fill/(e0*2*np.pi*freq*1e12)
fill_eps_off = 4 + 0*freq

wire_mat = Material(eps = wire_eps, freq = freq)
fill_mat_onn = Material(eps = fill_eps_onn, freq = freq)
fill_mat_off = Material(eps = fill_eps_off, freq = freq)

# subs_mat = Material(eps = [1.95**2, 1.95**2], freq = [1, 2])

s_ref = Structure(ys = ys,
                  nh = nh,
                  layers = [Wires(wire_mat = wire_mat,
                                  fill_mat = fill_mat_off,
                                  wire_fill_frac = 0.8,
                                  period = 10,
                                  d = 0.5)])

s_smp = Structure(ys = ys,
                  nh = nh,
                  layers = [Wires(wire_mat = wire_mat,
                                  fill_mat = fill_mat_onn,
                                  wire_fill_frac = 0.8,
                                  period = 10,
                                  d = 0.5)])

tf = [0.9968 + 0.0003j, 0.9968 + 0.0003j, 0.9968 + 0.0004j,  0.9968 + 0.0004j,  0.9969 + 0.0005j, 0.9969 + 0.0005j, 0.9969 + 0.0005j,  0.9969 + 0.0006j, 0.9969 + 0.0006j, 0.9969 + 0.0007j, 0.9970 + 0.0007j, 0.9970 + 0.0008j, 0.9970 + 0.0008j, 0.9970 + 0.0008j, 0.9970 + 0.0009j, 0.9971 + 0.0009j, 0.9971 + 0.0009j, 0.9971 + 0.0010j, 0.9971 + 0.0010j, 0.9972 + 0.0010j, 0.9972 + 0.0011j, 0.9972 + 0.0011j, 0.9972 + 0.0011j, 0.9973 + 0.0012j, 0.9973 + 0.0012j, 0.9973 + 0.0012j, 0.9974 + 0.0013j, 0.9974 + 0.0013j, 0.9974 + 0.0013j, 0.9974 + 0.0013j, 0.9975 + 0.0014j, 0.9975 + 0.0014j, 0.9975 + 0.0014j, 0.9976 + 0.0014j, 0.9976 + 0.0014j, 0.9976 + 0.0015j, 0.9977 + 0.0015j, 0.9977 + 0.0015j, 0.9977 + 0.0015j]

extracted = Extractor.extract(s_ref, s_smp, fill_mat_onn, freq, tf, 4 + 0j)
print(extracted)

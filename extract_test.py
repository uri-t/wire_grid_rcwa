import sys

sys.path.append('/home/uri/Desktop/grad')

import numpy as np
import wire_grid_rcwa as wgr

# import time domain data
d_on = np.genfromtxt('ds_test_on.txt', delimiter = "\t")
d_off = np.genfromtxt('ds_test_off.txt', delimiter = "\t") 

t_smp = d_on[:,0]; A_smp = d_on[:,1]
t_ref = d_off[:,0]; A_ref = d_off[:,1]

freq = np.arange(0.3, 2.25, 0.05)
tf = wgr.transfer_function(t_smp, A_smp, t_ref, A_ref,
                           freqs = freq, zero_padding = 2**18)

# set up geometry
ys = np.arange(0, 10 + 10/255, 10/255)
nh = 51

sig_wires = 1e5; sig_fill = 10; wire_eps = 16; fill_eps = 9;

wire_mat = wgr.Material(eps = wire_eps, cond = sig_wires,  freq = freq)
fill_mat_onn = wgr.Material(eps = fill_eps, cond = sig_fill, freq = freq)
fill_mat_off = wgr.Material(eps = fill_eps, freq = freq)
subs_mat = wgr.Material(eps = 1.95**2, freq = freq)

s_ref = wgr.Structure(ys = ys, nh = nh,
                    layers = [wgr.Wires(wire_mat = wire_mat,
                                        fill_mat = fill_mat_off,
                                        wire_fill_frac = 0.8,
                                        period = 10,
                                        d = 0.5)],
                    half_space_tr = wgr.HalfSpaceTr(subs_mat))

s_smp = wgr.Structure(ys = ys, nh = nh,
                      layers = [wgr.Wires(wire_mat = wire_mat,
                                          fill_mat = fill_mat_onn,
                                          wire_fill_frac = 0.8,
                                          period = 10,
                                          d = 0.5)],
                      half_space_tr = wgr.HalfSpaceTr(subs_mat))



extracted = wgr.Extractor.extract(s_ref, s_smp,
                                  fill_mat_onn, freq, tf, 9.01 - 0.001*1j)
print(extracted)


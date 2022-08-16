import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.append('..')
import wire_grid_rcwa as wgr

# import time domain data
d_on = np.genfromtxt('simulation_data/ds_test/trace_on_clean.txt')
d_off = np.genfromtxt('simulation_data/ds_test/trace_off_clean.txt')

t_smp = d_on[:,0]; A_smp = d_on[:,1]
t_ref = d_off[:,0]; A_ref = d_off[:,1]

freq = np.arange(0.3, 2.25, 0.05)
tf = wgr.transfer_function(t_smp, A_smp, t_ref, A_ref,
                           freqs = freq, zero_padding = 2**18)

# set up geometry
period = 12
ys = np.linspace(0, period, 256)
nh = 23

sig_wires = 1.5e5; sig_fill = 10; wire_eps = 9; fill_eps = 9;

wire_mat = wgr.Material(eps = wire_eps, cond = sig_wires,  freq = freq)
fill_mat_onn = wgr.Material(eps = fill_eps, cond = sig_fill, freq = freq)
fill_mat_off = wgr.Material(eps = fill_eps, freq = freq)
subs_mat = wgr.Material(eps = 1.95**2, freq = freq)

d_wires = 0.25
d_slab = 0.5
f = 0.66

s_ref = wgr.Structure(ys = ys, nh = nh,
                    layers = [wgr.Slab(fill_mat_off, d_slab),
                              wgr.Wires(wire_mat = wire_mat,
                                        fill_mat = fill_mat_off,
                                        wire_fill_frac = f,
                                        period = 12,
                                        d = d_wires)],
                    half_space_tr = wgr.HalfSpaceTr(subs_mat))

s_smp = wgr.Structure(ys = ys, nh = nh,
                      layers = [wgr.Slab(fill_mat_onn, d_slab),
                                wgr.Wires(wire_mat = wire_mat,
                                          fill_mat = fill_mat_onn,
                                          wire_fill_frac = f,
                                          period = period,
                                          d = d_wires)],
                      half_space_tr = wgr.HalfSpaceTr(subs_mat))



extracted = wgr.Extractor.extract(s_ref, s_smp,
                                  fill_mat_onn, freq, tf, 9.01 - 0.001*1j)
#print(extracted)
cond = wgr.eps_to_photocond(freq, extracted, fill_eps)

eps_sim_re = np.genfromtxt('simulation_data/ds_test/eps_on_re_clean.txt')
eps_sim_im = np.genfromtxt('simulation_data/ds_test/eps_on_im_clean.txt')

freq_sim = eps_sim_re[:,0]

eps_sim = eps_sim_re[:,1] - 1j*eps_sim_im[:,1]
cond_sim = wgr.eps_to_photocond(freq_sim, eps_sim, fill_eps)

plt.plot(freq_sim, np.real(cond_sim), 'b')
plt.plot(freq_sim, np.imag(cond_sim), 'b--')
plt.plot(freq, np.real(cond), 'r')
plt.plot(freq, np.imag(cond), 'r--')
plt.show()

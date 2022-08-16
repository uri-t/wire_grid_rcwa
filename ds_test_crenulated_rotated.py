import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.append('..')
import wire_grid_rcwa as wgr


plt.style.use(['./general.mplstyle', './single_column.mplstyle'])

# import time domain data
d_on_x = np.genfromtxt(
    'simulation_data/ds_test_crenulated/trace_on_11_deg_x.txt')
d_on_y = np.genfromtxt(
    'simulation_data/ds_test_crenulated/trace_on_11_deg_y.txt')

d_off_x = np.genfromtxt(
    'simulation_data/ds_test_crenulated/trace_off_11_deg_x.txt')
d_off_y = np.genfromtxt(
    'simulation_data/ds_test_crenulated/trace_off_11_deg_y.txt')


inds = d_on_x[:,0] < 13
d_on_xy = np.column_stack((d_on_x[inds,1], d_on_y[inds,1]))
d_off_xy = np.column_stack((d_off_x[inds,1], d_off_y[inds,1]))


A_on = d_on_xy @ np.array([0.2, 1])
A_off = d_off_xy @ np.array([0.2, 1])

t = d_on_x[inds,0]


freq = np.arange(0.3, 2.25, 0.05)
tf = wgr.transfer_function(t, A_on, t, A_off,
                           freqs = freq, zero_padding = 2**18)


# set up geometry
period = 12
ys = np.linspace(0, period, 256)
nh = 23

sig_wires = 1.5e5; sig_fill = 10; wire_eps = 9; fill_eps = 9;

wire_mat = wgr.Material(eps = wire_eps, cond = sig_wires,  freq = freq)
air_mat = wgr.Material(eps = 1, freq = freq)
fill_mat_onn = wgr.Material(eps = fill_eps, cond = sig_fill, freq = freq)
fill_mat_off = wgr.Material(eps = fill_eps, freq = freq)
subs_mat = wgr.Material(eps = 1.95**2, freq = freq)

d_wires = 0.25
d_smp = 0.5

d_slab = d_smp - d_wires
f = 0.66

s_ref = wgr.Structure(ys = ys, nh = nh,
                    layers = [wgr.Wires(wire_mat = fill_mat_off,
                                        fill_mat = air_mat,
                                        wire_fill_frac = f,
                                        period = 12,
                                        d = d_wires),
                              wgr.Slab(fill_mat_off, d_slab),
                              wgr.Wires(wire_mat = wire_mat,
                                        fill_mat = fill_mat_off,
                                        wire_fill_frac = f,
                                        period = 12,
                                        d = d_wires)],
                    half_space_tr = wgr.HalfSpaceTr(subs_mat))

s_smp = wgr.Structure(ys = ys, nh = nh,
                      layers = [wgr.Wires(wire_mat = fill_mat_onn,
                                        fill_mat = air_mat,
                                        wire_fill_frac = f,
                                        period = 12,
                                        d = d_wires),
                                wgr.Slab(fill_mat_onn, d_slab),
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

plt.ylabel('Conductivity (S/m)')
plt.xlabel('Frequency (THz)')

plt.show()

import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.append('..')
import wire_grid_rcwa as wgr


plt.style.use(['./general.mplstyle', './single_column.mplstyle'])

freq = np.arange(0.3, 2.25, 0.05)

def get_tf(fname_on, fname_off):
    d_on = np.genfromtxt(fname_on)
    d_off = np.genfromtxt(fname_off)
  

    t_smp = d_on[:,0]; A_smp = d_on[:,1]
    t_ref = d_off[:,0]; A_ref = d_off[:,1]

    A_smp = A_smp[t_smp < 13]
    t_smp = t_smp[t_smp < 13]

    A_ref = A_ref[t_ref < 13]
    t_ref = t_ref[t_ref < 13]

    tf = wgr.transfer_function(t_smp, A_smp, t_ref, A_ref,
                               freqs = freq, zero_padding = 2**18)
    return(tf)


# get no wire tf

tf = get_tf('simulation_data/effective_medium/trace_no_wire_100_sm_100nm_on.txt',
            'simulation_data/effective_medium/trace_no_wire_100_sm_100nm_off.txt')

# set up geometry
period = 12
ys = np.linspace(0, period, 256)
nh = 23

sig_wires = 1.5e5; sig_fill = 10; wire_eps = 9; fill_eps = 9;

wire_mat = wgr.Material(eps = wire_eps, cond = sig_wires,  freq = freq)
fill_mat_on = wgr.Material(eps = fill_eps, cond = sig_fill, freq = freq)
fill_mat_off = wgr.Material(eps = fill_eps, freq = freq)
subs_mat = wgr.Material(eps = 1.95**2, freq = freq)

d_wires = 0.25
d_smp = 0.75

d_slab = d_smp - d_wires
f = 0.66

s_ref = wgr.Structure(ys = ys, nh = nh,
                    layers = [wgr.Slab(fill_mat_off, d_smp)],
                              half_space_tr = wgr.HalfSpaceTr(subs_mat))
                      
s_smp = wgr.Structure(ys = ys, nh = nh,
                    layers = [wgr.Slab(fill_mat_on, d_smp)],
                              half_space_tr = wgr.HalfSpaceTr(subs_mat))

extracted = wgr.Extractor.extract(s_ref, s_smp,
                                  fill_mat_on, freq, tf, 9.01 - 0.001*1j)
cond = wgr.eps_to_photocond(freq, extracted, fill_eps)

plt.plot(freq, np.real(cond), 'r')
plt.plot(freq, np.imag(cond), 'r--')


# process wires

tf = get_tf('simulation_data/effective_medium/trace_wires_100_sm_100nm_on.txt',
            'simulation_data/effective_medium/trace_wires_100nm_off.txt')

s_ref = wgr.Structure(ys = ys, nh = nh,
                    layers = [wgr.Slab(fill_mat_off, d_slab),
                              wgr.Wires(wire_mat = wire_mat,
                                        fill_mat = fill_mat_off,
                                        wire_fill_frac = f,
                                        period = period,
                                        d = d_wires)],
                              half_space_tr = wgr.HalfSpaceTr(subs_mat))
                      
s_smp = wgr.Structure(ys = ys, nh = nh,
                    layers = [wgr.Slab(fill_mat_on, d_slab),
                              wgr.Wires(wire_mat = wire_mat,
                                          fill_mat = fill_mat_on,
                                          wire_fill_frac = f,
                                          period = period,
                                          d = d_wires)],
                              half_space_tr = wgr.HalfSpaceTr(subs_mat))

extracted = wgr.Extractor.extract(s_ref, s_smp,
                                  fill_mat_on, freq, tf, 9.01 - 0.001*1j)
cond = wgr.eps_to_photocond(freq, extracted, fill_eps)

plt.plot(freq, np.real(cond), 'b')
plt.plot(freq, np.imag(cond), 'b--')

plt.show()

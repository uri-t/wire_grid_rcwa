import sys

sys.path.append('/home/uri/Desktop/grad')

import numpy as np
import wire_grid_rcwa as wgr

# import time domain data
d_on = np.genfromtxt('ds_test_on.txt', delimiter = "\t")
d_off = np.genfromtxt('ds_test_off.txt', delimiter = "\t") 

t_smp = d_on[:,0]
A_smp = d_on[:,1]

t_ref = d_off[:,0]
A_ref = d_off[:,1]

freq = np.arange(0.3, 2.25, 0.05)
tf = wgr.transfer_function(t_smp, A_smp, t_ref, A_ref, freq, 2**18)


# set up geometry
ys = np.arange(0, 10 + 10/255, 10/255)
nh = 51

e0 = 8.854e-12; #F/m = (C/V)/m


sig_wires = 1e5
sig_fill = 10

wire_eps = 16 - 1j*sig_wires/(e0*2*np.pi*freq*1e12)
fill_eps_onn = 9 - 1j*sig_fill/(e0*2*np.pi*freq*1e12)
fill_eps_off = 9 + 0*freq

wire_mat = wgr.Material(eps = wire_eps, freq = freq)
fill_mat_onn = wgr.Material(eps = fill_eps_onn, freq = freq)
fill_mat_off = wgr.Material(eps = fill_eps_off, freq = freq)

subs_mat = wgr.Material(eps = 1.95**2 + freq*0, freq = freq)

s_ref = wgr.Structure(ys = ys,
                      nh = nh,
                      layers = [wgr.Wires(wire_mat = wire_mat,
                                          fill_mat = fill_mat_off,
                                          wire_fill_frac = 0.8,
                                          period = 10,
                                          d = 0.5)],
                      half_space_tr = wgr.HalfSpaceTr(subs_mat))

s_smp = wgr.Structure(ys = ys,
                      nh = nh,
                      layers = [wgr.Wires(wire_mat = wire_mat,
                                          fill_mat = fill_mat_onn,
                                          wire_fill_frac = 0.8,
                                          period = 10,
                                          d = 0.5)],
                      half_space_tr = wgr.HalfSpaceTr(subs_mat))



extracted = wgr.Extractor.extract(s_ref, s_smp,
                                  fill_mat_onn, freq, tf, 9.01 - 0.001*1j)
print(extracted)


# Error map
eps_re = np.arange(9.00, 9.04, 0.005)
eps_im = np.arange(-2e-2, 2e-2, 5e-3)

costs = np.zeros((len(eps_im), len(eps_re)))

for i in range(0, len(eps_im)):
    for j in range(0, len(eps_re)):
        trial_eps = eps_re[j] + 1j*eps_im[i]
        costs[i,j] = wgr.Extractor.cost(wgr.Structure.trial_tf_smp_ref(s_smp,
                                                                   s_ref,
                                                                   fill_mat_onn,
                                                                   0.5, trial_eps),
                                        tf[4])

        print(trial_eps)
        
plt.imshow(costs, extent = [min(eps_re), max(eps_re), min(eps_im), max(eps_im)])
plt.show()

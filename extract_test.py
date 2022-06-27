import sys

sys.path.append('/home/uri/Desktop/grad')

import numpy as np
import wire_grid_rcwa as wgr

ys = np.arange(0, 10 + 10/255, 10/255)
nh = 51

e0 = 8.854e-12; #F/m = (C/V)/m

freq = np.arange(0.3, 2.25, 0.05)

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




# sigma = 10 (?)
#tf = [0.9968 + 0.0003j, 0.9968 + 0.0003j, 0.9968 + 0.0004j,  0.9968 + 0.0004j,  0.9969 + 0.0005j, 0.9969 + 0.0005j, 0.9969 + 0.0005j,  0.9969 + 0.0006j, 0.9969 + 0.0006j, 0.9969 + 0.0007j, 0.9970 + 0.0007j, 0.9970 + 0.0008j, 0.9970 + 0.0008j, 0.9970 + 0.0008j, 0.9970 + 0.0009j, 0.9971 + 0.0009j, 0.9971 + 0.0009j, 0.9971 + 0.0010j, 0.9971 + 0.0010j, 0.9972 + 0.0010j, 0.9972 + 0.0011j, 0.9972 + 0.0011j, 0.9972 + 0.0011j, 0.9973 + 0.0012j, 0.9973 + 0.0012j, 0.9973 + 0.0012j, 0.9974 + 0.0013j, 0.9974 + 0.0013j, 0.9974 + 0.0013j, 0.9974 + 0.0013j, 0.9975 + 0.0014j, 0.9975 + 0.0014j, 0.9975 + 0.0014j, 0.9976 + 0.0014j, 0.9976 + 0.0014j, 0.9976 + 0.0015j, 0.9977 + 0.0015j, 0.9977 + 0.0015j, 0.9977 + 0.0015j]


# ds example
tf_re = [1.0000,
         1.0000,
         1.0000,
         1.0000,
         0.9999,
         0.9999,
         0.9999,
         0.9999,
         0.9999,
         0.9999,
         0.9999,
         0.9998,
         0.9998,
         0.9998,
         0.9998,
         0.9998,
         0.9997,
         0.9997,
         0.9997,
         0.9997,
         0.9997,
         0.9996,
         0.9996,
         0.9996,
         0.9996,
         0.9996,
         0.9996,
         0.9995,
         0.9995,
         0.9995,
         0.9995,
         0.9995,
         0.9995,
         0.9995,
         0.9994,
         0.9994,
         0.9994,
         0.9994,
         0.9994]
tf_im = [0.1120,
         0.1330,
         0.1560,
         0.1702,
         0.1888,
         0.1999,
         0.2161,
         0.2269,
         0.2416,
         0.2522,
         0.2645,
         0.2735,
         0.2825,
         0.2896,
         0.2954,
         0.3004,
         0.3040,
         0.3075,
         0.3091,
         0.3110,
         0.3103,
         0.3099,
         0.3069,
         0.3042,
         0.2993,
         0.2947,
         0.2887,
         0.2826,
         0.2760,
         0.2681,
         0.2604,
         0.2495,
         0.2405,
         0.2274,
         0.2177,
         0.2034,
         0.1942,
         0.1803,
         0.1711]

tf_re = [0.999976690009854,
         0.999977771778990,
         0.999959480242461,
         0.999951057737054,
         0.999934988368257,
         0.999923529648071,
         0.999909611967500,
         0.999896188396895,
         0.999882122494947,
         0.999866115216682,
         0.999850483045693,
         0.999832290319276,
         0.999815408472963,
         0.999795671636066,
         0.999778390657617,
         0.999759367835636,
         0.999741870976691,
         0.999722973706459,
         0.999704938717264,
         0.999685973512670,
         0.999667328837875,
         0.999648600874602,
         0.999629892117628,
         0.999612125409453,
         0.999594024110992,
         0.999577631809009,
         0.999560247292538,
         0.999544900490737,
         0.999527833792944,
         0.999512950630205,
         0.999496177493370,
         0.999481191390486,
         0.999465929458926,
         0.999452549753168,
         0.999440134136425,
         0.999427766032791,
         0.999418454947968,
         0.999405079549371,
         0.999397835133319]

tf_im = freq*0 + tf_im

tf_im = tf_im/1e3
tf = tf_re - 1j*tf_im

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
        costs[i,j] = wgr.Extractor.cost(Structure.trial_tf_smp_ref(s_smp,
                                                                   s_ref,
                                                                   fill_mat_onn,
                                                                   0.5, trial_eps),
                                        tf[4])

        print(trial_eps)
        
plt.imshow(costs, extent = [min(eps_re), max(eps_re), min(eps_im), max(eps_im)])
plt.show()

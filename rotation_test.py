import sys
from pathlib import Path
sys.path.append('..')
import numpy as np
import wire_grid_rcwa as wgr
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

plt.style.use(['./general.mplstyle', './single_column.mplstyle'])

smps = pd.read_csv('experimental_data/rotation_table.csv')\
        .set_index('degrees')\
        .to_dict(orient='index')

path = '/home/uri/Desktop/grad/wire_grid_rcwa/experimental_data/thz_traces/2022_08_04/Aug04_'

def process_wires(deg):
    w_wire, w_smp = [8, 4] 
    period = w_wire + w_smp
    f = w_wire/period

    d_wires = 0.25
    d_layer = 0.84 

    nh = 25
    y_pts = 256
    ys = np.linspace(0, period, num = y_pts)
    
    freq = np.arange(0.4, 2.3, 0.1)

    eps_off = 6**2
    subs_mat = wgr.Material(eps = 1.95**2, freq = freq)
    air_mat = wgr.Material(eps = 1, freq = freq)
    wire_mat = wgr.Material(eps = 10, cond = 1.5e5, freq = freq)
    fill_mat_on = wgr.Material(eps = eps_off, freq = freq)
    fill_mat_off = wgr.Material(eps = eps_off, freq = freq)

    smp_slab = wgr.Slab(fill_mat_on, d_layer)
    ref_slab = wgr.Slab(fill_mat_off, d_layer)
    wires_on = wgr.Wires(wire_mat = wire_mat,
                         fill_mat = fill_mat_on,
                         wire_fill_frac = f,
                         period = period,
                         d = d_wires)

    wires_off = wgr.Wires(wire_mat = wire_mat,
                          fill_mat = fill_mat_off,
                          wire_fill_frac = f,
                          period = period,
                          d = d_wires)
    
    wires_wo3_on = wgr.Wires(wire_mat = air_mat,
                             fill_mat = fill_mat_on,
                             wire_fill_frac = f,
                             period = period,
                             d = d_wires)

    wires_wo3_off = wgr.Wires(wire_mat = air_mat,
                              fill_mat = fill_mat_off,
                              wire_fill_frac = f,
                              period = period,
                              d = d_wires)
    
    
    s_ref = wgr.Structure(ys = ys, nh = nh,
                          layers = [wires_wo3_off, ref_slab, wires_off],
                          half_space_tr = wgr.HalfSpaceTr(subs_mat))

    s_smp = wgr.Structure(ys = ys, nh = nh,
                          layers = [wires_wo3_on, smp_slab, wires_on],
                          half_space_tr = wgr.HalfSpaceTr(subs_mat))


    diff_fname = path + ("%03d" % smps[deg]['smp']) + '.tim'
    off_fname = path + ("%03d" % smps[deg]['ref']) + '.tim'

    d_diff = np.genfromtxt(diff_fname)
    d_off =  np.genfromtxt(off_fname)

    t_smp = t_ref = d_diff[:,0]
    A_ref = d_off[:,1]
    A_smp = A_ref + d_diff[:,1]

    
    tf = wgr.transfer_function(t_smp, A_smp, t_ref, A_ref,
                               freqs = freq, zero_padding = 2**18)



    eps_extracted = wgr.Extractor.extract(s_ref, s_smp,
                                          fill_mat_on, freq, tf,
                                          start = fill_mat_on.get_eps(freq[0]))
    
    
    cond = wgr.eps_to_photocond(freq, eps_extracted, eps_off)
        
    plt.plot(freq, np.real(cond), 'b')
    plt.plot(freq, np.imag(cond), 'b--')
    plt.xlabel('Frequency (THz)')
    plt.ylabel('Conductivity (S/m)')



for deg in smps:
    process_wires(deg)

plt.show()

import sys
from pathlib import Path
sys.path.append('..')
import numpy as np
import wire_grid_rcwa as wgr
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd


smps = pd.read_csv('experimental_data/table.csv')\
         .set_index('sample_no')\
         .to_dict(orient='index')

def process_wires(smp_no):
    trace_path = 'experimental_data/thz_traces'

    diff_fname = Path(trace_path, smps[smp_no]['d_on'])\
        .with_suffix('.tim')
    off_fname = Path(trace_path, smps[smp_no]['d_off'])\
        .with_suffix('.tim')
    
    d_diff = np.genfromtxt(diff_fname)
    d_off =  np.genfromtxt(off_fname)

    t_smp = t_ref = d_diff[:,0]
    A_ref = d_off[:,1]
    A_smp = A_ref + d_diff[:,1]

    freq = np.arange(0.2, 2.3, 0.1)
    
    tf = wgr.transfer_function(t_smp, A_smp, t_ref, A_ref,
                               freqs = freq, zero_padding = 2**18)


    # set up geometry
    w_wire, w_smp = [float(x) for x in 
                     str.split(smps[smp_no]['sample_type'],":")]

    period = w_wire + w_smp
    f = w_wire/period

    d_wires = 0.250
    d_layer = smps[smp_no]['thickness'] - d_wires

    nh = 25
    y_pts = 128
    ys = np.linspace(0, period, num = y_pts)

    eps_off = 6**2
    subs_mat = wgr.Material(eps = 1.95**2, freq = freq)
    wire_mat = wgr.Material(eps = 10, cond = 1.5e5, freq = freq)
    fill_mat_on = wgr.Material(eps = eps_off, freq = freq)
    fill_mat_off = wgr.Material(eps = eps_off, freq = freq)

    smp_slab = wgr.Slab(fill_mat_off, d_layer)
    wires_on = wgr.Wires(wire_mat = wire_mat,
                         fill_mat = fill_mat_off,
                         wire_fill_frac = f,
                         period = period,
                         d = d_wires)
    ref_slab = wgr.Slab(fill_mat_on, d_layer)
    wires_off = wgr.Wires(wire_mat = wire_mat,
                          fill_mat = fill_mat_on,
                          wire_fill_frac = f,
                          period = period,
                          d = d_wires)
    
    s_ref = wgr.Structure(ys = ys, nh = nh, layers = [smp_slab, wires_on],
                          half_space_tr = wgr.HalfSpaceTr(subs_mat))

    s_smp = wgr.Structure(ys = ys, nh = nh, layers = [ref_slab, wires_off],
                          half_space_tr = wgr.HalfSpaceTr(subs_mat))

    eps_extracted = wgr.Extractor.extract(s_ref, s_smp,
                                          fill_mat_on, freq, tf,
                                          start = fill_mat_on.get_eps(freq[0]))
    
    
    cond = wgr.eps_to_photocond(freq, eps_extracted, eps_off)
        
    plt.plot(freq, np.real(cond), 'b')
    plt.plot(freq, np.imag(cond), 'b--')


    return {'freq': freq, 'cond': cond}


def process_no_wires(smp_no):
    trace_path = 'experimental_data/thz_traces'

    diff_fname = Path(trace_path, smps[smp_no]['d_on'])\
        .with_suffix('.tim')
    off_fname = Path(trace_path, smps[smp_no]['d_off'])\
        .with_suffix('.tim')
    
    d_diff = np.genfromtxt(diff_fname)
    d_off =  np.genfromtxt(off_fname)

    t_smp = t_ref = d_diff[:,0]
    A_ref = d_off[:,1]
    A_smp = A_ref + d_diff[:,1]

    freq = np.arange(0.2, 2.3, 0.1)
    
    tf = wgr.transfer_function(t_smp, A_smp, t_ref, A_ref,
                               freqs = freq, zero_padding = 2**18)

    # set up geometry
    d_layer = smps[smp_no]['thickness']

    nh = 25
    y_pts = 128
    period = 12
    ys = np.linspace(0, period, num = y_pts)

    eps_off = 6**2
    subs_mat = wgr.Material(eps = 1.95**2, freq = freq)
    fill_mat_on = wgr.Material(eps = eps_off, freq = freq)
    fill_mat_off = wgr.Material(eps = eps_off, freq = freq)

    
    s_ref = wgr.Structure(ys = ys, nh = nh,
                          layers = [wgr.Slab(fill_mat_off, d_layer)],
                          half_space_tr = wgr.HalfSpaceTr(subs_mat))

    s_smp = wgr.Structure(ys = ys, nh = nh,
                          layers = [wgr.Slab(fill_mat_on, d_layer)],
                          half_space_tr = wgr.HalfSpaceTr(subs_mat))

    eps_extracted = wgr.Extractor.extract(s_ref, s_smp,
                                          fill_mat_on, freq, tf,
                                          start = fill_mat_on.get_eps(freq[0]))
    
    
    cond = wgr.eps_to_photocond(freq, eps_extracted, eps_off)
        
    plt.plot(freq, np.real(cond), 'r')
    plt.plot(freq, np.imag(cond), 'r--')


    return {'freq': freq, 'cond': cond}



for smp in smps:
    if smps[smp]['sample_type'] == 'no wire':
        process_no_wires(smp)
    else:
        process_wires(smp)

plt.show()

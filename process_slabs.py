import sys
sys.path.append('..')
import numpy as np
import wire_grid_rcwa as wgr
import matplotlib.pyplot as plt
import matplotlib as mpl
import re
import glob
import os
from tqdm import tqdm

plt.style.use(['./general.mplstyle', './single_column.mplstyle'])

def process_slab(path, name, y_pts, nh, ax = None, **kwargs):
    # import time domain data
    d_on = np.genfromtxt(f'{path}/{name}_smp_post.tsv', skip_header = 2)
    d_off = np.genfromtxt(f'{path}/{name}_ref_post.tsv', skip_header = 2)

    t_smp = d_on[:,0]; A_smp = d_on[:,1]
    t_ref = d_off[:,0]; A_ref = d_off[:,1]

    # trim traces to cut out second reflection from substrate
    inds_smp = t_smp <= 13
    inds_ref = t_ref <= 13
    t_smp = t_smp[inds_smp]; A_smp = A_smp[inds_smp]
    t_ref = t_ref[inds_ref]; A_ref = A_ref[inds_ref]

    # process geometry parameters
    keys = re.findall("_*([a-zA-Z_]+)_[0-9]", name)
    values = [float(x) for x in re.findall("_([0-9.]+)", name)]
    params = dict(zip(keys, values))

    #set up geometry
    freq = np.arange(0.2, 2.15,0.1)
    tf = wgr.transfer_function(t_smp, A_smp, t_ref, A_ref,
                               freqs = freq, zero_padding = 2**18)

    period = params['period']
    
    ys = np.linspace(0, period, num = y_pts)

    
    subs_mat = wgr.Material(eps = 1.95**2, freq = freq)
    fill_mat_on = wgr.Material(eps = params['eb'], cond = params['sigb'],
                               freq = freq)
    fill_mat_off = wgr.Material(eps = params['eb'], freq = freq)

    d_photo = params['d_smp']
    s_ref = wgr.Structure(ys = ys, nh = nh,
                          layers = [wgr.Slab(fill_mat_off, d_photo)],
                          half_space_tr = wgr.HalfSpaceTr(subs_mat))

    s_smp = wgr.Structure(ys = ys, nh = nh,
                          layers = [wgr.Slab(fill_mat_on, d_photo)],
                          half_space_tr = wgr.HalfSpaceTr(subs_mat))
    
    eps_extracted = wgr.Extractor.extract(s_ref, s_smp,
                                          fill_mat_on, freq, tf,
                                          start = fill_mat_on.get_eps(freq[0]))




    cond = wgr.eps_to_photocond(freq, eps_extracted, params['eb'])

    sigb = params['sigb']
    pct_err_re = 100*(np.real(cond) - sigb)/sigb
    pct_err_im = 100*(np.imag(cond) - 0)/sigb

    if not ax:
        fig, ax = plt.subplots()
        
    ax.plot(freq, pct_err_re, **kwargs)
    ax.plot(freq, pct_err_im, '--', **kwargs)
    ax.set_title(name, fontsize = 4)

    return {'params': params,
            'pct_err_re': pct_err_re,
            'pct_err_im': pct_err_im,
            'freq': freq }


path = 'simulation_data/wires_on_off_w_photoexcited_layer_results/slab_70'
name = 'd_wires_0.5_d_smp_0.75_ea_9_eb_16_f_0_period_10_siga_150000_sigb_1'
y_pts = 256
nh = 23
process_slab(path, name, y_pts, nh)
plt.legend(['Re', 'Im'])
plt.ylabel('Error (%)')
plt.xlabel('Frequency (THz)')
plt.show()

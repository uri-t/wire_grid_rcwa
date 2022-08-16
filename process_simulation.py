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

def process_simulation(path, name, y_pts, nh, ax = None, **kwargs):
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
    wire_mat = wgr.Material(eps = params['ea'], cond = params['siga'],
                            freq = freq)
    fill_mat_on = wgr.Material(eps = params['eb'], cond = params['sigb'],
                               freq = freq)
    fill_mat_off = wgr.Material(eps = params['eb'], freq = freq)

    d_photo = params['d_smp'] - params['d_wires']
    s_ref = wgr.Structure(ys = ys, nh = nh,
                          layers = [wgr.Slab(fill_mat_off, d_photo),
                                    wgr.Wires(wire_mat = wire_mat,
                                              fill_mat = fill_mat_off,
                                              wire_fill_frac = params['f'],
                                              period = period,
                                              d = params['d_wires'])],
                          half_space_tr = wgr.HalfSpaceTr(subs_mat))

    s_smp = wgr.Structure(ys = ys, nh = nh,
                          layers = [wgr.Slab(fill_mat_on, d_photo),
                                    wgr.Wires(wire_mat = wire_mat,
                                              fill_mat = fill_mat_on,
                                              wire_fill_frac = params['f'],
                                              period = period,
                                              d = params['d_wires'])],
                          half_space_tr = wgr.HalfSpaceTr(subs_mat))
    eps_extracted = wgr.Extractor.extract(s_ref, s_smp,
                                          fill_mat_on, freq, tf,
                                          start = fill_mat_on.get_eps(freq[0]))

    
    if not ax:
        fig, ax = plt.subplots()
    
    eps_sim = np.array([fill_mat_on.get_eps(x) for x in freq])
    cond = wgr.eps_to_photocond(freq, eps_extracted, params['eb'])

    sigb = params['sigb']
    pct_err_re = 100*(np.real(cond) - sigb)/sigb
    pct_err_im = 100*(np.imag(cond) - 0)/sigb

    ax.plot(freq, pct_err_re, **kwargs)
    ax.plot(freq, pct_err_im, '--', **kwargs)
    ax.set_title(name, fontsize = 4)

    return {'params': params,
            'pct_err_re': pct_err_re,
            'pct_err_im': pct_err_im,
            'freq': freq }

def plot_conv(path, name, ax, f, keys):
    #nhs = [5,7,9,11,13,15,17,19,21,23]

    nhs = [11,15,19,23]
    
    pts = mpl.colors.Normalize()(nhs)
    for i in range(0, len(nhs)):
        
        data = process_simulation(path, name, 128, nhs[i], ax = ax,
                                  color = plt.get_cmap('cool')(pts[i]),
                                  alpha = 0.5)

        params = data['params']
        freq = data['freq']
        pct_err_re = data['pct_err_re']
        pct_err_im = data['pct_err_im']
        
        
        for j in range(0, len(freq)):
            for key in keys:
                f.write(str(params[key]) + ',')
            f.write(str(freq[j]) + ',')
            f.write(str(pct_err_re[j]) + ',')
            f.write(str(pct_err_im[j]) + ',')
            f.write(path + ",")
            f.write(str(nhs[i]))
            f.write("\n")

        



path_base = '/home/uri/Desktop/grad/wire_grid_rcwa/simulation_data/wires_on_off_w_photoexcited_layer_results/'

cells_per_wavelength = ['70', '80', '90']


with open("extraction_data.txt", 'w') as f:
    keys = ['d_wires', 'd_smp', 'ea', 'eb', 'f', 'period', 'siga', 'sigb']
    for key in keys:
            f.write(f'{key},')

    f.write('freq,pct_re,pct_im,path,nh\n')


    for cpw in cells_per_wavelength:
        path = path_base + cpw
        fnames = [os.path.basename(x) for x in glob.glob(f'{path}/*.tsv')]
        fnames = [x[:-13] for x in fnames]
        fnames = list(set(fnames))
        print(len(fnames))

        n_row = int(np.ceil(np.sqrt(len(fnames))))
        n_col = int(np.ceil(len(fnames)/n_row))

        fig, axs = plt.subplots(n_row, n_col, constrained_layout= True)
    
        for ii in tqdm(range(0, n_row)):
            for jj in tqdm(range(0, n_col)):
                ind = ii*n_col + jj
                print(f'===== {ind} ======')
                if ind < len(fnames):
                    plot_conv(path, fnames[ind], axs[ii, jj], f, keys)
            
            
            
plt.show()

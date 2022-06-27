import warnings
import numpy as np
import matplotlib.pyplot as plt

def time_pad(t_smp, A_smp, t_ref, A_ref):

    # warn about discrepancies between time traces
    dt_ref = np.mean(np.diff(t_ref))
    dt_smp = np.mean(np.diff(t_smp))

    pct_diff = abs(dt_ref-dt_smp)/min([dt_ref, dt_smp])
    if (pct_diff > 0.01):
        warnings.warn('The provided time traces have different time spacing; applying interpolation')

    if (min(t_ref) != min(t_smp)) or (max(t_ref) != max(t_smp)):
        warnings.warn('The provided time traces have different time ranges; applying padding')


    # generate new time scale
    t_lo = min(min(t_ref), min(t_smp))
    dt = min(dt_ref, dt_smp)
    t_hi = max(max(t_ref), max(t_smp))

    t = np.arange(t_lo, t_hi+dt, dt)

    # interpolate and pad 
    A_ref_padded = np.interp(t, t_ref, A_ref,
                             left = A_ref[0], right = A_ref[-1] )
    A_smp_padded = np.interp(t, t_smp, A_smp,
                             left = A_smp[0], right = A_smp[-1])

    # baseline subtract (to avoid jump after zero padding)
    A_ref_padded = A_ref_padded - A_ref_padded[-1]
    A_smp_padded = A_smp_padded - A_smp_padded[-1]
    
    return {'t': t, 'A_ref': A_ref_padded, 'A_smp': A_smp_padded}
    
    
def downsample(x_q, x, y):
    w = np.mean(np.diff(x))/2

    y_q = [np.mean(y[(x >= x_-w) & (x <= x_+w)]) for x_ in x_q]
    return np.asarray(y_q)

def faxis(t, n):
    dt = np.mean(np.diff(t))
    df = (1/dt)/n

    f = np.arange(0, n)*df
    return f
    
    
    
def transfer_function(t_smp, A_smp, t_ref, A_ref, freqs, zero_padding):
    padded = time_pad(t_smp, A_smp, t_ref, A_ref)
    
    spec_ref_full = np.fft.fft(padded['A_ref'], n = zero_padding)
    spec_smp_full = np.fft.fft(padded['A_smp'], n = zero_padding)

    f_full = faxis(padded['t'], zero_padding)

    spec_ref_ds = downsample(freqs, f_full, spec_ref_full)
    spec_smp_ds = downsample(freqs, f_full, spec_smp_full)

    return spec_smp_ds/spec_ref_ds
    
    
    
    
    
    

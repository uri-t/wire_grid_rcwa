# Installing the package

1. Clone the repository
2. Install dependencies with `pip install -r requirements.txt`

# Using the package

The general workflow for using the package to extract dielectric/electronic parameters is as follows:

1. Use `transfer_function` function to calculate the transfer function from the collected sample and reference THz pulses, e.g.:
```matlab
tf = wgr.transfer_function(t_smp, A_smp, t_ref, A_ref,
                               freqs = freq, zero_padding = 2**18)
```

2. Define sample and reference geometry, e.g.:

```matlab
 s_ref = wgr.Structure(ys = ys, nh = nh,
                          layers = [wgr.Slab(...),
                                    wgr.Wires(...)],
                          half_space_tr = wgr.HalfSpaceTr(...))
                      
    s_smp = wgr.Structure(ys = ys, nh = nh,
                          layers = [wgr.Slab(...),
                                    wgr.Wires(...)],
                          half_space_tr = wgr.HalfSpaceTr(...))
```


3. Perform data extraction:

```matlab
 extracted = wgr.Extractor.extract(s_ref, s_smp,
                                      fill_mat_on, freq, tf, 9.01 - 0.001*1j)
```



A full example can be found in `ds_test.py`

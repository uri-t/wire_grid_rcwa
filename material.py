import numpy as np
class Material:    
    def __init__(self, **kwargs):
        # check arguments
        # allow: static n, eps (or either + cond)
        # or frequency dependent if given freq with same length

        # assign permittivity, expanding static values if necessary
        self.freq = kwargs['freq']
        self.eps = kwargs['eps'] + 0*self.freq

        # add conductivity if present
        if 'cond' in kwargs:
            e0 = 8.854e-12; #F/m = (C/V)/m
            cond = kwargs['cond'] + 0*self.freq
            self.eps = self.eps - 1j*cond/(e0*2*np.pi*self.freq*1e12)
        

        if not np.all(np.diff(self.freq) > 0):
            raise ValueError("Frequency values must be increasing")

    def get_eps(self, freq):
        if freq > max(self.freq) or freq < min(self.freq):
            raise ValueError(
                "Requested permittivity for frequency outside of defined range")
        
        return np.interp(freq, self.freq, self.eps)
        
        
        

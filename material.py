import numpy as np
class Material:    
    def __init__(self, **kwargs):
        # check arguments
        # allow: static n, eps (or either + cond)
        # or frequency dependent if given freq with same length

        self.eps = kwargs['eps']
        self.freq = kwargs['freq']

        if not np.all(np.diff(self.freq) > 0):
            raise ValueError("Frequency values must be increasing")

    def get_eps(self, freq):
        if freq > max(self.freq) or freq < min(self.freq):
            raise ValueError(
                "Requested permittivity for frequency outside of defined range")
        
        return np.interp(freq, self.freq, self.eps)
        
        
        

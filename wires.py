import numpy as np
from .material import Material
from .layer import Layer

class Wires(Layer):
    def __init__(self, wire_mat, fill_mat, wire_fill_frac, period, d):
        
        self.wire_mat = wire_mat
        self.fill_mat = fill_mat
        self.wire_fill_frac = wire_fill_frac
        self.period = period
        self.d = d

    def eps(self, freq, ys):
        if max(ys) - min(ys) != self.period:
            raise ValueError(
                'The given y values are not compatible with the wire period')


        eps_ret = [self.fill_mat.get_eps(freq) for x in ys]

        wire_lo = (self.period/2.0)*self.wire_fill_frac
        wire_hi = self.period - wire_lo
        
        for i in range(0, len(ys)):
            if (ys[i] < wire_lo) | (ys[i] > wire_hi):
                eps_ret[i] = self.wire_mat.get_eps(freq)

        return eps_ret
            
        

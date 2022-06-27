import numpy as np
from .material import Material
from .layer import Layer

class Slab(Layer):
    def __init__(self, material, d):
        self.d = d
        self.material = material
        
    def eps(self, freq, ys):
        return [self.material.get_eps(freq) for y in ys]

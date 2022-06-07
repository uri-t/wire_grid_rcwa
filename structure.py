from layer import Layer
from S_mats import S_mats

class Structure:
    def __init__(ys = ys, nh = nh, layers = layers, t_mat = t_mat):
        self.ys = ys
        self.nh = nh
        self.layers = layers
        self.t_mat = t_mat

    def tf(freq):
        s_mat = t_mat
        layer_s_mats = [x.S_mats(freq, self.ys, self.nh) for x in layers] 
        [s_mat := S_mats.star(x., s_mat) for x in reverse(layer_smats)]

        ind = (nh-1)/2 + 1 
        return s_mat(ind, ind)
        
        



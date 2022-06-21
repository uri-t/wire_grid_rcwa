from layer import Layer
from S_mats import S_mats

class Structure:
    def __init__(self, ys, nh, layers):
        self.ys = ys
        self.nh = nh
        self.layers = layers

    def tf(self, freq):
        ys = self.ys
        nh = self.nh
        s_mat = self.layers[-1].S_mats(freq, ys, nh)
        
        layer_s_mats = [x.S_mats(freq, ys, nh) for x in self.layers[0:-1]] 
        [s_mat := S_mats.star(x, s_mat) for x in reversed(layer_s_mats)]

        ind = int((nh-1)/2)

        return s_mat.S12[ind, ind]
                    
    def trial_tf(self, mat, freq, eps):
        # store mat's get_eps function
        get_eps_store = mat.get_eps

        # overwrite get_eps function
        mat.get_eps = lambda x: eps

        # calculate transfer function
        tf_ret = self.tf(freq)

        # restore get_eps function
        mat.get_eps = get_eps_store

        return tf_ret

from scipy.optimize import minimize
import numpy as np

class Extractor:
    def cost(tf1, tf2):
        chi1 = (np.log(np.abs(tf1)) - np.log(np.abs(tf2)))**2
        dphi = np.angle(tf1) - np.angle(tf2)
        chi2 = (np.mod(dphi + np.pi, 2*np.pi)-np.pi)**2
        return chi1 + chi2

    def extract(struct_ref, struct_smp, mat, freq, tf, start):
        eps_extract = np.zeros(len(freq), dtype = complex)
        print(len(eps_extract))
        
        curr_eps = [np.real(start), np.imag(start)]
        
        for i in range(0, len(freq)):
            smp_tf = lambda eps: struct_smp.trial_tf(mat, freq[i], eps[0] + 1j*eps[1])
            ref_tf = lambda eps: struct_ref.trial_tf(mat, freq[i], eps[0] + 1j*eps[1])
            
            err = lambda eps: Extractor.cost(smp_tf(eps)/ref_tf(eps),tf[i])

            opt = minimize(err, curr_eps, method = 'nelder-mead').x
            eps_extract[i] = opt[0] + 1j*opt[1]

            print(opt)
            curr_eps = opt

        print(len(eps_extract))
        return eps_extract

            
                                                             

from .material import Material
from .S_mats import S_mats
import numpy as np

class HalfSpaceTr:
    def __init__(self, mat):
        self.mat = mat

    def S_mats(self, freq, ys, nh):
        c = 3e14     # speed of light (um/s)
        k0 = 2*np.pi*freq*1e12/c

        eps = self.mat.get_eps(freq)
        mu = 1
        
        L = max(ys) - min(ys)
        ks = (1/k0)*2*np.pi*np.arange(-(nh-1)/2, (nh-1)/2 + 1)/L
        K = np.diag(ks).astype(complex)

        omega_0 = K@K-np.eye(nh)
        W_0 = np.eye(nh)
        V_0 = np.diag(-1/np.sqrt(np.diag(omega_0)))

        omega_t = K@K - eps*mu*np.eye(nh)
        W_t = np.eye(nh)
        V_t = np.diag(-mu*eps/np.sqrt(np.diag(omega_t)))

        A = np.linalg.inv(W_0)@W_t + np.linalg.inv(V_0)@V_t
        B = np.linalg.inv(W_0)@W_t - np.linalg.inv(V_0)@V_t

        S11 = B@np.linalg.inv(A)
        S12 = 0.5*(A - B@np.linalg.inv(A)@B)
        S21 = 2*np.linalg.inv(A)
        S22 = -np.linalg.inv(A)@B

        return S_mats(S11 = S11, S12 = S12, S21 = S21, S22 = S22)
    

        

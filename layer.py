import numpy as np
from .S_mats import S_mats

class Layer:
    def __init__(self, d, eps):
        self.d = d
        self.eps = eps

    def S_mats(self, freq, ys, nh):
        c = 3e14   # speed of light (um/s)
        k0 = 2*np.pi*freq*1e12/c; #rad/um
        mu = 1;    # assume uniform susceptibility = 1

        eps = self.eps(freq, ys)
        d = self.d
        
        if nh > len(eps):
            raise ValueError(
                'Permittivity vector have at least as many entries as number of harmonics')

        if np.mod(nh, 2) == 0:
            raise ValueError('The number of harmonics must be odd')

        # construct convolution matrix for permittivity
        full_spec = np.fft.fftshift(np.fft.fft(eps))/len(eps)
        Ek = np.zeros((nh, nh)).astype(complex)

        for i in range(0, nh):
            mid = np.floor(len(eps)/2)
            inds = list(np.arange(0, -nh, -1) + i + mid)
            inds = [int(x) for x in inds]
            Ek[i,:] = full_spec[inds]

        # construct wave vector array
        dy = ys[1] - ys[0]

        if max(np.diff(np.diff(ys))) > 1e10:
            raise ValueError('Y spacing for permittivity must be even')

        L = max(ys) - min(ys)
        ks = (1/k0)*2*np.pi*np.arange(-(nh-1)/2, (nh-1)/2 + 1)/L

        K = np.diag(ks).astype(complex)

        # construct full propagation matrix
        omega_sq = K@np.linalg.inv(Ek)@K@Ek - mu*Ek
        Q_mat = -Ek

        # calculate scattering matrices for vacuum (gap layer)
        omega_0 = K@K-np.eye(nh)
        W_0 = np.eye(nh)
        V_0 = np.diag(-1/np.sqrt(np.diag(omega_0)))

        # calculate eigenvalues, eigenvectors
        (lambda_2, W) = np.linalg.eig(omega_sq)
        lambda_sq = np.diag(lambda_2)

        # set small imaginary components of eigenvalues to 0 for stability
        lambda_sq_im = np.imag(lambda_sq)
        lambda_sq_im[lambda_sq_im < 1e-10] = 0
        lambda_sq = np.real(lambda_sq) + 1j*lambda_sq_im
        lamb = np.lib.scimath.sqrt(np.diag(lambda_sq))

        # calculate matrices
        V = Q_mat@W@np.linalg.inv(np.diag(lamb))
        A = np.linalg.inv(W)@W_0 + np.linalg.inv(V)@V_0
        A_inv = np.linalg.inv(A)
        B = np.linalg.inv(W)@W_0 - np.linalg.inv(V)@V_0
        X = np.diag(np.exp(-lamb*d*k0))



        
        # generate scattering matricies
        S11 = np.linalg.inv(A - X@B@A_inv@X@B)@(X@B@A_inv@X@A - B)
        S21 = np.linalg.inv(A - X@B@A_inv@X@B)@X@(A - B@A_inv@B)
        S12 = S21
        S22 = S11

        return S_mats(S11 = S11, S12 = S12, S21 = S21, S22 = S22)
        

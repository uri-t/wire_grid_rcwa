function [smats, K] = layer_mats(ys, eps, d, freq)

% constants
k0 = 2*pi*freq*1e12/(3e8*1e6); % rad/um
mu = 1;
c = 3e14; % speed of light, micrometers per second
p = @(freq, d, n) exp(-1i*(2*pi*freq*1e12/c).*n*d);

% construct convolution matrix for permittivity
nh = 25;
full_spec = fftshift(fft(eps))/numel(eps);
Ek = zeros(nh, nh);

for ii = 1:nh
    n = floor(nh/2);
    middle = floor(numel(eps)/2)+1;
    
    inds = [0:-1:-2*n] + (ii-1) + middle;
    Ek(ii, :) = full_spec(inds);
end

% wave vectors corresponding to fourier components
assert(sum(diff(diff(ys))) < 1e-10, 'must have even spacing in input permittivity')

% construct vector of wave vectors corresponding to fourier coefficients
dy = ys(2)-ys(1);
N = nh;

assert(mod(N,2) ~= 0, 'The number of Fourier components (given by size of eps vector) must be odd')
L = max(ys)-min(ys);
ks = (1/k0)*2*pi*[-(N-1)/2:(N-1)/2]*1/L;
K = diag(ks);


% construct full propagation matrix
omega_sq = K*inv(Ek)*K*Ek - mu*Ek;
P_mat = K*inv(Ek)*K - mu*eye(size(Ek));
Q_mat = -Ek;

% calculate scattering matrices for vacuum (gap layer)
omega_0 = K*K-eye(size(Ek));
W_0 = eye(size(Ek));
V_0 = diag(-1./sqrt(diag(omega_0)));

% calculate eigenvalues, eigenvecs
[W, lambda_2] = eig(omega_sq);

lambda_sq = diag(lambda_2);

% set small imaginary parts to 0 for stability
lambda_sq_im = imag(lambda_sq);
lambda_sq_im(abs(lambda_sq_im) < 1e-10) = 0;
lambda_sq = real(lambda_sq) + 1i*lambda_sq_im;
lambda = sqrt(lambda_sq);

s_in = zeros(N,1);
s_in((N-1)/2 + 1) = 1;

V = Q_mat*W*inv(diag(lambda));
A = inv(W)*W_0 + inv(V)*V_0;
B = inv(W)*W_0 - inv(V)*V_0;
X = diag(exp(-lambda*d*k0));

smats.S11 = inv(A - X*B*inv(A)*X*B)*(X*B*inv(A)*X*A - B);
smats.S21 = inv(A - X*B*inv(A)*X*B)*X*(A - B*inv(A)*B);
smats.S12 = smats.S21;
smats.S22 = smats.S11;

% keyboard

% convolution matrix for refractive index
function [cmat] = ref_conv(n)
    n_spec = fftshift(fft(n))/numel(n);
    
    cmat = zeros(nh, nh);
    
    for ii = 1:nh
        num_terms = floor(nh/2);
        middle = floor(numel(n)/2)+1;
        
        inds = [0:-1:-2*num_terms] + (ii-1) + middle;
        cmat(ii, :) = n_spec(inds);
    end
end
end
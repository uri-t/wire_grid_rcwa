function [smats] = trn_mats(eps, mu, K)
% generate transmission scattering matrices for uniform media

% gap medium (vacuum) matrices
omega_0 = K*K-eye(size(K));
W_0 = eye(size(K));
V_0 = diag(-1./sqrt(diag(omega_0)));

% transmission medium matrices
omega_t = K*K-eps*mu*eye(size(K));
W_t = eye(size(K));
V_t = diag(-mu*eps./sqrt(diag(omega_t)));


A = inv(W_0)*W_t + inv(V_0)*V_t;
B = inv(W_0)*W_t - inv(V_0)*V_t;

smats.S11 = B*inv(A);
smats.S12 = 0.5*(A-B*inv(A)*B);
smats.S21 = 2*inv(A);
smats.S22 = -inv(A)*B;

% keyboard
end
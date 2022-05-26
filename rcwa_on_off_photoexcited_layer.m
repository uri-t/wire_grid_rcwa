function [tf] = rcwa_on_off_photoexcited_layer(freq, eps_off, eps_on, eps_wires, eps_subs, f, d_wires, d_smp, period, N)

ys = period*[0:1/(N-1):1];

a_lo = (period/2)*(1-f);
a_hi = (period/2)*(1+f);


% eps_wires_on
eps_full_on = repmat(eps_wires, [numel(ys), 1]);
eps_full_on(ys <= a_lo | ys >= a_hi) = eps_on;

% eps_off
eps_full_off = repmat(eps_wires, [numel(ys), 1]);
eps_full_off(ys <= a_lo | ys >= a_hi) = eps_off;

% layer past wires
eps_on_layer = repmat(eps_on, [numel(ys), 1]);
eps_off_layer = repmat(eps_off, [numel(ys), 1]);

[S_wire_on, ~] = layer_mats(ys, eps_full_on, d_wires, freq);
[S_wire_off, K] = layer_mats(ys, eps_full_off, d_wires, freq);
[S_layer_on, K] = layer_mats(ys, eps_on_layer, d_smp - d_wires, freq);
[S_layer_off, K] = layer_mats(ys, eps_off_layer, d_smp - d_wires, freq);


S_trn = trn_mats(eps_subs, 1, K);

S_on = star(S_layer_on, star(S_wire_on, S_trn));
S_off = star(S_layer_off, star(S_wire_off, S_trn));

nh = size(K,1);

s_in = zeros(nh,1);
s_in((nh-1)/2 + 1) = 1;

s_out_on = S_on.S21*s_in;
s_out_off = S_off.S21*s_in;

mid = (nh-1)/2 + 1;

tf = (s_out_on(mid)/s_out_off(mid));
end
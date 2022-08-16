path = '/home/uri/Desktop/grad/wire_grid_rcwa/';
d_sim_re = importdata(fullfile(path, 'eps_re_sim.txt'));
d_sim_re = d_sim_re.data;

d_sim_im = importdata(fullfile(path, 'eps_im_sim.txt'));
d_sim_im = d_sim_im.data;

d_on = importdata(fullfile('ds_test_on.txt'));
d_on = d_on.data;

d_off = importdata(fullfile(path,'ds_test_off.txt'));
d_off = d_off.data;

t_ref = d_off(:,1);
A_ref = d_off(:,2);

inds = t_ref <= 13;
A_ref = A_ref(inds);
t_ref = t_ref(inds);

t_smp = d_on(:,1);
A_smp = d_on(:,2);

inds = t_smp <= 13;
A_smp = A_smp(inds);
t_smp = t_smp(inds);

inp = fullfile(path, 'layer_test_input.json');

[freq, tf, ~, ~, spec_smp, spec_ref] = exp_tf(t_smp, A_smp, t_ref, A_ref, load_input(inp));

ea = 9; eb = 16; sigb = 1e5; f = 0.2; period = 10; d = 0.5;

e0 = 8.854e-12; %F/m = (C/V)/m
eb_full = eb - sigb*1i./(e0*freq*1e12*2*pi);

[eps_on] = extract_eps_on_off(tf, freq, ea, eb_full, 3.8025, f, d, period, 256);

cond = n_to_photocond(freq, sqrt(eps_on), sqrt(ea));


function [freq, cond_archive_wires] = wires_process(fname_on, fname_off, d_smp, d_wires)
d_on = importdata(fname_on);
on_data = d_on(:,2:end);

d_off = importdata(fname_off);

t_ref = d_off(:,1);
A_ref = d_off(:,2);

t_smp = d_on(:,1);
% A_smp = d_on(:,2) + d_off(:,2);


inp = '/home/uri/Desktop/grad/wire_grid_rcwa/experiments/s00124_inp.json';

[freq, ~, ~, ~, ~, ~] = exp_tf(t_smp, A_ref, t_ref, A_ref, load_input(inp));

eps_off = 36; eb = 1; sigb = 1.5e5; f = 1/3; period = 12; 
% d_wires = 0.25; d_smp = 0.86; 

e0 = 8.854e-12; %F/m = (C/V)/m
eps_wires = eb - sigb*1i./(e0*freq*1e12*2*pi);
eps_subs = 1.95^2;

N = 256;

cond_archive_wires = [];

for ii = 1:200
    [~, r]  = sort(rand(1,68));
    inds = r < 7;

    d_on = mean(on_data(:,inds), 2);
    [freq, tf, ~, ~, spec_smp, spec_ref] = exp_tf(t_smp, A_ref + d_on, t_ref, A_ref, load_input(inp));
    
    [eps_on] =  extract_eps_on_off_photoexcited_layer(tf, freq, ...
        eps_off, eps_wires, eps_subs, f, d_wires, d_smp, period, N);
    
    cond = n_to_photocond(freq, sqrt(eps_on), sqrt(eps_off));
    
    figure(2)
    plot(freq, -real(cond), 'k')
    hold on
    plot(freq, imag(cond), 'k--')
    title(ii)
    drawnow
    
    cond_archive_wires = [cond_archive_wires; cond];
end


figure(3)
mean_re = -mean(real(cond_archive_wires));
mean_im = mean(imag(cond_archive_wires));

std_re = std(real(cond_archive_wires));
std_im = std(imag(cond_archive_wires));

fill([freq fliplr(freq)], [mean_re - 2*std_re fliplr(mean_re + 2*std_re)], 'b',...
    'FaceAlpha', 0.2, 'edgecolor', 'none')
hold on
plot(freq, mean_re, 'b', 'linewidth', 1.1)

fill([freq fliplr(freq)], [mean_im - 2*std_im fliplr(mean_im + 2*std_im)], 'b',...
    'FaceAlpha', 0.2, 'edgecolor', 'none')
plot(freq, mean_im, 'b--', 'linewidth', 1.1)
end

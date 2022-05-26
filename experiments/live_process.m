function [freq, cond_archive] = live_process(ref_name, smp_name, d)

inp = 'C:\Users\utayv\OneDrive\Desktop\grad\research\wires_writeup\experiments\s00124_inp.json';


n_smp =50;

cond_archive = [];

for ii = 1:n_smp
d_ref = importdata(ref_name);
d_smp = importdata(smp_name);

smp_data = d_smp(:,2:end);

[~, r]  = sort(rand(1,68));
inds = r < 7;

d_on = mean(smp_data(:,inds), 2);

inp = load_input(inp);

inp.sample(3).d = d;
inp.reference(3).d = d;

[freq, n_fit]...
    = nelly_main(inp, d_smp(:,1), d_on+d_ref(:,2),...
    d_ref(:,1), d_ref(:,2));
cond = n_to_photocond(freq, n_fit, 6);

figure(4)
plot(freq, real(cond), 'k')
hold on
plot(freq, imag(cond), 'k--')
drawnow
    
cond_archive = [cond_archive; cond];
end

figure(3)
mean_re = mean(real(cond_archive));
mean_im = mean(imag(cond_archive));

std_re = std(real(cond_archive));
std_im = std(imag(cond_archive));

fill([freq fliplr(freq)], [mean_re - 2*std_re fliplr(mean_re + 2*std_re)], 'r',...
    'FaceAlpha', 0.2, 'edgecolor', 'none')
hold on
plot(freq, mean_re, 'r', 'linewidth', 1.1)

fill([freq fliplr(freq)], [mean_im - 2*std_im fliplr(mean_im + 2*std_im)], 'r',...
    'FaceAlpha', 0.2, 'edgecolor', 'none')
plot(freq, mean_im, 'r--', 'linewidth', 1.1)
end
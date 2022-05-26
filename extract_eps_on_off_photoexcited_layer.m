function [eps_on] = ...
    extract_eps_on_off_photoexcited_layer(tf, freq, eps_off, eps_wires, eps_subs, f, d_wires, d_smp, period, N)

eps_on = zeros(size(freq));

eps_start = [36, -0.001];

for ii = 1:numel(freq)
    err = @(eps) n_error(tf(ii),...
                  rcwa_on_off_photoexcited_layer(freq(ii), eps_off, eps(1)+1i*eps(2), eps_wires(ii), eps_subs,...
                  f, d_wires, d_smp, period, N));
    opt = fminsearch(err, eps_start);
    eps_on(ii) = opt(1) + 1i*opt(2);
    
    figure(1)
    subplot(2,1,1)
    plot(freq(ii), opt(1), '.k')
    hold on
    
    subplot(2,1,2)
    plot(freq(ii), opt(2), '.k')
    hold on
    drawnow
    eps_start = opt
end


    function [chi] = n_error(t1, t2)
        chi1 = (log(abs(t1)) - log(abs(t2)))^2;
        dphi = angle(t1) - angle(t2);
        chi2 = (mod(dphi + pi, 2*pi) - pi)^2;
        chi = chi1+chi2;
    end
end
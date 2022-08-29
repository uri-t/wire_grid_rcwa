library(ggplot2)
d <- read.csv('/home/uri/Desktop/grad/wire_grid_rcwa/overetch/overetch_sim_results.csv')

ggplot(d) +
  geom_line(aes(freq, cond_re, col = d_rot, 
                 group = d_rot)) + 
  geom_line(aes(freq, cond_im, col = d_rot, 
                group = d_rot), linetype = 'dashed') + 
  ggtitle('Extracted conductivity vs. overetch angle') + 
  labs(x = 'Frequency (THz)', y = 'Conductivity (S/m)', col = "Overetch angle")
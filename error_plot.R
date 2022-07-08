
library(ggplot2)
d <- read.csv('/home/uri/Desktop/grad/wire_grid_rcwa/extraction_data.txt')

inds <- (d$freq > 0.2) & (d$f > 0.1) & 
  (d$path == "/home/uri/Desktop/grad/wire_grid_rcwa/simulation_data/wires_on_off_w_photoexcited_layer_results/70")

d <- d[inds,]
d$period <- as.factor(d$period)

p_re <- ggplot(d, aes(freq, pct_re, col = nh, 
                      group = interaction(nh, period), linetype = period)) + 
  geom_line()  + labs(x = 'Frequency (THz)', 
                      y = 'Error (%)', 
                      col = "Harmonics",
                      linetype = expression(paste("Period (", mu, "m)"))) + 
  ggtitle('Error in real part of conductivity')

p_im <- ggplot(d, aes(freq, pct_im, col = nh, 
                      group = interaction(nh, period), linetype = period)) + 
  geom_line()  + labs(x = 'Frequency (THz)', 
                      y = 'Error (%)', 
                      col = "Harmonics",
                      linetype = expression(paste("Period (", mu, "m)"))) + 
  ggtitle('Error in imaginary part of conductivity')

p_re <- p_re + facet_grid(sigb ~ f) + 
  scale_y_continuous(sec.axis = sec_axis(~ . , name = "Conductivity (S/m)", breaks = NULL, labels = NULL)) +
  scale_x_continuous(sec.axis = sec_axis(~ . , name = "Wire fill fraction", breaks = NULL, labels = NULL))

p_im <- p_im + facet_grid(sigb ~ f) + 
  scale_y_continuous(sec.axis = sec_axis(~ . , name = "Conductivity (S/m)", breaks = NULL, labels = NULL)) +
  scale_x_continuous(sec.axis = sec_axis(~ . , name = "Wire fill fraction", breaks = NULL, labels = NULL))


ggsave(file="error_plot_re.png", plot = p_re,  width=7, height=4, dpi=300)
ggsave(file="error_plot_im.png", plot = p_im,  width=7, height=4, dpi=300)





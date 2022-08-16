library(ggplot2)

df <- read.csv('Desktop/grad/wire_grid_rcwa/np_effective_medium.csv')

df <- df[df$np_size == 0.05,]

plt <- ggplot(df)  + 
  geom_line(aes(x = freq, y = cond_re, group = interaction(grid, wires), 
                col = wires, alpha = grid))  + 
  geom_line(aes(x = freq, y = cond_im, group = interaction(grid, wires), 
                col = wires, alpha = grid), linetype = 2) +
  labs(x = 'Frequency (THz)', 
       y = 'Conductivity (S/m)', 
       col = "Wires",
       alpha = "Cells per wavelength") 


ggsave(file="np_effective_medium.png", plot = plt,  width=5, height=4, dpi=300)


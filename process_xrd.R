
library(rjags)
library(ggplot2)
process_xrd <- function(fname, peaks, range, n_smps){
  data <- read.csv(fname)
  
  y <- data$yobs - data$bkg
  th <- data$X.twotheta
  
  inds <- (th > range[1]) & (th < range[2])
  y <- y[inds]
  th <- th[inds]

  print(y)
  model <- "

  model{ 
    
    for (i in 1:length(peaks)){
      p[i] ~ dunif(peaks[i]-tol, peaks[i] + tol)
    }
    
    for (i in 1:length(peaks)){
      sig[i] ~ dexp(10)
      a[i] ~ dnorm(3000, 1e-5)
    }
    
    
    for (i in 1:length(peaks)){
      for (j in 1:length(th)){
        # gaussians[i,j] <- a[i]*exp(-(th[j] - p[i])^2/(2*sig[i]^2))
        gaussians[i,j] <- a[i]/(1 + ((th[j] - p[i])/sig[i])^2)
      }
    }
    
    
    
    sig_data ~ dexp(0.1)
    
    for (i in 1:length(y)){
      y_fit[i] <- sum(gaussians[1:length(p),i])
      y[i] ~ dnorm(y_fit[i], 1/(sig_data)^2)
    }
  }
"
  
  m1 <- jags.model(textConnection(model), 
                   data=list(peaks = peaks,
                             tol = 0.1,
                             th = th,
                             y = y)
  )
  
  update(m1,n_smps)
  cs <- coda.samples(m1, c('sig', 'y_fit', 'p', 'a'), n_smps)
  smps <- as.data.frame(x=cs[[1]])
  
  fits <- as.matrix(smps[grepl('y_fit', names(smps))])
  sigs <- as.matrix(smps[grepl('sig', names(smps))])
  ps <- as.matrix(smps[grepl('p', names(smps))])
  as <- as.matrix(smps[grepl('a', names(smps))])
  
  return(list(fits = fits,
              sigs = sigs, 
              ps = ps, 
              th = th, 
              y=y,
              as = as))
}


plot_smps <- function(smps){
  plot(smps$th, smps$y, xlab= expression(paste(2, theta, ' (deg)')),
       ylab = 'I (cps)')
  err_lo = sapply(1:dim(smps$fits)[2], function(i) {
    quantile(smps$fits[,i], 0.025)})
  
  err_hi = sapply(1:dim(smps$fits)[2], function(i) {
    quantile(smps$fits[,i], 0.975)})
  
  lines(smps$th, err_lo)
  lines(smps$th, err_hi)
}

add_to_df <- function(df, smp_name, smps){
 for (i in 1:dim(smps$sigs)[2]){
   for (j in 1:dim(smps$sigs)[1]) {
     df[nrow(df) + 1,]  <- c(smp = smp_name,
                             pk_no = i,
                             w = smps$sigs[j,i],
                             pos = smps$ps[j,i],
                             a = smps$as[j,i])
   }
 }
  
  df$pk_no <- as.numeric(df$pk_no)
  df$w <- as.numeric(df$w)
  df$pos <- as.numeric(df$pos)
  df$a <- as.numeric(df$a)
  
  return(df)
}

smps = c('124', '125', '128', '129', '131', '132')

d <- data.frame(smp = character(), 
                pk_no = numeric(),
                w = numeric(),
                pos = numeric(),
                a = numeric())

for (smp in smps){
  path <- '/home/uri/Desktop/grad/wire_grid_rcwa/experimental_data/220722'
  fname <- paste0(path, '/s00', smp, '.csv')
  
  smps <- process_xrd(fname, c(23.12, 23.6, 24.4), c(22.5, 25.0), 1000)
  plot_smps(smps)
  

  d <- add_to_df(d, smp, smps)
}

d$wires <- d$smp %in% c('132', '131', '128')
ggplot(data = d, aes(y = pos, x = smp, edge = smp, fill = wires)) + geom_violin() +
  facet_wrap(~pk_no, scales = "free")

ggplot(data = d, aes(y = w, x = smp, edge = smp, fill = wires)) + geom_violin() +
  facet_wrap(~pk_no)


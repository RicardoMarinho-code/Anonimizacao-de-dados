# Instala o sdcApp
if (!requireNamespace("remotes", quietly = TRUE)) install.packages("remotes")
remotes::install_github("sdcTools/sdcApp")

library(sdcApp)
runApp()
# install.packages("devtools", dependencies = TRUE, INSTALL_opts = '--no-lock')
# install.packages("rjson")
# library(devtools)

# if("devtools" %in% rownames(installed.packages()) == FALSE) {
#     install.packages("devtools", dependencies = TRUE, INSTALL_opts = '--no-lock')
# }
# library("devtools")
#if("SPEI" %in% rownames(installed.packages()) == FALSE) {
#    install.packages('SPEI', dependencies = TRUE, INSTALL_opts = '--no-lock')
#}
library("SPEI")
#if("rjson" %in% rownames(installed.packages()) == FALSE) {
#    install.packages("rjson", dependencies = TRUE, INSTALL_opts = '--no-lock')
#}
library("rjson")

args <- commandArgs(trailingOnly = TRUE)
name <- args[1]
lat <- as.numeric(args[2])

rcp <- c("rcp26", "rcp45", "rcp85")
years <- c(2050, 2100)
speiData <- data.frame(matrix(ncol = 7, nrow = 60))
colnames(speiData) <- c("date", paste0("rcp26", "_", years), paste0("rcp45", "_", years), paste0("rcp85", "_", years))
speiData["date"] <- format(seq(as.Date("2046-01-01"), as.Date("2050-12-01"), "month"), "%Y-%m")

# Calculate potential evapotranspiration using penman for a combined time frame 
# between 2046 - 2050 and 2096 - 2100
for(r in rcp) {
    for(year in years) {
        data <- fromJSON(file = file.path("./portfolio/climate_risk_dash/data/temp", paste0(name, "_", r, "_", year, ".json")))
        pen <- penman(Tmin = data$tasmin, Tmax = data$tasmax, U2 = data$sfcWind, lat = lat, Rs = data$rsds, RH = data$hurs, P = data$ps)
        p <- data$pr - pen
        speiData[paste0(r, "_", year)] <- spei(p, 12)$fitted
        print(year)
    }
}
write.csv(speiData, file = file.path("./portfolio/climate_risk_dash/report", paste0(name, "_speiData.csv")))

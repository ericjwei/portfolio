# install.packages("devtools", dependencies = TRUE, INSTALL_opts = '--no-lock')
# install_github('sbegueria/SPEI')
# install.packages("rjson")
# library(devtools)
library(SPEI)
library(rjson)
args <- commandArgs(trailingOnly = TRUE)
lat <- as.numeric(args[1])
z <- as.numeric(args[2])
name <- args[3]
files <- c("26_2050", "26_2100", "45_2050", "45_2100", "85_2050", "85_2100")
speiData <- data.frame(matrix(ncol = 6, nrow = 12))
colnames(speiData) <- files
rownames(speiData) <- c("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
for(f in files) {
    data <- fromJSON(file = paste0("./data/output", f, ".json"))
    pen <- penman(Tmin = data$tasmin, Tmax = data$tasmax, U2 = data$sfcWind, lat = lat, Rs = data$rsds, RH = data$hurs, P = data$ps, z = z)
    p <- data$pr - pen
    speiData[f] <- tail(spei(p, 12)$fitted, 12)
}
write.csv(speiData, file = paste0("./data/", name, "_speiData.csv"))

# colnames(speiData) <- files
# names(speiData)
# speiData
# # getData <- function(f) {
# #     return(fromJSON(file = c("./data/output", f, ".json")))
# # }

# # data26_2050 <- fromJSON(file = "output26_2050.json")
# # data85_2050 <- fromJSON(file = "output85_2050.json")

# # Using the penman with the use of more variables
# # Tave - temperature in C -> 2m temperature K
# # lat - in degrees -> latpt
# # Tmax - max temp C -> Maximum 2m temperature K
# # Tmin - min temp C -> Minimum 2m temperature K
#     # -273.15
# # Pre - precipitation mm -> Mean precipitation flux kg/m^2s
#     # precipitation flux * 2.628e+6 = mm/month
# # U2 - Wind speeds 2m height m/s -> 10m wind_speed m/s
# # RS - Solar radiation MJ/m^2d -> Surface solar radiation downwards W/m^2
# # CC - Could cover % -> Total cloud cover %
# # RH - Relative humidity % -> Near surface relative humidity %
# # P atmospheric pressure at surface kPa -> Surface pressure Pa
#     # /1000

# # data(wichita)
# # wichita$PET <- thornthwaite(wichita$TMED, 37.6475)
# # # wichita$PET <- penman(TMIN, TMAX, AWND, CC = ACSH, lat=37.6475, z=402.6, na.rm=TRUE)
# # wichita$BAL <- wichita$PRCP - wichita$PET
# # print(wichita$BAL)
# # spei1 <- spei(wichita[, 'BAL'], 1)
# # spei2 <- spei(wichita[, 'BAL'], 12)
# # summary(spei1)
# # attach(wichita)
# # names(wichita)
# # pen <- penman(TMIN, TMAX, AWND, CC = ACSH, lat=37.6475, z=402.6, na.rm=TRUE)
# # print(pen)
# TMIN <- c(-3.3, -3.4)
# print(TMIN)
# t <- penman(Tmin = c(-3.3, -3.4), Tmax = c(1.4, 1.3), U2 = c(3.75, 3.3), lat = 39.95, Rs = c(6.29, 11), RH = c(77.69, 75), P = c(98.53, 98.65), z =7)
# # t <- penman(Tmin=-3.3, Tmax=1.4, U2=3.75, lat=39.95, z=402.6)

# t1 <- penman(Tmin = data26$tasmin, Tmax = data26$tasmax, U2 = data26$sfcWind, lat = 39.95, Rs = data26$rsds, RH = data26$hurs, P = data26$ps, z = 7)
# s1 <- data26$pr - t1

# t2 <- penman(Tmin = data85$tasmin, Tmax = data85$tasmax, U2 = data85$sfcWind, lat = 39.95, Rs = data85$rsds, RH = data85$hurs, P = data85$ps, z = 7)
# s2 <- data85$pr - t2

# spei1 <- spei(s1, 12)
# spei2 <- spei(s2, 12) 

# print(mean(spei1$fitted[37:60]))
# print(mean(spei2$fitted[37:60]))

# summary(spei1)
# summary(spei2)


# print(s)
# summary(spei1)
# spei2 <- spei(wichita[0:48,'BAL'], 1)
# summary(spei2)

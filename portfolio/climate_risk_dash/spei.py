from netCDF4 import Dataset
# from datetime import datetime, timedelta
from numpy import argmin
from json import dump
# from csv import writer
from typing import Any
from subprocess import call
from flask import Flask

from speiData import SpeiDataset
 
# Get index for closest lat and lon using first dataset
def getLatLon(testData: Any, lat: float, lon: float) -> (int, int):
    i_lat = abs(testData.variables['lat'][:] - lat).argmin()
    i_lon = abs(testData.variables['lon'][:] - lon).argmin()
    return([i_lat, i_lon])

# Compiles the CMIP5 predictions for a specific location for each environmental variable speiData.
# Requires date range and location (latitude, longitude)
# data: dictionary of NetCDF4 variable key to dataset
# i_dateStart: index start month after starting month in dataset
# i_dateEnd: index end month after starting month in dataset
# latpt: latitude of location in decimal 
# lonpt: longitude of location in 360 decimal 
def CMIP5monthly(data: dict, i_dateStart: int, i_dateEnd: int, 
                    i_lat: int, i_lon: int) -> dict:
    dataMonthly = {}
    for v in data: 
        d = data[v]
        monthly = [None] * (i_dateEnd - i_dateStart)
        for m in range(i_dateStart, i_dateEnd):
            var = d.variables[v]
            # i_lat = abs(d.variables['lat'][:] - latpt).argmin()
            # i_lon = abs(d.variables['lon'][:] - lonpt).argmin()    
            monthly[m - i_dateStart] = float(var[m, i_lat, i_lon])
        dataMonthly[v] = monthly
    return dataMonthly

# Change units to conform with SPEI formula
def conversion(dataMonthly: dict) -> None:
    dataMonthly['tas'] = [i - 273.15 for i in dataMonthly['tas']]
    dataMonthly['tasmax'] = [i - 273.15 for i in dataMonthly['tasmax']]
    dataMonthly['tasmin'] = [i - 273.15 for i in dataMonthly['tasmin']]
    dataMonthly['pr'] = [i * 2.628e+6 for i in dataMonthly['pr']]
    dataMonthly['rsds'] = [i * 0.0864 for i in dataMonthly['rsds']]
    dataMonthly['ps'] = [i / 1000 for i in dataMonthly['ps']]

# Get current SPEI 12 month from SPEI Database
def currentSpei(currentData: Any, lat: float, lon: float) -> float:
    i_lat = abs(currentData.variables['lat'][:] - lat).argmin()
    i_lon = abs(currentData.variables['lon'][:] - lon).argmin()    
    return currentData.variables['spei'][-1, i_lat, i_lon]

def main(name, lat, lon, z):
    currentData = Dataset("./data/spei12.nc", mode = 'r')
    spei = currentSpei(currentData, lat, lon)
    currentData.close()
    speiData = SpeiDataset()
    speiData.getData()

    # Get index for closest lat and lon 
    i_lat, i_lon = getLatLon(speiData.data26_2050[next(iter(speiData.data26_2050))], lat, lon % 360)

    # Filter for POI
    data = {
        "26_2050": CMIP5monthly(speiData.data26_2050, 0, 60, i_lat, i_lon),
        "26_2050": CMIP5monthly(speiData.data26_2050, 0, 60, i_lat, i_lon),
        "26_2100": CMIP5monthly(speiData.data26_2100, 0, 60, i_lat, i_lon),
        "45_2050": CMIP5monthly(speiData.data45_2050, 0, 60, i_lat, i_lon),
        "45_2100": CMIP5monthly(speiData.data45_2100, 0, 60, i_lat, i_lon), 
        "85_2050": CMIP5monthly(speiData.data85_2050, 0, 60, i_lat, i_lon),
        "85_2100": CMIP5monthly(speiData.data85_2100, 0, 60, i_lat, i_lon)
    }

    # Convert units
    for d in data:
        conversion(data[d])

    # Output data to json for spei.r calculation
    for d in data:
        with open('./data/output' + d + '.json', 'w')as fp:
            dump(data[d], fp)
    speiData.closeData()

    # Run r script
    cmd = ["/usr/bin/Rscript", "--vanilla", "./spei.r"] + [str(lat), str(z), name]
    rOutput = call(cmd)
    if (rOutput != 0):
        print("error in r script")

# Variables for POI location
lat = 28.025880
lon = -81.732880
z = 10
name = "Winter Haven Hotel"
main(name, lat, lon, z)














# data26 = {
#     # Surface Temperature
#     "tas": Dataset("./rcp26/tas_Amon_GFDL-ESM2G_rcp26_r1i1p1_204601-205012.nc", mode = 'r'),
#     # Surface Temperature Max
#     "tasmax": Dataset("./rcp26/tasmax_Amon_GFDL-ESM2G_rcp26_r1i1p1_204601-205012.nc", mode = 'r'),
#     # Surface Temperature Min
#     "tasmin": Dataset("./rcp26/tasmin_Amon_GFDL-ESM2G_rcp26_r1i1p1_204601-205012.nc", mode = 'r'),
#     # Precipitation
#     "pr": Dataset("./rcp26/pr_Amon_GFDL-ESM2G_rcp26_r1i1p1_204601-205012.nc", mode = 'r'),
#     # Surface Wind Speed
#     "sfcWind": Dataset("./rcp26/sfcWind_Amon_GFDL-ESM2G_rcp26_r1i1p1_204601-205012.nc", mode = 'r'),
#     # Surface Solar Radiation
#     "rsds": Dataset("./rcp26/rsds_Amon_GFDL-ESM2G_rcp26_r1i1p1_204601-205012.nc", mode = 'r'),
#     # Total Cloud Cover
#     "clt": Dataset("./rcp26/clt_Amon_GFDL-ESM2G_rcp26_r1i1p1_204601-205012.nc", mode = 'r'),
#     # Humidity
#     "hurs": Dataset("./rcp26/hurs_Amon_GFDL-ESM2G_rcp26_r1i1p1_204601-205012.nc", mode = 'r'),
#     # Surface Pressure
#     "ps": Dataset("./rcp26/ps_Amon_GFDL-ESM2G_rcp26_r1i1p1_204601-205012.nc", mode = 'r')
#     # Evaporation Rate
#     # "evspsbl": Dataset("./rcp26/evspsbl_Amon_GFDL-ESM2G_rcp26_r1i1p1_204601-205012.nc", mode = 'r')
# }

# data85 = {
#     # Surface Temperature
#     "tas": Dataset("./rcp85/tas_Amon_GFDL-ESM2G_rcp85_r1i1p1_204601-205012.nc", mode = 'r'),
#     # Surface Temperature Max
#     "tasmax": Dataset("./rcp85/tasmax_Amon_GFDL-ESM2G_rcp85_r1i1p1_204601-205012.nc", mode = 'r'),
#     # Surface Temperature Min
#     "tasmin": Dataset("./rcp85/tasmin_Amon_GFDL-ESM2G_rcp85_r1i1p1_204601-205012.nc", mode = 'r'),
#     # Precipitation
#     "pr": Dataset("./rcp85/pr_Amon_GFDL-ESM2G_rcp85_r1i1p1_204601-205012.nc", mode = 'r'),
#     # Surface Win(d Speed
#     "sfcWind": Dataset("./rcp85/sfcWind_Amon_GFDL-ESM2G_rcp85_r1i1p1_204601-205012.nc", mode = 'r'),
#     # Surface Solar Radiation
#     "rsds": Dataset("./rcp85/rsds_Amon_GFDL-ESM2G_rcp85_r1i1p1_204601-205012.nc", mode = 'r'),
#     # Total Cloud Cover
#     "clt": Dataset("./rcp85/clt_Amon_GFDL-ESM2G_rcp85_r1i1p1_204601-205012.nc", mode = 'r'),
#     # Humidity
#     "hurs": Dataset("./rcp85/hurs_Amon_GFDL-ESM2G_rcp85_r1i1p1_204601-205012.nc", mode = 'r'),
#     # Surface Pressure
#     "ps": Dataset("./rcp85/ps_Amon_GFDL-ESM2G_rcp85_r1i1p1_204601-205012.nc", mode = 'r')
#     # Evaporation Rate
#     #"evspsbl": Dataset("./rcp85/evspsbl_Amon_GFDL-ESM2G_rcp85_r1i1p1_204601-205012.nc", mode = 'r')
# }


# with open('output26_2050.json', 'w') as fp:
#     dump(dataMonthly26, fp)

# with open('output85.json', 'w') as fp:
#     dump(dataMonthly85, fp)

# closeData(data26)
# closeData(data85)
# currentData.close()

# conversion(dataMonthly26)
# conversion(dataMonthly85)



# csv_columns = ["tas", "tasmax", "tasmin", "pr", "sfcWind", "rsds", "clt", "hurs", "ps", "evspsbl"]
# csv_file = "output.csv"
# try:
#     with open(csv_file, 'w', newline='') as csvfile:
#         writer = writer(csvfile)
#         writer.writeheader()
#         for data in dataMonthly:
#             writer.writerow(dataMonthly)
# except IOError:
#     print("I/O error")

# print(data.variables.keys())
# print(data['tas'].variables['lat'][:])
# print(type(cloudCoverData))
# time = cloudCoverData.variables['time']
# timeH = humidityData.variables['time']
# print(cloudCoverData.variables['lon'][:])
# print(humidityData.variables['lon'][:])

# data Start 2046 01
# clt = cltF(cloudCov, range(48, 60), 39.95, 75.16)
# print(clt)



# clt = data.variables['clt']
# print(datetime(2006, 1, 1) + timedelta(16075.5))
# print(datetime(2006, 1, 1) + timedelta(16409.5))

#ncdump(data, True)
#d = data.variables['lat'][:]
# print(data['time'][:])
# d = data.variables['lat'][]
# data.close()

#2050 Jan: 48

# cloudCoverData.close()           
# c = cloudCover(data, 59, 39.95, 75.16)
# print(c)
# clt = list(map(cloudCover(data, i_date, 39.95, 75.16), range(48, 60)))
# clt = [cloudCover(data, i_date, 39.95, 75.16) for i_date in range(48, 60)]

# clt = cloudCover(data, 48, 39.95, 75.16)
# print(clt)
# latvals = data.variables['lat'][:]
# lonvals = data.variables['lon'][:]
# def __getClosest(latvals, lonvals, latpt: int, lonpt: int) -> (int, int):
#     lat = abs(latvals - latpt).argmin()
#     lon = abs(lonvals - lonpt).argmin()
#     return lat, lon

# i_lat, i_lon = getclosest(latvals, lonvals, 39.95, 75.16)
# lat = latvals[i_lat]
# lon = lonvals[i_lon]
# # print(clt[time[48], lat, lon])
# print(clt)
# print(clt[48,i_lat,i_lon])
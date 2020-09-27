# pylint: disable=no-name-in-module
from netCDF4 import Dataset
import os
# from os import path as path
# netCDF4 data of CMIP5 projections for rcp 2.6, rcp 4.5, and rcp 8.5. 
# Data source: https://cds.climate.copernicus.eu/cdsapp#!dataset/projections-cmip5-monthly-single-levels?tab=overview
# Variables selected for SPEI calculations
    # 2m temperature (tas) Does not use for penman
    # Maximum 2m temperature in the last 24 hours (tasmax)
    # Minimum 2m temperature in the last 24 hours (tasmin)
    # Surface pressure (pr)
    # 10m wind speed (sfcWind)
    # Mean precipitation flux (pr)
    # Surface solar radiation downwards (rsds)
    # Near-surface relative humidity (hurs)
# Model chosen: GFDL-ESM2G (NOAA, USA)
# Ensemble member: r1i1p1
# Period: 204101-204512, 204601-205012, 209101-209512, 209601-210012
# Period: 204601-205012, 209601-210012


class SpeiDataset:
    def __init__(self):
        self.lat = None
        self.lon = None
        self.data = {}

    def getData(self) -> None:
        wd = os.path.dirname(__file__)
        
        # Get lat lon values
        self.lat = Dataset(os.path.join(wd, "data/lat.nc"), mode = 'r')
        self.lon = Dataset(os.path.join(wd, "data/lon.nc"), mode = 'r')

        models = ["rcp26", "rcp45", "rcp85"]
        # models = ["rcp26"]
        # years = ["204101-204512", "204601-205012", "209101-209512", "209601-210012"]
        years = ["204601-205012", "209601-210012"]
        variables = ["tasmax", "tasmin", "pr", "sfcWind", "rsds", "hurs", "ps"]

        for rcp in models:
            for year in years:
                self.data[rcp + "_" + year[7:11]] = {}
                for var in variables:
                    self.data[rcp + "_" + year[7:11]][var] = Dataset(os.path.join(wd, "data", rcp, (var + "_Amon_GFDL-ESM2G_" + rcp +"_r1i1p1_" + year + ".nc")), mode = 'r')    

    def closeData(self) -> None:
        self.lat.close()
        self.lon.close()
        for d in self.data:
            for v in self.data[d]:
                self.data[d][v].close()

        

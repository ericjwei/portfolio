from netCDF4 import Dataset
from os import path as path
# netCDF4 data of CMIP5 projections for rcp 2.6, rcp 4.5, and rcp 8.5. 
# Data source: https://cds.climate.copernicus.eu/cdsapp#!dataset/projections-cmip5-monthly-single-levels?tab=overview
# Variables selected for SPEI calculations
    # 10m wind speed
    # 2m temperature
    # Maximum 2m temperature in the last 24 hours
    # Mean precipitation flux
    # Minimum 2m temperature in the last 24 hours
    # Near-surface relative humidity
    # Surface pressure
    # Surface solar radiation downwards
    # Total cloud cover
# Model chosen: GFDL-ESM2G (NOAA, USA)
# Ensemble member: r1i1p1
# Period: 204601-205012, 209601-210012

class SpeiDataset:
    def __init__(self):
        self.lat = None
        self.lon = None
        self.data26_2050 = None
        self.data26_2100 = None
        self.data45_2050 = None
        self.data45_2100 = None
        self.data85_2050 = None
        self.data85_2100 = None
        # self.currentData = None

    def getData(self) -> None:
        wd = path.dirname(__file__)
        
        print(path.join(wd, "data/lat.nc"))
        # Get lat lon values
        self.lat = Dataset(path.join(wd, "data/lat.nc"), mode = 'r')
        self.lon = Dataset(path.join(wd, "data/lon.nc"), mode = 'r')
        self.data26_2050 = {
            # Surface Temperature
            "tas": Dataset(path.join(wd, "data/rcp26/tas_Amon_GFDL-ESM2G_rcp26_r1i1p1_204601-205012.nc"), mode = 'r'),
            # Surface Temperature Max
            "tasmax": Dataset(path.join(wd, "data/rcp26/tasmax_Amon_GFDL-ESM2G_rcp26_r1i1p1_204601-205012.nc"), mode = 'r'),
            # Surface Temperature Min
            "tasmin": Dataset(path.join(wd, "data/rcp26/tasmin_Amon_GFDL-ESM2G_rcp26_r1i1p1_204601-205012.nc"), mode = 'r'),
            # Precipitation
            "pr": Dataset(path.join(wd, "data/rcp26/pr_Amon_GFDL-ESM2G_rcp26_r1i1p1_204601-205012.nc"), mode = 'r'),
            # Surface Wind Speed
            "sfcWind": Dataset(path.join(wd, "data/rcp26/sfcWind_Amon_GFDL-ESM2G_rcp26_r1i1p1_204601-205012.nc"), mode = 'r'),
            # Surface Solar Radiation
            "rsds": Dataset(path.join(wd, "data/rcp26/rsds_Amon_GFDL-ESM2G_rcp26_r1i1p1_204601-205012.nc"), mode = 'r'),
            # Total Cloud Cover
            "clt": Dataset(path.join(wd, "data/rcp26/clt_Amon_GFDL-ESM2G_rcp26_r1i1p1_204601-205012.nc"), mode = 'r'),
            # Humidity
            "hurs": Dataset(path.join(wd, "data/rcp26/hurs_Amon_GFDL-ESM2G_rcp26_r1i1p1_204601-205012.nc"), mode = 'r'),
            # Surface Pressure
            "ps": Dataset(path.join(wd, "data/rcp26/ps_Amon_GFDL-ESM2G_rcp26_r1i1p1_204601-205012.nc"), mode = 'r')
            # Evaporation Rate
            # "evspsbl": Dataset(path.join(wd, "data/rcp26/evspsbl_Amon_GFDL-ESM2G_rcp26_r1i1p1_204601-205012.nc"), mode = 'r')
        }

        self.data26_2100 = {
            # Surface Temperature
            "tas": Dataset(path.join(wd, "data/rcp26/tas_Amon_GFDL-ESM2G_rcp26_r1i1p1_209601-210012.nc"), mode = 'r'),
            # Surface Temperature Max
            "tasmax": Dataset(path.join(wd, "data/rcp26/tasmax_Amon_GFDL-ESM2G_rcp26_r1i1p1_209601-210012.nc"), mode = 'r'),
            # Surface Temperature Min
            "tasmin": Dataset(path.join(wd, "data/rcp26/tasmin_Amon_GFDL-ESM2G_rcp26_r1i1p1_209601-210012.nc"), mode = 'r'),
            # Precipitation
            "pr": Dataset(path.join(wd, "data/rcp26/pr_Amon_GFDL-ESM2G_rcp26_r1i1p1_209601-210012.nc"), mode = 'r'),
            # Surface Wind Speed
            "sfcWind": Dataset(path.join(wd, "data/rcp26/sfcWind_Amon_GFDL-ESM2G_rcp26_r1i1p1_209601-210012.nc"), mode = 'r'),
            # Surface Solar Radiation
            "rsds": Dataset(path.join(wd, "data/rcp26/rsds_Amon_GFDL-ESM2G_rcp26_r1i1p1_209601-210012.nc"), mode = 'r'),
            # Total Cloud Cover
            "clt": Dataset(path.join(wd, "data/rcp26/clt_Amon_GFDL-ESM2G_rcp26_r1i1p1_209601-210012.nc"), mode = 'r'),
            # Humidity
            "hurs": Dataset(path.join(wd, "data/rcp26/hurs_Amon_GFDL-ESM2G_rcp26_r1i1p1_209601-210012.nc"), mode = 'r'),
            # Surface Pressure
            "ps": Dataset(path.join(wd, "data/rcp26/ps_Amon_GFDL-ESM2G_rcp26_r1i1p1_209601-210012.nc"), mode = 'r')
            # Evaporation Rate
            # "evspsbl": Dataset(path.join(wd, "data/rcp26/evspsbl_Amon_GFDL-ESM2G_rcp26_r1i1p1_209601-210012.nc"), mode = 'r')
        }       

        self.data45_2050 = {
            # Surface Temperature
            "tas": Dataset(path.join(wd, "data/rcp45/tas_Amon_GFDL-ESM2G_rcp45_r1i1p1_204601-205012.nc"), mode = 'r'),
            # Surface Temperature Max
            "tasmax": Dataset(path.join(wd, "data/rcp45/tasmax_Amon_GFDL-ESM2G_rcp45_r1i1p1_204601-205012.nc"), mode = 'r'),
            # Surface Temperature Min
            "tasmin": Dataset(path.join(wd, "data/rcp45/tasmin_Amon_GFDL-ESM2G_rcp45_r1i1p1_204601-205012.nc"), mode = 'r'),
            # Precipitation
            "pr": Dataset(path.join(wd, "data/rcp45/pr_Amon_GFDL-ESM2G_rcp45_r1i1p1_204601-205012.nc"), mode = 'r'),
            # Surface Wind Speed
            "sfcWind": Dataset(path.join(wd, "data/rcp45/sfcWind_Amon_GFDL-ESM2G_rcp45_r1i1p1_204601-205012.nc"), mode = 'r'),
            # Surface Solar Radiation
            "rsds": Dataset(path.join(wd, "data/rcp45/rsds_Amon_GFDL-ESM2G_rcp45_r1i1p1_204601-205012.nc"), mode = 'r'),
            # Total Cloud Cover
            "clt": Dataset(path.join(wd, "data/rcp45/clt_Amon_GFDL-ESM2G_rcp45_r1i1p1_204601-205012.nc"), mode = 'r'),
            # Humidity
            "hurs": Dataset(path.join(wd, "data/rcp45/hurs_Amon_GFDL-ESM2G_rcp45_r1i1p1_204601-205012.nc"), mode = 'r'),
            # Surface Pressure
            "ps": Dataset(path.join(wd, "data/rcp45/ps_Amon_GFDL-ESM2G_rcp45_r1i1p1_204601-205012.nc"), mode = 'r')
            # Evaporation Rate
            # "evspsbl": Dataset(path.join(wd, "data/rcp45/evspsbl_Amon_GFDL-ESM2G_rcp26_r1i1p1_204601-205012.nc"), mode = 'r')
        }
        
        self.data45_2100 = {
            # Surface Temperature
            "tas": Dataset(path.join(wd, "data/rcp45/tas_Amon_GFDL-ESM2G_rcp45_r1i1p1_209601-210012.nc"), mode = 'r'),
            # Surface Temperature Max
            "tasmax": Dataset(path.join(wd, "data/rcp45/tasmax_Amon_GFDL-ESM2G_rcp45_r1i1p1_209601-210012.nc"), mode = 'r'),
            # Surface Temperature Min
            "tasmin": Dataset(path.join(wd, "data/rcp45/tasmin_Amon_GFDL-ESM2G_rcp45_r1i1p1_209601-210012.nc"), mode = 'r'),
            # Precipitation
            "pr": Dataset(path.join(wd, "data/rcp45/pr_Amon_GFDL-ESM2G_rcp45_r1i1p1_209601-210012.nc"), mode = 'r'),
            # Surface Wind Speed
            "sfcWind": Dataset(path.join(wd, "data/rcp45/sfcWind_Amon_GFDL-ESM2G_rcp45_r1i1p1_209601-210012.nc"), mode = 'r'),
            # Surface Solar Radiation
            "rsds": Dataset(path.join(wd, "data/rcp45/rsds_Amon_GFDL-ESM2G_rcp45_r1i1p1_209601-210012.nc"), mode = 'r'),
            # Total Cloud Cover
            "clt": Dataset(path.join(wd, "data/rcp45/clt_Amon_GFDL-ESM2G_rcp45_r1i1p1_209601-210012.nc"), mode = 'r'),
            # Humidity
            "hurs": Dataset(path.join(wd, "data/rcp45/hurs_Amon_GFDL-ESM2G_rcp45_r1i1p1_209601-210012.nc"), mode = 'r'),
            # Surface Pressure
            "ps": Dataset(path.join(wd, "data/rcp45/ps_Amon_GFDL-ESM2G_rcp45_r1i1p1_209601-210012.nc"), mode = 'r')
            # Evaporation Rate
            # "evspsbl": Dataset(path.join(wd, "data/rcp45/evspsbl_Amon_GFDL-ESM2G_rcp26_r1i1p1_209601-210012.nc"), mode = 'r')
        }

        self.data85_2050 = {
            # Surface Temperature
            "tas": Dataset(path.join(wd, "data/rcp85/tas_Amon_GFDL-ESM2G_rcp85_r1i1p1_204601-205012.nc"), mode = 'r'),
            # Surface Temperature Max
            "tasmax": Dataset(path.join(wd, "data/rcp85/tasmax_Amon_GFDL-ESM2G_rcp85_r1i1p1_204601-205012.nc"), mode = 'r'),
            # Surface Temperature Min
            "tasmin": Dataset(path.join(wd, "data/rcp85/tasmin_Amon_GFDL-ESM2G_rcp85_r1i1p1_204601-205012.nc"), mode = 'r'),
            # Precipitation
            "pr": Dataset(path.join(wd, "data/rcp85/pr_Amon_GFDL-ESM2G_rcp85_r1i1p1_204601-205012.nc"), mode = 'r'),
            # Surface Wind Speed
            "sfcWind": Dataset(path.join(wd, "data/rcp85/sfcWind_Amon_GFDL-ESM2G_rcp85_r1i1p1_204601-205012.nc"), mode = 'r'),
            # Surface Solar Radiation
            "rsds": Dataset(path.join(wd, "data/rcp85/rsds_Amon_GFDL-ESM2G_rcp85_r1i1p1_204601-205012.nc"), mode = 'r'),
            # Total Cloud Cover
            "clt": Dataset(path.join(wd, "data/rcp85/clt_Amon_GFDL-ESM2G_rcp85_r1i1p1_204601-205012.nc"), mode = 'r'),
            # Humidity
            "hurs": Dataset(path.join(wd, "data/rcp85/hurs_Amon_GFDL-ESM2G_rcp85_r1i1p1_204601-205012.nc"), mode = 'r'),
            # Surface Pressure
            "ps": Dataset(path.join(wd, "data/rcp85/ps_Amon_GFDL-ESM2G_rcp85_r1i1p1_204601-205012.nc"), mode = 'r')
            # Evaporation Rate
            #"evspsbl": Dataset(path.join(wd, "data/rcp85/evspsbl_Amon_GFDL-ESM2G_rcp85_r1i1p1_204601-205012.nc"), mode = 'r')
        }

        self.data85_2100 = {
            # Surface Temperature
            "tas": Dataset(path.join(wd, "data/rcp85/tas_Amon_GFDL-ESM2G_rcp85_r1i1p1_209601-210012.nc"), mode = 'r'),
            # Surface Temperature Max
            "tasmax": Dataset(path.join(wd, "data/rcp85/tasmax_Amon_GFDL-ESM2G_rcp85_r1i1p1_209601-210012.nc"), mode = 'r'),
            # Surface Temperature Min
            "tasmin": Dataset(path.join(wd, "data/rcp85/tasmin_Amon_GFDL-ESM2G_rcp85_r1i1p1_209601-210012.nc"), mode = 'r'),
            # Precipitation
            "pr": Dataset(path.join(wd, "data/rcp85/pr_Amon_GFDL-ESM2G_rcp85_r1i1p1_209601-210012.nc"), mode = 'r'),
            # Surface Wind Speed
            "sfcWind": Dataset(path.join(wd, "data/rcp85/sfcWind_Amon_GFDL-ESM2G_rcp85_r1i1p1_209601-210012.nc"), mode = 'r'),
            # Surface Solar Radiation
            "rsds": Dataset(path.join(wd, "data/rcp85/rsds_Amon_GFDL-ESM2G_rcp85_r1i1p1_209601-210012.nc"), mode = 'r'),
            # Total Cloud Cover
            "clt": Dataset(path.join(wd, "data/rcp85/clt_Amon_GFDL-ESM2G_rcp85_r1i1p1_209601-210012.nc"), mode = 'r'),
            # Humidity
            "hurs": Dataset(path.join(wd, "data/rcp85/hurs_Amon_GFDL-ESM2G_rcp85_r1i1p1_209601-210012.nc"), mode = 'r'),
            # Surface Pressure
            "ps": Dataset(path.join(wd, "data/rcp85/ps_Amon_GFDL-ESM2G_rcp85_r1i1p1_209601-210012.nc"), mode = 'r')
            # Evaporation Rate
            #"evspsbl": Dataset(path.join(wd, "data/rcp85/evspsbl_Amon_GFDL-ESM2G_rcp85_r1i1p1_209601-210012.nc"), mode = 'r')
        }

        # self.currentData = Dataset(".data/spei12.nc", mode = 'r')

    def closeData(self) -> None:
        self.lat.close()
        self.lon.close()
        for d in [self.data26_2050, self.data26_2100, self.data45_2050, self.data45_2100, 
                    self.data85_2050, self.data85_2100]:
            for v in d:
                d[v].close()
        # self.currentData.close()
        

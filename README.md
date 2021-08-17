<h1 style="padding-bottom: 10px;">Climate Risk Dashboard Documentation</h1>
    <p style="font-size: 1.5em; padding-bottom: 15px;">The Climate Risk
    Dashboard is a predicted property risk assessment based on five chronic
    stress factors for two time frames (2050 and 2100). Projected environment
    data is from global climate models participating in the Coupled Model
    Intercomparison Project 5 (CMIP5), and follow three IPCC scenarios (RCP2.6,
    RCP4.5, and RCP8.5). This model data is then used to calculate each chronic
    stress factor at a specified location.
    </p>
    <h2 style="padding-bottom: 10px;">Risk Factors</h2>
    <p style="font-size: 1.5em">Drought Stress: The drought stress score
    describes the change in the water balance (precipitation minus potential
    evapotranspiration). It is based on the Standardized
    Precipitation-Evapotranspiration Index (SPEI), which is modelled with the
    penman formula using monthly averages of temperature, precipitation, solar
    radiation, humidity, and surface pressure. SPEI is calculated using the R
    SPEI package (
    <a href="https://cran.r-project.org/web/packages/SPEI/SPEI.pdf">SPEI documentation</a>). 
    This dashboard calculates the 12 month SPEI which incorporates the influence
    of the previous 12 months in calculating each month of interest.
    <h2 style="padding-bottom: 10px;">Dashboard</h2>
    This project is an interactive dashboard using Dash and plotly, written in python.
    It allows the user to input any address (processed by a geolocation api) and customize the scenario, and time phrame of interest.
    Graphs and a report tailored to the chosen variables is then outputed to the user. 
    <a href="https://github.com/ericjwei/portfolio/tree/master/portfolio/climate_risk_dash">Detailed code of climate dashboard</a>

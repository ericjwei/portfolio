from pandas import read_csv
import plotly.express as px
import plotly.graph_objects as go

import json
from requests import get
from requests.exceptions import HTTPError
from urllib.parse import quote
address = quote("  ")
try:
    response = get("https://maps.googleapis.com/maps/api/geocode/json?address=" + address + "&key=AIzaSyCTuoIYV1ihbdWZO7H6j7CEH7ObCInlus")
    response.raise_for_status()
    result = response.json()
except HTTPError as http_err:
    print('HTTP error:' + http_err)
except Exception as err:
    print(err)
else:
    if (result == None):
        print("Invalid request error")
    elif (result["status"] == "ZERO_RESULTS"):
        print("Address not found.")
    else:
        print(result)    
        address = result["results"][0]["formatted_address"]
        print(address)
        location = result["results"][0]["geometry"]["location"]
        print(location)

#     print(response.results)
# data = read_csv("./data/Courtyard - San Diego_speiData.csv")
# # print(data["26_2050"])
# print(data.iloc[:,0])

# fig = go.Figure(data = [
#     go.Scatter(y=data["26_2050"], x=data.iloc[:,0], mode='lines', fill='tozeroy')
# ])
# fig.update_yaxes(tickvals=[-2.33, -1.65, -1.28, -0.84, 0, 0.84, 1.28, 1.65, 2.33], 
#                     range=[-3, 3])

# # fig = px.line(data["26_2050"], x=data.iloc[:,0], y="26_2050", fill='tozeroy')
# fig.show()
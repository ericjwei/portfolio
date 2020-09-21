import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from pandas import read_csv
import json
from requests import get
from requests.exceptions import HTTPError
from urllib.parse import quote

# from portfolio.climate_risk_dash.spei import getSPEI
import getSPEI

def create_dashboard(server):
  dash_app = dash.Dash(
    server = server,
    routes_pathname_prefix='/climate_risk/',
    external_stylesheets=[
      dbc.themes.BOOTSTRAP,
    ]
  )

  # Navbar
  navbar = dbc.Navbar(
    [
      dbc.Row(
        [
          dbc.Col(dbc.NavbarBrand("Eric Wei Projects", href="/", external_link=True)),
          dbc.Col(html.H3("Climate Risk Dashboard"), className="text-nowrap"),
        ],
        justify="center",
      ),
      dbc.NavbarToggler(id="navbar-toggler"),
      dbc.Collapse(
        dbc.Row(
          [
            dbc.Col(dbc.NavLink("Documentation", href="/climate_risk_doc", style={"color": "black"}, external_link=True)),
          ],
          className="ml-auto flex-nowrap mt-3 mt-md-0"
        ),
        id="navbar-collapse",
        navbar=True
      ),
    ],
  )

  dash_app.title = 'Climate Risk Dashboard'

  dash_app.layout = html.Div(children=[
    navbar,
    dbc.Row(
      [
        dbc.Col(
          dbc.FormGroup(
            [
              dbc.Label("Address"),
              dbc.Input(
                type='text',
                id="address",
                placeholder="Address",
              ),
            ]
          ),
          width=6,
        ),
        dbc.Col(
          dbc.FormGroup(
            [
              dbc.Label("City"),
              dbc.Input(
                type='text',
                id="city",
                placeholder="City",
              ),
            ]
          ),
          width=6,
        ),
      ]
    ),
    dbc.Row(
      [
        dbc.Col(
          dbc.FormGroup(
            [
              dbc.Label("State/Province"),
              dbc.Input(
                type='text',
                id="state",
                placeholder="State/Province",
              ),
            ]
          ),
          width=4,
        ),
        dbc.Col(
          dbc.FormGroup(
            [
              dbc.Label("Country"),
              dbc.Input(
                type='text',
                id="country",
                placeholder="Country",
              ),
            ]
          ),
          width=4,
        ),
        dbc.Col(
          dbc.FormGroup(
            [
              dbc.Label("Zip/Postal Code"),
              dbc.Input(
                type='text',
                id="zip",
                placeholder="Zip/Postal Code",
              ),
            ]
          ),
          width=4,
        ),
      ]
    ),

    html.Div(
      [
        dbc.Button("Retrieve Data", id="submit-address", color="primary", block=True),
        html.Div(id="output")
      ]
    ),

    dbc.FormGroup(
      [
        dbc.Label("Representative Concentration Pathway (RCP)"),
        dbc.RadioItems(
          options=[
            {'label': 'RCP 2.6', 'value': '26'},
            {'label': 'RCP 4.5', 'value': '45'},
            {'label': 'RCP 8.5', 'value': '85'}
          ],
          value='26',
          id='rcp-radio',
          inline=True,
        ),
      ]
    ),

    dbc.Row(
      [
        dbc.Col(dcc.Graph(id='RCP-Graph2050'), md=6, lg=6),
        dbc.Col(dcc.Graph(id='RCP-Graph2100'), md=6, lg=6),
      ],
      no_gutters=True,
    ),

  ])

  init_callbacks(dash_app)

  return dash_app.server

def init_callbacks(dash_app):
  @dash_app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
  )
  def toggle_navbar_collapse(n, is_open):
    if n:
      return not is_open
    return is_open

  @dash_app.callback(
    Output('output', 'children'),
    [Input('submit-address', 'n_clicks')],
    [State('address', 'value'),
    State('city', 'value'),
    State('state', 'value'),
    State('country', 'value'),
    State('zip', 'value')])
  def update_address(click, address, city, state, country, zip):
    if (click):
      address = quote("".join([(address + ", ") if address else "",
      (city + ", ") if city else "",
      (state +  ", ") if state else "",
      (country + ", ") if country else "",
      (zip + ", ") if zip else ""])[:-2])
      base = "https://maps.googleapis.com/maps/api/geocode/json?address="
      key = ""

      lat = 28.025880
      lon = -81.732880
      z = 10
      name = "Winter Haven Hotel"

      currentSpei = getSPEI(name, lat, lon, z)
      print(currentSpei)

      # try:
      #     response = get(base + address + key)
      #     response.raise_for_status()
      #     result = response.json()
      # except HTTPError as http_err:
      #     raise SystemError(http_err)
      # except Exception as err:
      #     raise SystemError(err)
      # else:
      #     if (result["status"] == "ZERO_RESULTS"):
      #         return("Address not found.")
      #     else:
      #         address = result["results"][0]["formatted_address"]
      #         location = result["results"][0]["geometry"]["location"]

      #         return(address)
      location = {"lat": 47.62, "lng": -122.32}
      return address
    return ""

  @dash_app.callback(
    [Output('RCP-Graph2050', 'figure'), 
    Output('RCP-Graph2100', 'figure')],
    [Input('rcp-radio', 'value')])
  def update_figure2050(rcp):
    data = read_csv("./data/Courtyard - San Diego_speiData.csv")
    fig2050 = go.Figure(data = [
        go.Scatter(y=data[rcp + "_2050"], x=data.iloc[:,0], mode='lines', fill='tozeroy')                    
    ])
    fig2050.update_yaxes(tickvals=[-2.33, -1.65, -1.28, -0.84, 0, 0.84, 1.28, 1.65, 2.33], 
                    range=[-3, 3])
    fig2050.update_layout(transition_duration=500, 
                    title={'text': "SPEI-12 Estimate for 2050", 'xanchor': "center", 'x': 0.5}, 
                    xaxis_title="Month",
                    yaxis_title="SPEI")

    fig2100 = go.Figure(data = [
        go.Scatter(y=data[rcp + "_2100"], x=data.iloc[:,0], mode='lines', fill='tozeroy')                    
    ])
    fig2100.update_yaxes(tickvals=[-2.33, -1.65, -1.28, -0.84, 0, 0.84, 1.28, 1.65, 2.33], 
                    range=[-3, 3])
    fig2100.update_layout(transition_duration=500, 
                    title={'text': "SPEI-12 Estimate for 2100", 'xanchor': "center", 'x': 0.5}, 
                    xaxis_title="Month",
                    yaxis_title="SPEI")
    
    return fig2050, fig2100  
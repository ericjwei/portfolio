import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from pandas import read_csv
import json
from requests import get
from requests.exceptions import HTTPError
from urllib.parse import quote
from os import path, getenv
from datetime import datetime
from dateutil.relativedelta import relativedelta

from portfolio.climate_risk_dash.spei import getSPEI, currentSpei

DEBUG = False

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
      ]
    ),

    dbc.Jumbotron(
      [
        html.H3("Search a location.", id="location", className="text-center"),
        html.P(id="lng", className="lead text-center"),
        html.P(id="lat", className="lead text-center"),
        html.H3(id="curMonth", className="text-center"),
        html.P(id="curSpei", className="lead text-center"),
        html.P(id="err", className="lead text-center"),
        html.P(id="speiErr", className="lead text-center"),
      ]
    ),

    dbc.FormGroup(
      [
        html.H3("Predicted Risk", className="text-center"),
        html.H4("Representative Concentration Pathway (RCP)", className="text-center"),
        dbc.RadioItems(
          options=[
            {'label': 'RCP 2.6', 'value': 'rcp26'},
            {'label': 'RCP 4.5', 'value': 'rcp45'},
            {'label': 'RCP 8.5', 'value': 'rcp85'}
          ],
          value='rcp26',
          id='rcp-radio',
          inline=True,
          style={'textAlign': 'center'}
        ),
      ],
    id='rcpForm',
    style={'display': 'none'}
    ),

    # html.Div(id="currentSPEI", className="lead text-center"),

    dbc.Row(
      [
        dbc.Col(html.Div(id="speiGraph2050"), md=6, lg=6),
        dbc.Col(html.Div(id="speiGraph2100"), md=6, lg=6),    
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
    [Output('location', 'children'),
    Output('lat', 'children'),
    Output('lng', 'children'),
    Output('curMonth', 'children'),
    Output('curSpei', 'children'),
    Output('err', 'children')],
    [Input('submit-address', 'n_clicks')],
    [State('address', 'value'),
    State('city', 'value'),
    State('state', 'value'),
    State('country', 'value'),
    State('zip', 'value')])
  def update_address(click, address: str, city: str, state: str, country: str, zip: str):
    if (click):
      address = quote("".join([(address + ", ") if address else "",
      (city + ", ") if city else "",
      (state +  ", ") if state else "",
      (country + ", ") if country else "",
      (zip + ", ") if zip else ""])[:-2])
      base = "https://maps.googleapis.com/maps/api/geocode/json?address="
      GEO_KEY = getenv('GEO_KEY')
      key = ("&key=" + GEO_KEY)
      
      if(DEBUG):
        location = "412 Broadway Seattle WA 98122 USA"
        # currentSPEI = getSPEI(location, 47.6058925, -122.3203337)
        currentSPEI = 0
        today = datetime.today()
        pastMonth = today - relativedelta(months=1)
        return[location, 'Latitude: {}'.format(0), 'Longitude: {}'.format(0), 
                        'Risk assessment for {}'.format(pastMonth.strftime("%B")), 'Spei-12: {}'.format(currentSPEI),
                        None]

      try:
          response = get(base + address + key)
          response.raise_for_status()
          result = response.json()
      except HTTPError as http_err:
          raise SystemError(http_err)
      except Exception as err:
          raise SystemError(err)
      else:
          if (result["status"] == "ZERO_RESULTS"):
              return(None, None, None, None, None, "Address not found.")
          else:
              location = result["results"][0]["formatted_address"]
              latlng = result["results"][0]["geometry"]["location"]
              try:
                currentSPEI = getSPEI(location.replace(",", ""), latlng["lat"], latlng["lng"])
              except Exception as err:
                return[None, None, None, None, None, "Error calculating SPEI"]
              else:
                today = datetime.today()
                pastMonth = today - relativedelta(months=1)
                return[location, 'Latitude: {}'.format(latlng["lat"]), 'Longitude: {}'.format(latlng["lng"]), 
                                'Risk assessment for {}'.format(pastMonth.strftime("%B")), 'Spei-12: {}'.format(currentSPEI), 
                                None]
    else:
      raise PreventUpdate
    
  @dash_app.callback(
    [Output('speiGraph2050', 'children'),
    Output('speiGraph2100', 'children'),
    Output('rcpForm', 'style'),
    Output('speiErr', 'children')],
    [Input('location', 'children'), 
    Input('rcp-radio', 'value')], prevent_initial_call=True)
  def update_spei_figure(location: str, rcp: str):
    if location is None:
      raise PreventUpdate
    wd = path.dirname(__file__)
    location = location.replace(",", "")
    f = path.join(wd, "report", (location + "_speiData.csv"))
 
    try:
      data = read_csv(f)
    except IOError:
      # return(None, None, "Error loading SPEI graph, please try again later.")
      return(None, None, {'display': 'none'}, "Error loading SPEI graph, please try again later.")

    fig2050 = go.Figure(data = [
        go.Scatter(y=data[rcp + "_2050"][12:], x=data["date"][13:], mode='lines', fill='tozeroy')                    
    ])
    fig2050.update_yaxes(tickvals=[-2.33, -1.65, -1.28, -0.84, 0, 0.84, 1.28, 1.65, 2.33], 
                    range=[-3, 3])
    fig2050.update_layout(transition_duration=500, 
                    title={'text': "SPEI-12 Estimate for 2050", 'xanchor': "center", 'x': 0.5}, 
                    xaxis_title="Date",
                    yaxis_title="SPEI")

    fig2100 = go.Figure(data = [
        go.Scatter(y=data[rcp + "_2100"][12:], x=data["date"][13:], mode='lines', fill='tozeroy')                    
    ])
    fig2100.update_yaxes(tickvals=[-2.33, -1.65, -1.28, -0.84, 0, 0.84, 1.28, 1.65, 2.33], 
                    range=[-3, 3])
    fig2100.update_layout(transition_duration=500, 
                    title={'text': "SPEI-12 Estimate for 2100", 'xanchor': "center", 'x': 0.5}, 
                    xaxis_title="Date",
                    yaxis_title="SPEI")
    
    return[dcc.Graph(id='RCP-Graph2050', figure=fig2050), dcc.Graph(id='RCP-Graph2100', figure=fig2100),
                      {'display': 'block'}, None]  

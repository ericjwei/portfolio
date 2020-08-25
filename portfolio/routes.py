from flask import current_app as app
from flask import render_template

@app.route('/')
def index():
  return render_template('index.html', title="Home")

@app.route('/climate_risk_doc')
def climateDoc():
  return render_template('climate_documentation.html')

@app.route('/hello/<name>')
def hello(name):
    return 'Hello ' + name

@app.route('/about')
def about():
    return render_template('bio.html')

# @app.route('/ClimateRisk')
# def ClimateRisk():
#     return "Climate Risk"

from flask import current_app as app

@app.route('/')
def home():
    return "Home"

@app.route('/hello/<name>')
def hello(name):
    return 'Hello ' + name

# @app.route('/ClimateRisk')
# def ClimateRisk():
#     return "Climate Risk"

from flask import current_app as app
from flask import render_template, send_from_directory
from os import path as path

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

@app.route('/resume', methods=['GET'])
def getResume():
  uploads = path.join(app.root_path, app.config['UPLOAD_FOLDER'])
  return send_from_directory(directory=uploads, filename="Eric Wei_Resume.pdf", 
                          as_attachment=True)

# @app.route('/ClimateRisk')
# def ClimateRisk():
#     return "Climate Risk"

from flask import render_template
from flask import current_app as app

@app.route('/')
def home():
    return render_template(
        'index.jinja2',
        title='Plotly Dash Flask',
        description='Climate risk embed',
        template='home-template',
        body='Home Page'
    )
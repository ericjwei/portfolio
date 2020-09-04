from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

UPLOAD_FOLDER = 'static/'
GEO_KEY = environ.get('GEO_KEY')

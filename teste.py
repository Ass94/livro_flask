import os
import string

TEMPLATE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

print(TEMPLATE_FOLDER)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

print('Root dir: ', ROOT_DIR)

app_active = os.getenv('FLASK_ENV_TEST')

print(app_active)
from flask import Flask

app = Flask(__name__, instance_relative_config=True)
# load the instance config
app.config.from_pyfile('config.py')

import application.views
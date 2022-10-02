from quart import Quart

app = Quart(__name__, instance_relative_config=True)#
# load the instance config
app.config.from_pyfile('config.py')

import application.views
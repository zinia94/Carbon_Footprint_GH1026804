from flask import Flask, session
from src.routes import Routes
from .db import db
from flask_bootstrap import Bootstrap
import flask_excel as excel

# the root of the appliction and the routes

app = Flask(__name__)

app.json.sort_keys = False
app.secret_key = 'secret'
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
excel.init_excel(app)

db.init_app(app)

routes = Routes(app, session)
routes.initRoutes()
    



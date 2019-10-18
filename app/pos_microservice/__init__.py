import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient
from flask_mongoalchemy import MongoAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
app = Flask(__name__)

# #client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'],27017)
# client = MongoClient('mongodb://db:27017/')
# db = client.tododb
# db = client.PointOfSale_DB

app.config['MONGOALCHEMY_DATABASE'] = 'PointOfSale_DB'
app.config['MONGOALCHEMY_CONNECTION_STRING'] = 'mongodb://db:27017/'
app.config['MONGOALCHEMY_ECHO'] = True
db = MongoAlchemy(app)

# Init marshmallow
ma = Marshmallow(app)

# Bcrypt
bcrypt = Bcrypt(app)



from pos_microservice.pointOfSale.routes import pos
app.register_blueprint(pos)

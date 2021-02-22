#import the flask library
from flask import Flask
from config import Config

#configure an object of class Flask with __name__
app = Flask(__name__)
app.config.from_object(Config)

#here app is a package not to be confused with directory app
from app import routes
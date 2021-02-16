#import the flask library
from flask import Flask 

#configure an object of class Flask with __name__
app = Flask(__name__)

#here app is a package not to be confused with directory app
from app import routes
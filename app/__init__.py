from flask import Flask


#creating an instance of the Flask class(it takes one input)
app = Flask(__name__)


from . import routes
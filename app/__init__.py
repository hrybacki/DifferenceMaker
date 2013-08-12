__author__ = 'jakerose27'

from flask import Flask

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['txt'])


from app import DifferenceMaker

from flask import Flask

app = Flask(__name__)

from .views import main
from .views import lol
from .views import bser
from .views import pubg

app.register_blueprint(main.main_BluePrint)
app.register_blueprint(lol.lol_BluePrint)
app.register_blueprint(bser.bser_BluePrint)
app.register_blueprint(pubg.pubg_BluePrint)
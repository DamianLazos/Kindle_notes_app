# ******************************PYTHON LIBRARIES******************************
import os
# ******************************EXTERNAL LIBRARIES****************************
from flask import Flask
from dotenv import load_dotenv
# ******************************OWN LIBRARIES*********************************
from routes.routes import blp as KindleBlueprint
# ****************************************************************************
load_dotenv()

def create_app():
    
    app = Flask(__name__)
    
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    
    app.register_blueprint(KindleBlueprint)
    
    return app
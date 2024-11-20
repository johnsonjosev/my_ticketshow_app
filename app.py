from flask import Flask
from backend.models import db
app = None

def setup_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ticket_show2.sqlite3" 
    # Implement sqlite connection
    db.init_app(app) # Flask app is connected to DB
    app.debug =True
    app.app_context().push() # Direct access to other modules
    print(" Ticket Show is started...")



# Call the set up to enable calling methods form external modules like controllers... 
# else it will throw error
setup_app()

from backend.controllers import *
if __name__ =="__main__":
    
    app.run(port=5522)
## to create instance folder
# Go to python in commandline, run below commands
# from backend.models import  *
# from app import *
# db.create_all()

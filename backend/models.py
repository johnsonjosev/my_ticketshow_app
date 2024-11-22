# Data models

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserInfo(db.Model):
    __tablename__ = "user_info"
    id = db.Column(db.Integer,primary_key = True)
    email =db.Column(db.String, unique=True,nullable=False)
    password = db.Column(db.String,nullable=False)
    role=db.Column(db.Integer,default =1)
    full_name = db.Column(db.String,nullable=False)
    address = db.Column(db.String,nullable=False)
    pin_code = db.Column(db.Integer,nullable=False)
    
    # ToDo: relationships
    #user can acess all of his tickets
    tickets = db.relationship("Ticket",cascade="all,delete",backref="user_info",lazy=True)


class Theatre(db.Model):
    __tablename__ = "theatre"
    id =db.Column(db.Integer,primary_key = True)
    name =db.Column(db.String, unique=True,nullable=False)
    location = db.Column(db.String,nullable=False)
    pin_code = db.Column(db.Integer,nullable=False)
    capacity = db.Column(db.Integer,nullable=False)
    venue_pic_url = db.Column(db.String,nullable=True,default="None")
    

    #Theatre  can acess all of its shows
    shows = db.relationship("Show",cascade="all,delete",backref="theatre",lazy=True)


class Show(db.Model):
    __tablename__ = "show"
    id =db.Column(db.Integer,primary_key = True)
    name =db.Column(db.String, unique=True,nullable=False)
    tags = db.Column(db.String,nullable=False)
    rating = db.Column(db.Integer,default=0)
    tkt_price = db.Column(db.Float,default=0.0)
    date_time = db.Column(db.DateTime,nullable=False)
    theatre_id =  db.Column(db.Integer,db.ForeignKey("theatre.id"),nullable=False)


class Ticket(db.Model):
    __tablename__ = "ticket"
    id =db.Column(db.Integer,primary_key = True)
    no_of_tickets = db.Column(db.Integer,default=0)
    sl_nos = db.Column(db.String,nullable=False)
    rating = db.Column(db.Integer,default=0) 
    user_id =  db.Column(db.Integer,db.ForeignKey("user_info.id"),nullable=False)
    show_id =  db.Column(db.Integer,db.ForeignKey("show.id"),nullable=False)
    

    

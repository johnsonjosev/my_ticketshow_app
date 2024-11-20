# All App routes
from flask import render_template,request,redirect,url_for
from flask import current_app as app
from .models import *
from datetime import datetime
@app.route("/")
def home():
    return render_template("index.html")

# common route for admin dashboard
@app.route("/admin/<name>")
def admin_dashboard(name):
    theathres = get_theatres()
    return render_template("admin_dashboard.html",name = name,theatres=theathres) 

# common route for user dashboard
@app.route("/user/<name>")
def user_dashboard(name):
    return render_template("user_dashboard.html",name = name) 

@app.route("/login",methods=["GET","POST"])
def signin():
    if request.method == "POST":
        uname = request.form.get('user_name')
        password = request.form.get('password')

        usr = UserInfo.query.filter_by(email=uname,password=password).first()
        if usr and usr.role==0:
            return redirect(url_for("admin_dashboard", name=uname))
        elif usr and usr.role==1:
            return redirect(url_for("user_dashboard", name=uname))
        else:
            return render_template("login.html",msg= "Invalid User Credentials")
    return render_template("login.html",msg="")

@app.route("/register",methods=["GET","POST"])
def signup():
    if request.method == "POST":
        uname = request.form.get('user_name')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        location = request.form.get('location')
        pincode = request.form.get('pincode')

        usr = UserInfo.query.filter_by(email=uname).first()
        if usr:
            return render_template("signup.html",msg="Sorry, this mail already registered...!")
        new_user = UserInfo(email=uname,password=password,full_name=full_name,address=location,pin_code=pincode)
        db.session.add(new_user)
        db.session.commit()
        return render_template("login.html",msg="Registered Successfully, Try login now")

    return render_template("signup.html",msg="")

@app.route("/venue/<name>",methods=["GET","POST"])
def add_venue(name):
    if request.method == "POST":
        vname = request.form.get('name')
        location = request.form.get('location')
        capacity = request.form.get('capacity')
        pincode = request.form.get('pincode')
        new_theatre = Theatre(name=vname,location=location,pin_code=pincode,capacity=capacity)
        db.session.add(new_theatre)
        db.session.commit()
        return redirect(url_for("admin_dashboard", name=name))
        #return render_template("admin_dashboard.html",name= name,msg="Theatre Successfully Added")

    return render_template("add_venue.html",name=name)

@app.route("/show/<v_id>/<name>",methods=["GET","POST"])
def add_show(v_id,name):
    if request.method == "POST":
        sname = request.form.get('name')
        tags = request.form.get('tags')
        rating = request.form.get('rating')
        tkt_price = request.form.get('tkt_price')
        date_time = request.form.get('date_time')
        date_time = datetime.strptime(date_time,"%Y-%m-%dT%H:%M")
        theatre_id = request.form.get('theatre_id')
        new_show = Show(name=sname,tags=tags,rating=rating,tkt_price=tkt_price,date_time=date_time,theatre_id=v_id)
        db.session.add(new_show)
        db.session.commit()
        return redirect(url_for("admin_dashboard", name=name))
        #return render_template("admin_dashboard.html",name= name,msg="Theatre Successfully Added")

    return render_template("add_show.html",v_id=v_id,name=name)


#other support functions

def get_theatres():
    theatres = Theatre.query.all()
    return theatres
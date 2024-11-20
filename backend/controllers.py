# All App routes
from flask import render_template,request
from flask import current_app as app
from .models import *
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login",methods=["GET","POST"])
def signin():
    if request.method == "POST":
        uname = request.form.get('user_name')
        password = request.form.get('password')

        usr = UserInfo.query.filter_by(email=uname,password=password).first()
        if usr and usr.role==0:
            return render_template("admin_dashboard.html") 
        elif usr and usr.role==1:
            return render_template("user_dashboard.html") 
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


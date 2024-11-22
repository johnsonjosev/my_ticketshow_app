# All App routes
from flask import render_template,request,redirect,url_for
from flask import current_app as app
from .models import *
from datetime import datetime
from sqlalchemy import func
@app.route("/")
def home():
    return render_template("index.html")

# common route for admin dashboard
@app.route("/admin/<name>")
def admin_dashboard(name):
    theathres = get_theatres()
    return render_template("admin_dashboard.html",name = name,theatres=theathres) 

# common route for user dashboard
@app.route("/user/<id>/<name>")
def user_dashboard(id,name):
    theathres = get_theatres()
    dt_time_now=datetime.today().strftime("%Y-%m-%dT%H:%M")
    dt_time_now=datetime.strptime(dt_time_now,"%Y-%m-%dT%H:%M")
    return render_template("user_dashboard.html", dt_time_now=dt_time_now,uid=id,name = name,theatres=theathres) 

@app.route("/login",methods=["GET","POST"])
def signin():
    if request.method == "POST":
        uname = request.form.get('user_name')
        password = request.form.get('password')

        usr = UserInfo.query.filter_by(email=uname,password=password).first()
        if usr and usr.role==0:
            return redirect(url_for("admin_dashboard", name=uname))
        elif usr and usr.role==1:
            return redirect(url_for("user_dashboard", name=uname,id= usr.id))
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


@app.route("/search/<name>",methods=["GET","POST"])
def search(name):
    if request.method == "POST":
        search_txt = request.form.get('search_txt')
        by_venue = search_by_venue(search_txt)
        by_loc = search_by_loc(search_txt)
        if by_venue:
            return render_template("admin_dashboard.html",name = name,theatres=by_venue) 
        elif by_loc:
            return render_template("admin_dashboard.html",name = name,theatres=by_loc)        
        else:
            return redirect(url_for("admin_dashboard", name=name))        
    return redirect(url_for("admin_dashboard", name=name))

@app.route("/edit_venue/<id>/<name>",methods=["GET","POST"])
def edit_venue(id,name):
    v =get_venue(id)
    if request.method == "POST":
        vname = request.form.get('name')
        location = request.form.get('location')
        capacity = request.form.get('capacity')
        pincode = request.form.get('pincode')

        v.name = vname
        v.location = location
        v.capacity = capacity
        v.pin_code = pincode
        db.session.commit()
        return redirect(url_for("admin_dashboard", name=name))
    return render_template("edit_venue.html",venue=v,name=name)
   
@app.route("/delete_venue/<id>/<name>",methods=["GET","POST"])
def delete_venue(id,name):
    v =get_venue(id)
    if v:
        db.session.delete(v)
        db.session.commit()
    return redirect(url_for("admin_dashboard", name=name))

@app.route("/edit_show/<id>/<name>",methods=["GET","POST"])
def edit_show(id,name):
    v =get_show(id)
    if request.method == "POST":
        sname = request.form.get('name')
        tags = request.form.get('tags')
        rating = request.form.get('rating')
        tkt_price = request.form.get('tkt_price')
        date_time = request.form.get('date_time')
        date_time = datetime.strptime(date_time,"%Y-%m-%dT%H:%M")

        v.name = sname    
        v.tags = tags
        v.rating = rating
        v.tkt_price = tkt_price
        v.date_time = date_time
        db.session.commit()

        return redirect(url_for("admin_dashboard", name=name))
    return render_template("edit_show.html",show=v,name=name)
   
@app.route("/delete_show/<id>/<name>",methods=["GET","POST"])
def delete_show(id,name):
    s=get_show(id)
    if s:
        db.session.delete(s)
        db.session.commit()
    return redirect(url_for("admin_dashboard", name=name))

@app.route("/book_ticket/<uid>/<sid>/<name>",methods=["GET","POST"])
def book_ticket(uid,sid,name):
    if request.method == "POST":
        no_tickets = request.form.get('no_tickets')
        new_ticket = Ticket(no_of_tickets = no_tickets,sl_nos=" ",user_id=uid,show_id=sid)
        db.session.add(new_ticket)
        db.session.commit()
        return redirect(url_for("user_dashboard",id=uid, name=name))
    
    # Get methods
    show = Show.query.filter_by(id=sid).first()
    theatre = Theatre.query.filter_by(id = show.theatre_id).first()
    available_seats = theatre.capacity

    #booked_tickets by aggregate function sum

    book_tickets = Ticket.query.with_entities(func.sum(Ticket.no_of_tickets)).group_by(Ticket.show_id).filter_by(show_id=sid).first()
    book_ticket
    if book_tickets:
        available_seats -=book_tickets[0]
    return render_template("book_ticket.html",uid=uid,sid=sid,name=name,tname=theatre.name,sname=show.name,available_seats=available_seats,tkt_price=show.tkt_price)



    



#other support functions

def get_theatres():
    theatres = Theatre.query.all()
    return theatres


def search_by_venue(search_txt):
    theatres = Theatre.query.filter(Theatre.name.ilike(f"%{search_txt}%"))
    return  theatres

def search_by_loc(search_txt):
    theatres = Theatre.query.filter(Theatre.location.ilike(f"%{search_txt}%"))
    return  theatres

def get_venue(id):
    theatre = Theatre.query.filter_by(id=id).first()
    return theatre

def get_show(id):
    show = Show.query.filter_by(id=id).first()
    return show
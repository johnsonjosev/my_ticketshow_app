from flask_restful import Resource, Api
from flask import request,make_response
from .models import *
from json import JSONEncoder, dumps
from datetime import datetime
api = Api()

class ShowApi(Resource):

    def get(self):
        shows = Show.query.all()
        shows_json =[]
        for show in shows:
            shows_json.append(
                {'id':show.id,'name':show.name,'tags':show.tags,
                'rating':show.rating,'tkt_price':show.tkt_price,
                'date_time':str(show.date_time),'theatre_id':show.theatre_id})
        # response = make_response(dumps(shows_json))
        # response.headers['Content-Type'] = 'application/json'
        # response.headers['mimetype'] = 'application/json'
        return shows_json


    def post(self):
        name = request.json.get("name")
        tags = request.json.get("tags")
        rating = request.json.get("rating")
        tkt_price = request.json.get("tkt_price")
        theatre_id = request.json.get("theatre_id")
        dt_time = request.json.get("date_time")
        dt_time= datetime.strptime(dt_time,"%Y-%m-%d %H:%M:%S")
        new_show = Show(name=name,tags=tags,rating=rating,tkt_price=tkt_price,date_time=dt_time,theatre_id=theatre_id)
        db.session.add(new_show)
        db.session.commit()

        return {"message": "New show added"},201

    def put(self,id):
        show = Show.query.filter_by(id=id).first()
        if show:
            show.name = request.json.get("name")
            show.tags = request.json.get("tags")
            show.rating = request.json.get("rating")
            show.tkt_price = request.json.get("tkt_price")
            show.theatre_id = request.json.get("theatre_id")
            dt_time = request.json.get("date_time")
            show.date_time= datetime.strptime(dt_time,"%Y-%m-%d %H:%M:%S")
            db.session.commit()
            return {"message": "Show updated"},200
        return {"message": "Show ID not Found"},404


    def delete(self,id):
        show = Show.query.filter_by(id=id).first()
        if show:
            db.session.delete(show)
            db.session.commit()
            return {"message": "Show deleted"},200
        return {"message": "Show ID not Found"},404

class ShowSearchApi(Resource):

    def get(self,id):
        show = Show.query.filter_by(id=id).first()
        if show:
            shows_json =[]
            shows_json.append(
                    {'id':show.id,'name':show.name,'tags':show.tags,
                    'rating':show.rating,'tkt_price':show.tkt_price,
                    'date_time':str(show.date_time),'theatre_id':show.theatre_id})
            return shows_json
        return {"message": "Show ID not Found"},404


api.add_resource(ShowApi,"/api/get_shows","/api/create_show","/api/edit_show/<id>","/api/delete_show/<id>")
api.add_resource(ShowSearchApi,"/api/search_show/<id>")
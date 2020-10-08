#!/usr/bin/env python3

import os

from datetime import date
from flask import jsonify, Flask, request
from flask.json import JSONEncoder  # for date formatting
from flask_sqlalchemy import SQLAlchemy
from time import time

# Add CRUD functionality
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

# REMEMBER to import the tables you want to query!
from database_setup import Base, President, Police

engine = create_engine(os.environ['DATABASE_URL'])
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.deafult(self, obj)


app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# db = SQLAlchemy(app)


# class PresidentModel(db.Model):
#     __tablename__ = ''

#     globaleventid = db.Column(db.Integer(), primary_key=True)
#     date = db.Column(db.Date())
#     actor1name = db.Column(db.Text())
#     actor2name = db.Column(db.Text())
#     eventcode = db.Column(db.Text())
#     quadclass = db.Column(db.Integer())
#     goldsteinscale = db.Column(db.Float())
#     nummentions = db.Column(db.Integer())
#     numsources = db.Column(db.Integer())
#     numarticles = db.Column(db.Integer())
#     avgtone = db.Column(db.Float())
#     sourceurl = db.Column(db.Text())

#     def __init__(self, globaleventid, date, actor1name, actor2name, eventcode,
#                  quadclass, goldsteinscale, nummentions, numsources,
#                  numarticles, avgtone, sourceurl):
#         self.event_id = globaleventid
#         self.date = date
#         self.actor1_name = actor1name
#         self.actor2_name = actor2name
#         self.event_code = eventcode
#         self.quad_class = quadclass
#         self.goldstein_scale = goldsteinscale
#         self.num_mentions = nummentions
#         self.num_sources = numsources
#         self.num_articles = numarticles
#         self.avg_tone = avgtone
#         self.source_URL = sourceurl


# def gather_data(tablename):
#     '''
#     Gathers data for delivery.

#     Parameters
#     ----------
#     tablename : str
#         The tablename for the respective query

#     Returns
#     -------
#     list
#         The list generated from the query
#     '''
#     PresidentModel.__tablename__ = tablename

#     print("Gathering data...")
#     start = time()
#     DATA_LIST = [{
#         'Event ID': event.globaleventid,
#         'Date': event.date,
#         'Actor1 Name': event.actor1name,
#         'Actor2 Name': event.actor2name,
#         'Event Code': event.eventcode,
#         'Quad Class': event.quadclass,
#         'Goldstein Scale': event.goldsteinscale,
#         'Num Mentions': event.nummentions,
#         'Num Sources': event.numsources,
#         'Num Articles': event.numarticles,
#         'Average Tone': event.avgtone,
#         'Source URL': event.sourceurl
#     } for event in PresidentModel.query.all()]
#     end = time()
#     print("Done!")
#     print(f"Total time: {end-start:0.2f} sec")

#     return DATA_LIST

# FILTERING THE DATA MORE decreases load time...
# Consider high filtering of data.
# print("Gathering data...")
# start = time()
# DATA_LIST = [{
#     'Event ID': event.globaleventid,
#     'Date': event.date,
#     'Actor1 Name': event.actor1name,
#     'Actor2 Name': event.actor2name,
#     'Event Code': event.eventcode,
#     'Quad Class': event.quadclass,
#     'Goldstein Scale': event.goldsteinscale,
#     'Num Mentions': event.nummentions,
#     'Num Sources': event.numsources,
#     'Num Articles': event.numarticles,
#     'Average Tone': event.avgtone,
#     'Source URL': event.sourceurl
# } for event in PresidentModel.query.all()]
# end = time()
# print("Done!")
# print(f"Total time: {end-start:0.2f} sec")


# Again, include the ending '/' in case the user forgets
@app.route('/events/president/positive/high/')
def president_pos_high():
    '''
    Displays just a test query.
    '''
    positive_impact = session.query(President).filter(
        and_(President.avgtone > 0, President.goldsteinscale > 5)
    )

    return jsonify(HighPositive=[event.serialize for event in positive_impact])


@app.route('/events/president/negative/high/')
def president_neg_high():
    '''
    Displays next test query.
    '''
    negative_impact = session.query(President).filter(
        and_(President.avgtone < 0, President.goldsteinscale > 5)
    )

    return jsonify(HighNegative=[event.serialize for event in negative_impact])


@app.route('/events/police/negative/high/')
def police_neg_high():
    '''
    Displays location by state.
    '''
    police_impact = session.query(Police).filter(and_(
        Police.AvgTone < 0,
        Police.GoldsteinScale > 5,
        Police.IsRootEvent
    ))

    return jsonify(PoliceImpact=[
        event.serialize for event in police_impact
    ])


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

#!/usr/bin/env python3

import os

from datetime import date
from flask import jsonify, Flask, request, redirect, render_template, url_for
from flask.json import JSONEncoder  # for date formatting
from flask_sqlalchemy import SQLAlchemy
from time import time

# Add CRUD functionality
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

# REMEMBER to import the tables you want to query!
from database_setup import (
    Base, President, Police, PoliceNeg, PolicePos, PresidentPos, PresidentNeg
)

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


@app.route('/', methods=['GET', 'POST'])
def home():
    '''
    Displays the home page. Contains a form for URL entry.
    '''
    if request.method == 'POST':
        url = request.form['url']

        url_route = url.split('/')[2:]
        url_route[1] = url_route[1][:3]
        url_route = '_'.join(url_route)

        return redirect(url_for(url_route))
    else:
        return render_template('home.html')

# Again, include the ending '/' in case the user forgets
@app.route('/events/president/positive/high/')
def president_pos_high():
    '''
    Displays just a test query.
    '''
    positive_impact = session.query(PresidentPos).all() # filter(
    #     and_(President.avgtone > 0, President.goldsteinscale > 5)
    # )

    return jsonify(HighPositive=[event.serialize for event in positive_impact])


@app.route('/events/president/negative/high/')
def president_neg_high():
    '''
    Displays next test query.
    '''
    negative_impact = session.query(PresidentNeg).all()  # .filter(
    #     and_(President.avgtone < 0, President.goldsteinscale > 5)
    # )

    return jsonify(HighNegative=[
         event.serialize for event in negative_impact])
    # return render_template('president_neg.html',
    #                        negative_impact=negative_impact)


@app.route('/events/police/negative/high/')
def police_neg_high():
    '''
    Displays location by state.
    '''
    police_impact = session.query(PoliceNeg).all()  # filter(and_(
    #     Police.AvgTone < 0,
    #     Police.GoldsteinScale > 5,
    #     Police.IsRootEvent
    # ))

    return jsonify(PoliceImpact=[
         event.serialize for event in police_impact
    ])
    #  return render_template('police_results.html',
    #                        police_impact=police_impact)

@app.route('/events/police/positive/high/')
def police_pos_high():
    '''
    Displays event data where police is actor and reaction is positive.
    '''
    police_impact = session.query(PolicePos).all()

    return jsonify(PoliceImpact=[
        event.serialize for event in police_impact
    ])


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

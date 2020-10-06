import os

from flask import jsonify, Flask, request
from flask_sqlalchemy import SQLAlchemy
from time import time

# PostgreSQL INFO
user = os.environ['PG_USER']
password = os.environ['PG_PWD']
mode = "append"
url = "jdbc:postgresql://localhost:5432/gdelt_data"
properties = {"user": user, "password": password,
              "driver": "org.postgresql.Driver"}

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


class PresidentModel(db.Model):
    __tablename__ = 'pres_positive_high'

    globaleventid = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Date())
    actor1name = db.Column(db.Text())
    actor2name = db.Column(db.Text())
    eventcode = db.Column(db.Text())
    quadclass = db.Column(db.Integer())
    goldsteinscale = db.Column(db.Float())
    nummentions = db.Column(db.Integer())
    numsources = db.Column(db.Integer())
    numarticles = db.Column(db.Integer())
    avgtone = db.Column(db.Float())
    sourceurl = db.Column(db.Text())

    def __init__(self, globaleventid, date, actor1name, actor2name, eventcode,
                 quadclass, goldsteinscale, nummentions, numsources,
                 numarticles, avgtone, sourceurl):
        self.event_id = globaleventid
        self.date = date
        self.actor1_name = actor1name
        self.actor2_name = actor2name
        self.event_code = eventcode
        self.quad_class = quadclass
        self.goldstein_scale = goldsteinscale
        self.num_mentions = nummentions
        self.num_sources = numsources
        self.num_articles = numarticles
        self.avg_tone = avgtone
        self.source_URL = sourceurl


# FILTERING THE DATA MORE decreases load time...
# Consider high filtering of data.
print("Gathering data...")
start = time()
DATA_LIST = [{
    'Event ID': event.globaleventid,
    'Date': event.date,
    'Actor1 Name': event.actor1name,
    'Actor2 Name': event.actor2name,
    'Event Code': event.eventcode,
    'Quad Class': event.quadclass,
    'Goldstein Scale': event.goldsteinscale,
    'Num Mentions': event.nummentions,
    'Num Sources': event.numsources,
    'Num Articles': event.numarticles,
    'Average Tone': event.avgtone,
    'Source URL': event.sourceurl
} for event in PresidentModel.query.all()]
end = time()
print("Done!")
print(f"Total time: {end-start:0.2f} sec")


@app.route('/events/president/positive/high')
def run_test_query():
    '''
    Displays just a test query.
    '''

    return jsonify(Data=DATA_LIST)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

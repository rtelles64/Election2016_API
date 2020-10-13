#!/usr/bin/env python3

# This file sets up database access

# 4 Major components to creating a database with SQLAlchemy:
# 1. Configuration
# 2. Class
# 3. Table
# 4. Mapper

import os

# handy for mapper
from sqlalchemy import Column, Integer, String, Float, Date, Text, Boolean
# for configuration and class code
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine  # for configuration at end

# let's sqlalchemy know that our classes are special sqlalchemy classes
Base = declarative_base()


# CLASS (contains TABLE and MAPPER code)
class President(Base):
    '''
    Class to represent 'presidential' table.
    '''
    # TABLE
    # sqlalchemy syntax: __tablename__ = 'some_table'
    __tablename__ = 'presidential'

    # MAPPER
    # sqlalchemy syntax: column_name = Column(attributes, ...)
    globaleventid = Column(Integer, primary_key=True)
    date = Column(Date, primary_key=True)
    actor1name = Column(Text, primary_key=True)
    actor2name = Column(Text)
    eventcode = Column(Text)
    quadclass = Column(Integer)
    goldsteinscale = Column(Float)
    nummentions = Column(Integer)
    numsources = Column(Integer)
    numarticles = Column(Integer)
    avgtone = Column(Float)
    sourceurl = Column(Text)

    # SERIALIZE: to help with JSON
    @property
    def serialize(self):
        '''
        Returns object data in JSON format.
        '''
        return {
            'event id': self.globaleventid,
            'date': self.date,
            'actor1 name': self.actor1name,
            'actor2 name': self.actor2name,
            'event code': self.eventcode,
            'quad class': self.quadclass,
            'goldstein scale': self.goldsteinscale,
            'num mentions': self.nummentions,
            'num sources': self.nummentions,
            'num articles': self.numarticles,
            'avg tone': self.avgtone,
            'source url': self.sourceurl
        }


class PresidentPos(Base):
    '''
    Class to represent 'pres_positive_high' table.
    '''
    __tablename__ = 'pres_positive_high'

    globaleventid = Column(Integer, primary_key=True)
    date = Column(Date, primary_key=True)
    actor1name = Column(Text, primary_key=True)
    actor2name = Column(Text)
    eventcode = Column(Text)
    quadclass = Column(Integer)
    goldsteinscale = Column(Float)
    nummentions = Column(Integer)
    numsources = Column(Integer)
    numarticles = Column(Integer)
    avgtone = Column(Float)
    sourceurl = Column(Text)

    @property
    def serialize(self):
        '''
        Returns object data in JSON format.
        '''
        return {
            'event id': self.globaleventid,
            'date': self.date,
            'actor1 name': self.actor1name,
            'actor2 name': self.actor2name,
            'event code': self.eventcode,
            'quad class': self.quadclass,
            'goldstein scale': self.goldsteinscale,
            'num mentions': self.nummentions,
            'num sources': self.nummentions,
            'num articles': self.numarticles,
            'avg tone': self.avgtone,
            'source url': self.sourceurl
        }


class PresidentNeg(Base):
    '''
    Class to represent 'pres_negative_high' table.
    '''
    __tablename__ = 'pres_negative_high'

    globaleventid = Column(Integer, primary_key=True)
    date = Column(Date, primary_key=True)
    actor1name = Column(Text, primary_key=True)
    actor2name = Column(Text)
    eventcode = Column(Text)
    quadclass = Column(Integer)
    goldsteinscale = Column(Float)
    nummentions = Column(Integer)
    numsources = Column(Integer)
    numarticles = Column(Integer)
    avgtone = Column(Float)
    sourceurl = Column(Text)

    @property
    def serialize(self):
        '''
        Returns object data in JSON format.
        '''
        return {
            'event id': self.globaleventid,
            'date': self.date,
            'actor1 name': self.actor1name,
            'actor2 name': self.actor2name,
            'event code': self.eventcode,
            'quad class': self.quadclass,
            'goldstein scale': self.goldsteinscale,
            'num mentions': self.nummentions,
            'num sources': self.nummentions,
            'num articles': self.numarticles,
            'avg tone': self.avgtone,
            'source url': self.sourceurl
        }


class Police(Base):
    '''
    Class to represent 'police' table.
    '''
    __tablename__ = 'police'

    GlobalEventID = Column(Integer, primary_key=True)
    Date = Column(Date, primary_key=True)
    Day = Column(Integer)
    Month = Column(Integer)
    Year = Column(Integer)
    Actor1Code = Column(Text)
    Actor1Name = Column(Text)
    Actor2Code = Column(Text)
    Actor2Name = Column(Text)
    IsRootEvent = Column(Boolean)
    EventCode = Column(Text)
    EventBaseCode = Column(Text)
    EventRootCode = Column(Text)
    QuadClass = Column(Integer)
    GoldsteinScale = Column(Float)
    NumMentions = Column(Integer)
    NumSources = Column(Integer)
    NumArticles = Column(Integer)
    AvgTone = Column(Float)
    Actor1Geo_Type = Column(Integer)
    Actor1Geo_FullName = Column(Text)
    Actor1Geo_CountryCode = Column(Text)
    Actor2Geo_Type = Column(Integer)
    Actor2Geo_FullName = Column(Text)
    Actor2Geo_CountryCode = Column(Text)
    Actor1Geo_Lat = Column(Text)
    Actor1Geo_Long = Column(Text)
    Actor2Geo_Lat = Column(Text)
    Actor2Geo_Long = Column(Text)
    SourceURL = Column(Text)

    @property
    def serialize(self):
        return {
            'event id': self.GlobalEventID,
            'date': self.Date,
            'actor1 name': self.Actor1Name,
            'actor2 name': self.Actor2Name,
            'event code': self.EventCode,
            'quad class': self.QuadClass,
            'goldstein scale': self.GoldsteinScale,
            'num mentions': self.NumMentions,
            'num articles': self.NumArticles,
            'avg tone': self.AvgTone,
            'actor1geo fullname': self.Actor1Geo_FullName,
            'actor2geo fullname': self.Actor2Geo_FullName,
            'source url': self.SourceURL
        }


class PoliceNeg(Base):
    '''
    Class to represent 'police_neg_high' table.
    '''
    __tablename__ = 'police_neg_high'

    GlobalEventID = Column(Integer, primary_key=True)
    Date = Column(Date, primary_key=True)
    Day = Column(Integer)
    Month = Column(Integer)
    Year = Column(Integer)
    Actor1Code = Column(Text)
    Actor1Name = Column(Text)
    Actor2Code = Column(Text)
    Actor2Name = Column(Text)
    IsRootEvent = Column(Boolean)
    EventCode = Column(Text)
    EventBaseCode = Column(Text)
    EventRootCode = Column(Text)
    QuadClass = Column(Integer)
    GoldsteinScale = Column(Float)
    NumMentions = Column(Integer)
    NumSources = Column(Integer)
    NumArticles = Column(Integer)
    AvgTone = Column(Float)
    Actor1Geo_Type = Column(Integer)
    Actor1Geo_FullName = Column(Text)
    Actor1Geo_CountryCode = Column(Text)
    Actor2Geo_Type = Column(Integer)
    Actor2Geo_FullName = Column(Text)
    Actor2Geo_CountryCode = Column(Text)
    Actor1Geo_Lat = Column(Text)
    Actor1Geo_Long = Column(Text)
    Actor2Geo_Lat = Column(Text)
    Actor2Geo_Long = Column(Text)
    SourceURL = Column(Text)

    @property
    def serialize(self):
        return {
            'event id': self.GlobalEventID,
            'date': self.Date,
            'actor1 name': self.Actor1Name,
            'actor2 name': self.Actor2Name,
            'event code': self.EventCode,
            'quad class': self.QuadClass,
            'goldstein scale': self.GoldsteinScale,
            'num mentions': self.NumMentions,
            'num articles': self.NumArticles,
            'avg tone': self.AvgTone,
            'actor1geo fullname': self.Actor1Geo_FullName,
            'actor2geo fullname': self.Actor2Geo_FullName,
            'source url': self.SourceURL
        }


class PolicePos(Base):
    '''
    Class to represent 'police_pos_high' table.
    '''
    __tablename__ = 'police_pos_high'

    GlobalEventID = Column(Integer, primary_key=True)
    Date = Column(Date, primary_key=True)
    Day = Column(Integer)
    Month = Column(Integer)
    Year = Column(Integer)
    Actor1Code = Column(Text)
    Actor1Name = Column(Text)
    Actor2Code = Column(Text)
    Actor2Name = Column(Text)
    IsRootEvent = Column(Boolean)
    EventCode = Column(Text)
    EventBaseCode = Column(Text)
    EventRootCode = Column(Text)
    QuadClass = Column(Integer)
    GoldsteinScale = Column(Float)
    NumMentions = Column(Integer)
    NumSources = Column(Integer)
    NumArticles = Column(Integer)
    AvgTone = Column(Float)
    Actor1Geo_Type = Column(Integer)
    Actor1Geo_FullName = Column(Text)
    Actor1Geo_CountryCode = Column(Text)
    Actor2Geo_Type = Column(Integer)
    Actor2Geo_FullName = Column(Text)
    Actor2Geo_CountryCode = Column(Text)
    Actor1Geo_Lat = Column(Text)
    Actor1Geo_Long = Column(Text)
    Actor2Geo_Lat = Column(Text)
    Actor2Geo_Long = Column(Text)
    SourceURL = Column(Text)

    @property
    def serialize(self):
        return {
            'event id': self.GlobalEventID,
            'date': self.Date,
            'actor1 name': self.Actor1Name,
            'actor2 name': self.Actor2Name,
            'event code': self.EventCode,
            'quad class': self.QuadClass,
            'goldstein scale': self.GoldsteinScale,
            'num mentions': self.NumMentions,
            'num articles': self.NumArticles,
            'avg tone': self.AvgTone,
            'actor1geo fullname': self.Actor1Geo_FullName,
            'actor2geo fullname': self.Actor2Geo_FullName,
            'source url': self.SourceURL
        }


# CONFIGURATION: Insert at end of file
# Create instance of create_engine class and poitn to database
engine = create_engine(os.environ['DATABASE_URL'])
Base.metadata.create_all(engine)

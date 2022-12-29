from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

engine = create_engine("sqlite:////Users/yuhsichen/Desktop/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(autoload_with = engine)

Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"//api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
        f"start_date format: YYYY.MM.DD<br/>"
        f"end_date format: YYYY.MM.DD"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > year_ago).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_percipitation = []
    for date, prcp in results:
        percipitation_dict = {}
        percipitation_dict["date"] = date
        percipitation_dict["prcp"] = prcp
        all_percipitation.append(percipitation_dict)

    return jsonify(all_percipitation)


@app.route("/api/v1.0/stations")
def station():

    session = Session(engine)
    results = session.query(Station.id, Station.station, Station.name).all()

    session.close()

    station_list = []
    for id, station, name in results:
        station_dict = {}
        station_dict["id"] = id
        station_dict["station"] = station
        station_dict["name"] = name
        station_list.append(station_dict)

    return jsonify(station_list)
    

@app.route("/api/v1.0/tobs")
def temperature():

    session = Session(engine)

    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > year_ago).\
    filter(Measurement.station == "USC00519281").\
    order_by(Measurement.tobs).all()

    session.close()

    temp_list =[]
    for date, tobs in results:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        temp_list.append(temp_dict)
    
    return jsonify(temp_list)


@app.route("/api/v1.0/<start>")
def start(start):
    date_formated = start.replace(".","-")

    session = Session(engine)


    sel = [
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)]

    results = session.query(*sel).\
        filter(Measurement.date > date_formated).all()

    session.close()

    temp_list =[]
    for min, max, avg in results:
        temp_dict = {}
        temp_dict["min"] = min
        temp_dict["max"] = max
        temp_dict["avg"] = avg
        temp_list.append(temp_dict)
    
    return jsonify(temp_list)





@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    start_formated = start.replace(".","-")
    end_formated = end.replace(".","-")
    

    session = Session(engine)


    sel = [
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)]

    results = session.query(*sel).\
        filter(Measurement.date > start_formated).\
        filter(Measurement.date < end_formated).all()

    session.close()

    temp_list =[]
    for min, max, avg in results:
        temp_dict = {}
        temp_dict["min"] = min
        temp_dict["max"] = max
        temp_dict["avg"] = avg
        temp_list.append(temp_dict)
    
    return jsonify(temp_list)







if __name__ == "__main__":
    app.run(debug=True)

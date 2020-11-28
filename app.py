import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# engine = create_engine("sqlite:///D:\Git Hub Repositorie\SQLalchemy-Challenge\Resources\hawaii.sqlite")
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start date<br/>"
        f"/api/v1.0/start date/end date<br/>"
        f"<br/>"
        f"<br/>"
        f"Dates must be entered as YYYY-MM-DD"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)


    # Query date and precipitation from measurment table
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of prcp_date
    prcp_date = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_date.append(prcp_dict)

    return jsonify(prcp_date)



@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query station names from station table
    results = session.query(Station.station).all()

    session.close()

    return jsonify(results)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query station names from station table

        # determines dates used in filter
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date2 = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
    year_before_last_date = dt.date(last_date2.year, last_date2.month, last_date2.day) - dt.timedelta(days=365)

    session.close()

        # determines station used in filter
    active_station = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()
    
    most_active = active_station[0][0]
    
    session.close()

        # Grabs the station, dates, and temp values for the most active station and last year of data
    year_of_data = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= year_before_last_date).\
        filter(Measurement.station == most_active).\
        group_by(Measurement.date).\
        order_by((Measurement.date).desc()).all()
    
    return jsonify(year_of_data)



@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    sel = [func.min(Measurement.tobs), 
        func.round(func.avg(Measurement.tobs),1), 
        func.max(Measurement.tobs),]

    temp_values = session.query(*sel).\
        filter(Measurement.date >= start).all()

    return (jsonify(temp_values))

@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    sel = [func.min(Measurement.tobs), 
        func.round(func.avg(Measurement.tobs),1), 
        func.max(Measurement.tobs),]

    temp_values2 = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    return jsonify(temp_values2)


if __name__ == '__main__':
    app.run(debug=True)

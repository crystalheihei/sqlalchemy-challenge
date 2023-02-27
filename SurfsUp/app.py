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
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route('/')
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]"
    )        
        
        
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation data"""
    
    # Query all precipitation
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-23").all()

    session.close()

    # Convert list to Dictionary
    all_precipitation = []
    for date,prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_precipitation.append(prcp_dict)

    return jsonify(all_precipitation)




@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    
    # Query all stations
    results = session.query(Station.station).\
        order_by(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

        

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    
    # Query all tobs
    results = session.query(Measurement.date, Measurement.prcp, Measurement.tobs).\
        filter(Measurement.date >= "2016-08-23").\
        filter(Measurement.station == 'USC00519281').\
        order_by(Measurement.date).all()

    session.close()

    # Convert list to Dictionary
    all_tobs = []
    for date, prcp, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["prcp"] = prcp
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)
        
         
        
@app.route("/api/v1.0/<start>")
def Start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, avg and max tobs for a start date"""
    
    # Query all start
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()

    session.close()

    # Create a dictionary from the row data and append to a list of start_date_tobs
    all_tobs = []
    for min, avg, max in results:
        tobs_dict = {}
        tobs_dict["min_temp"] = min
        tobs_dict["avg_temp"] = avg
        tobs_dict["max_temp"] = max
        all_tobs.append(tobs_dict) 
        
    return jsonify(all_tobs)



        
@app.route("/api/v1.0/<start>/<end>")
def Start_end_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, avg and max tobs for start and end dates"""
    
    # Query all start/end
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()
  
    # Create a dictionary from the row data and append to a list of start_end_tobs
    start_end_tobs = []
    for min, avg, max in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min_temp"] = min
        start_end_tobs_dict["avg_temp"] = avg
        start_end_tobs_dict["max_temp"] = max
        start_end_tobs.append(start_end_tobs_dict) 
    

    return jsonify(start_end_tobs)       


if __name__ == '__main__':
    app.run(debug=True)
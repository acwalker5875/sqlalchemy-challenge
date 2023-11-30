# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__weather__)



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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Convert the query results from your precipitation analysis to a dictionary"""
    
    # Query  data
    date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= date).all()

    session.close()
    
    # Create a dictionary from the row data
    precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)

    
@app.route("/api/v1.0/stations")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all stations
    station_list = session.query(func.distinct(Station.station)).all()

    session.close()
    
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query the dates and temperature observations of the most-active station for the previous year of data.
    date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs) \
    .filter(Measurement.station == station_id, Measurement.date >= date) \
    .all()

    """Return a JSON list of temperature observations for the previous year"""
    
    session.close()
    
    return jsonify(results)

@app.route("/api/v1.0/<start>")
def names():
    #Define Start date
    start_date = dt.date(2016, 8, 23) 
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date."""
    # Get unique station IDs
    unique_station_ids = session.query(Station.station).distinct().all()

    # Loop through each station ID and calculate TMIN, TAVG, and TMAX
    for station_id, in unique_station_ids:
        results = session.query(func.min(Measurement.tobs).label('TMIN'),
                            func.max(Measurement.tobs).label('TMAX'),
                            func.avg(Measurement.tobs).label('TAVG')) \
                    .filter(Measurement.station == station_id) \
                    .filter(Measurement.date >= start_date).first()

    session.close()
    
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def names():
    
    #Define start and end dates
    start_date = dt.date(2015, 8, 23) 
    end_date = dt.date(2016, 8, 23)
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive."""
    # Get unique station IDs
    unique_station_ids = session.query(Station.station).distinct().all()

    # Loop through each station ID and calculate TMIN, TAVG, and TMAX
    for station_id, in unique_station_ids:
        results = session.query(func.min(Measurement.tobs).label('TMIN'),
                            func.max(Measurement.tobs).label('TMAX'),
                            func.avg(Measurement.tobs).label('TAVG')) \
                    .filter(Measurement.station == station_id) \
                    .filter(Measurement.date >= start_date)\
                    .filter(Measurement.date <= end_date).first()

    session.close()
    
    return jsonify(results)
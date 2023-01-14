import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify,request, render_template


# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement= Base.classes.measurement
Station = Base.classes.station


# Flask Setup
app = Flask(__name__)


# Flask Routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"  
    )


# add a precipitation route that returns json with the date as the key and the value as the precipitation

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create a session (link) from Python to the DB
    session = Session(engine)
    
    # Query measurement table to get desired columns in variable names
    results = session.query(Measurement.date,Measurement.prcp).all()

    session.close()

    # Create a dictionary with requisite data for date and precipitation
    
    all_results = []
    for date,prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_results.append(prcp_dict)
    
    return jsonify(all_results)

    # Jsonified precipitation data for only the last year in the database 
    
    result_oneyear = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= dt.date(2016,8,23)).filter(Measurement.date <= dt.date(2017,8,23)).all()
    one_year =[]
    
    for date,prcp in result_oneyear:
        prcp_dict_year = {}
        prcp_dict_year["date"] = date
        prcp_dict_year["prcp"] = prcp
        one_year.append(prcp_dict_year)
    return jsonify(one_year)


# Add a stations route that returns jsonified data of all of the stations in the database

@app.route("/api/v1.0/station")
def station():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query stations data to get staion data 
    station_results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()
    
    station_results_all = []
    for station,name,latitude,longitude,elevation in station_results:
        station_dict = {}
        station_dict["Id"] = station
        station_dict["Name"] = name
        station_dict["Latutude"] = latitude
        station_dict["Longitude"] = longitude
        station_dict["Elevation"] = elevation
        station_results_all.append(station_dict)

    return jsonify(station_results_all)

# Add a tobs route that returns jsonified data for the most active station (USC00519281) 
@app.route("/api/v1.0/tobs")
def tobs():

# Create a session (link) from Python to the DB
    session = Session(engine)
    
    # query to find most active station
    active_stations= session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    most_active = active_stations[0][0]
    # return most_active
    
    tobs_mostactive = session.query(Measurement.station,Measurement.date,Measurement.tobs).filter(Measurement.station == most_active).all()
    tobs_results = []
    for station,date,tobs in tobs_mostactive:
        tobs_dict = {}
        tobs_dict["Station"] = station
        tobs_dict["Date"] = date
        tobs_dict["Temperature"] = tobs
       
        tobs_results.append(tobs_dict)
        
    # return jsonify(tobs_results)

    # Only returns the jsonified data for the last year of data 
    temp_data=session.query(Measurement.station,Measurement.date,Measurement.tobs).filter(Measurement.date >= dt.date(2016,8,18)).filter(Measurement.date <= dt.date(2017,8,18)).all()
    tobs_oneyear = []
    for station,date,tobs in temp_data:
        temp_dict = {}
        temp_dict["Station"] = station
        temp_dict["Date"] = date
        temp_dict["Temperature"] = tobs
       
        tobs_oneyear.append(temp_dict)
        
    return jsonify(tobs_oneyear)

@app.route("/api/v1.0/start/<start_date>")
def start(start_date):
    session = Session(engine)
    date_test = session.query(Measurement.date).filter(Measurement.date == start).distinct().all()
 
    # create a list of values to extract
    sel=[
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)
    ]


    # query for dates after start date provided
    temperature = session.query(*sel).filter(Measurement.date>=start).all()
    result = list(np.ravel(temperature))

    try:
        return jsonify(result)
    except: jsonify({"error": f" Date {start} not found"}),404    

if __name__ == '__main__':
    app.run(debug=True)

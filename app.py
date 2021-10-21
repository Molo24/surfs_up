# Date, NumPy and Pandas dependencies
import datetime as dt
import numpy as np
import pandas as pd

# SQLAlchemy Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Flask dependencies
from flask import Flask, jsonify

####
#### Set up the Database
####
# Setup the connection to the SQLite database
# The create_engine() function allows us to access and query our SQLite database file.
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into our classes.
Base = automap_base()

# Add Base.prepare() function to reflect the reflect the tables into SQLAlchemy.
Base.prepare(engine, reflect=True)

# With the database reflected, we can save our references to each table.
# Create a variable for each of the classes so that we can reference them later.
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link from Python to our database
session = Session(engine)

####
#### Set up Flask
####
# Define Flask app
app = Flask(__name__)

####
#### Creating Flask Route
####
# Our first task when creating a Flask route is to define what our route will be.
# We want our welcome route to be the root, which in our case is essentially the homepage.
# All of your routes should go after the app = Flask(__name__) line of code.

####
#### Define the Welcome/Root route
####
# First, we need to define the starting point, also known as the root.
# The forward slash inside of the app.route denotes that we want to put our data at the root of our routes.
# The forward slash is commonly known as the highest level of hierarchy in any computer system.
@app.route("/")

# The next step is to add the routing information for each of the other routes.
# For this we'll create a function, and our return statement will have f-strings as a reference to all of the other routes.
# This will ensure our investors know where to go to view the results of our data.

# Create a function welcome() with a return statement. 
# And add the precipitation, stations, tobs, and temp routes that we'll need for this module into our return statement.
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API <br>
    Available Routes: <br>
    /api/v1.0/precipitation <br>
    /api/v1.0/stations <br>
    /api/v1.0/tobs <br>
    /api/v1.0/temp/start/end
    
    ''')

# When creating routes, we follow the naming convention /api/v1.0/ followed by the name of the route.
# This convention signifies that this is version 1 of our application.
# This line can be updated to support future versions of the app as well.

####
#### Precipitation Route
####
# Every time you create a new route, your code should be aligned to the left in order to avoid errors.
@app.route("/api/v1.0/precipitation")

# Create the precipitation() function.
# Add the line of code that calculates the date one year ago from the most recent date in the database.
# Write a query to get the date and precipitation for the previous year.
# Finally, we'll create a dictionary with the date as the key and the precipitation as the value.
## To do this, we will "jsonify" our dictionary.
##  Jsonify() is a function that converts the dictionary to a JSON file.
##
##  JSON files are structured text files with attribute-value pairs and array data types.
##  They have a variety of purposes, especially when downloading information from the internet through API calls.
##  We can also use JSON files for cleaning, filtering, sorting, and visualizing data, among many other tasks.
##  When we are done modifying that data, we can push the data back to a web interface, like Flask.
##
##  We'll use jsonify() to format our results into a JSON structured file.
##  When we run this code, we'll see what the JSON file structure looks like.

def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# You will need to navigate to the precipitation route in order to see the output of your code.
# You can do this by adding api/v1.0/precipitation to the end of the web address.

####
#### Station Route
####
# Begin by defining the route and route name.
@app.route("/api/v1.0/stations")

# Create a query that will allow us to get all of the stations in our database.
# We want to start by unraveling our results into a one-dimensional array.
#  To do this, we want to use the function np.ravel(), with results as our parameter.
# Next, we will convert our unraveled results into a list.
#  To convert the results to a list, we will need to use the list function, which is list(), and then convert that array into a list.
# Then we'll jsonify the list and return it as JSON.
#  You may notice here that to return our list as JSON, we need to add stations=stations.
#  This formats our list into JSON.

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

####
#### Monthly Temperature Route
####
# Define the route (" temperature observations")
@app.route("/api/v1.0/tobs")

# Calculate the date one year ago from the last date in the database.
# Query the primary station for all the temperature observations from the previous year.
# Unravel the results into a one-dimensional array and convert that array into a list.
# Jsonify the list and return our results
# 

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

####
#### Statistics Route
####
# Define the route - need to provide both a starting and ending date
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# Add parameters to our stats()function: a start parameter and an end parameter.
# Create a query to select the minimum, average, and maximum temperatures from our SQLite database.
#  We'll start by just creating a list called sel
#   In the following code, take note of the asterisk in the query next to the sel list.
#   Here the asterisk * is used to indicate there will be multiple results for our query: minimum, average, and maximum temperatures.
# Since we need to determine the starting and ending date, add an if-not statement to our code.
#  This will help us accomplish a few things.
#   We'll need to query our database using the list sel that we just made.
#   Then, we'll unravel the results into a one-dimensional array and convert them to a list.
#   Finally, we will jsonify our results and return them.


def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
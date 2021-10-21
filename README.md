# Surfs_Up Temperature Summary with SQLite & SQLAlchemy

## Overview & Purpose
The purpose of the assignment was to use an existing SQLite data file that contains temperature data from various points around the island of Oahu. Parsing the dataset, the goal was to create descriptive statistics of temperature measurements from the months of June and December.

In order to accomplish the analysis the following tools were used:
* Jupyter Notebook
* Python
* SQLite data file
* Dependencies:
  * numpy
  * pandas
  * sqlalchemy
  * datetime
 
 First, explored the dataset:
 ```
# Pull tables in SQLite file
inspector = inspect(engine)
inspector.get_table_names()
['measurement', 'station']

# Get a list of column names and types
m_columns = inspector.get_columns('measurement')
for c in m_columns:
    print(c['name'], c["type"])
id INTEGER
station TEXT
date TEXT
prcp FLOAT
tobs FLOAT
```

Next, explored the Measurement table:
```
engine.execute('SELECT * FROM measurement LIMIT 10').fetchall()
[(1, 'USC00519397', '2010-01-01', 0.08, 65.0),
 (2, 'USC00519397', '2010-01-02', 0.0, 63.0),
 (3, 'USC00519397', '2010-01-03', 0.0, 74.0),
 (4, 'USC00519397', '2010-01-04', 0.0, 76.0),
 (5, 'USC00519397', '2010-01-06', None, 73.0),
 (6, 'USC00519397', '2010-01-07', 0.06, 70.0),
 (7, 'USC00519397', '2010-01-08', 0.0, 64.0),
 (8, 'USC00519397', '2010-01-09', 0.0, 68.0),
 (9, 'USC00519397', '2010-01-10', 0.0, 73.0),
 (10, 'USC00519397', '2010-01-11', 0.01, 64.0)]
 ```
 
 Isolated the June and December data into lists
 ```
june_temps = session.query(Measurement.tobs).\
    filter(func.strftime("%m", Measurement.date) == june_month_string).all()
 
 dec_temps = session.query(Measurement.tobs).\
    filter(func.strftime("%m", Measurement.date) == dec_month_string).all()
```

Lastly, moved the lists into DataFrames and performed ```describe()```
```
june_temps_df = pd.DataFrame(june_temps, columns=["june_temperature"])
dec_temp_df = pd.DataFrame(dec_temps, columns=["dec_temperature"])

june_temps_df.describe()
dec_temp_df.describe()
```
## Results

From the result tables below we can see some interesting facts about the June & December temperatures of Oahu:
1) The max are very close at 85 (June) and 83 (December)
2) The distance between the Q1, Q2 and Q3 values for each month is very close
3) Despite how close most of the results are between June and Dec, the min for Dec (56) is well below the min for June (64).

![june_temps_describe](https://user-images.githubusercontent.com/89284280/138193103-f66b5d75-d5bd-4bd2-9b26-c27d930ce378.PNG)

![dec_temps_describe](https://user-images.githubusercontent.com/89284280/138193106-16ba8960-1aae-4a42-8e80-6701f82cee77.PNG)

Of note, performing ```.median()``` on the June and December DataFrames shows a median of 75 (June) and 71 (Dec). These values are are very close to their means, which suggests the dataset is symetrical for both months.

## Conclusion
Overall, the temperature fluctuations between June and December are pretty minimal. However, the island of Oahu is not small and is not flat. For a deeper analysis it would be intersting to group the temperature results by station. Next, it would make sense to join the ```measurement``` table with the ```station``` table from which one could plot the stations on the map using the Lat and Long of the data set. Perhaps there is more variation in the temperatures based geolocation (and elevation). The analysis above gives a good overview of expected aggregated average temperature of Oahu, but a deeper analysis on geolocation would be worthwhile.







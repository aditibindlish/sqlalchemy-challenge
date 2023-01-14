# sqlalchemy-challenge
Analysing sql database in python using SQL Alchemy and Flask API to create routes in server
Used the provided database, hawaii.sqlite to query and analyse data in python 

used  create_engine() function to connect to the database everytime, then using automap_base() function to reflect the tables into python classes and the references to the classes named station and measurement were saved in same name variables. Further Python was linked to the database by creating a SQLAlchemy session using Session.engine

various queries were run to anlayse the precipitation and temperature data from different stations in hawaii and the resulting data was stored in pythom dataframes and then plotted using pd.plot function. 

we found the most active station as well in Hawaii, i.e. station which had maximum observations and the summary stats for this station.

Flask API was used to display data in the browser. Jsonify function was used to display it in a readable manner.  

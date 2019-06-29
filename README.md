# Porting Pulse 

A dashboard I made for showcasing metrics. 

## Basic outline:

1. Base data is pulled from Metabase SQL database using **Psycopg2**
2. Base data is cleaned, and manipulated using Python
3. Cleaned data is organized and stored in my local **PostGreSQL** database using **Psycopg2**
4. Stored data is transferred to **Flask** dashboard via **flask_sqlalchemy** and **SQLAlchemy**  
5. **Flask** data is manipulated and displayed on **Flask** dashboard using **Pandas** and **Charts.js**

The dashboard also supports report generation for all “general” and “VIP” customer data on a year to date scale using **xlsxwriter** and **Flask**'s send file function.

![Alt Text](https://github.com/it-avenger/FWR-Porting-Pulse/blob/master/flask-pp/flask_PP/static/demo-gif.gif)

### *Disclaimer*: All numbers and names represented in the GIF above do NOT reflect any accurate business information, metrics or names associated with Flowroute LLC or any of it's customers. 
### This is a local build with names subsituted for masks and ALL metrics shown are pulled from my testing database.



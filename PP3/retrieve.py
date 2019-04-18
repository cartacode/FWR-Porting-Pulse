from credentials import REDSHIFT_SETTINGS
from credentials import pg_sql

import datetime
from collections import Counter

import psycopg2 as pg2
from psycopg2 import sql
import numpy as np 
import pandas as pd

"""
===GET BASE DATA FROM REDSHIFT/METABASE===
"""

def redshift_connector():
    """connect to redshift using credentials.py"""

    try:
      conn = pg2.connect(host=REDSHIFT_SETTINGS['HOST'],
                  port=REDSHIFT_SETTINGS['PORT'],
                  database=REDSHIFT_SETTINGS['DATABASE_NAME'],
                  user=REDSHIFT_SETTINGS['USERNAME'],
                  password=REDSHIFT_SETTINGS['PASSWORD'],
                  connect_timeout=5)
      return conn
    except:
      print("Redshift is busted. Check VPN")

def get_wildcard():
    """find range of days from/including last saturday to this past sunday"""
    
    today = datetime.date.today()
    idx = (today.weekday() + 1) 
    sun = today - datetime.timedelta(7+idx)

    date = [(sun + datetime.timedelta(day)) for day in range(0,7)] 
    date_range = [x for x in date]
    return date_range

def get(wildcard, query):
    """get our query from redshift/metabase"""

    conn = redshift_connector()
    rs_cur = conn.cursor()
    rs_cur.execute(sql.SQL(query), (wildcard,))
    row = rs_cur.fetchall()
    result = ([i for i in row])
    rs_cur.close
    result = tuple(result)
    return result

def count():
    query = """
SELECT "public"."trunking_portorder"."id" AS "id", "public"."trunking_portorder"."customer_id" AS "customer_id"
FROM "public"."trunking_portorder"
WHERE CAST("public"."trunking_portorder"."date_created" AS date) = %s
GROUP BY "public"."trunking_portorder"."id", "public"."trunking_portorder"."customer_id"
ORDER BY "public"."trunking_portorder"."id" ASC, "public"."trunking_portorder"."customer_id" """
    
    port_count = 0
    vip_dict = {26193:0,20193:0,59775:0,58:0,38640:0,52284:0,47037:0}

    date_range = get_wildcard()
    for date in date_range: #for each day in week, set SQL wildcard to date and run query for that date
        wildcard = date
        for pon,uid in get(wildcard, query):
          port_count += 1
          if uid in vip_dict:
            vip_dict[uid] += 1
    return port_count,vip_dict

"""
===RECORD AND SAVING RESULTS BEGINS HERE===
"""

def pgsql_connector():
    """connect to postgresql DB """

    try:
        local_conn = pg2.connect(database = pg_sql['db_name'], user = pg_sql['postgres_user'], password = pg_sql['postgres_pw'])
        return local_conn
    except:
        "Local DB Connection is busted. **Investigate**"

def find_month():
    """find month string and for inputting data into SQL table"""

    month_range = get_wildcard() #re-call our weekly date range
    month_range = [i.strftime('%m') for i in month_range]
    c = Counter(month_range) #determine month by most common month entry in month_range
    month = str(c.most_common(1))[3:5]
    month_dict = {'01': 'January', '02': 'Feburary', '03': 'March', '04': 'April', 
                    '05': 'May', '06': 'June', '07': 'July', '08': 'August', '09': 'September', 
                    '10': 'October', '11': 'November', '12': 'December'}
    return month_dict[month]

def find_week(month):
    """locate our input week"""
    
    conn = pgsql_connector()

    df = pd.read_sql("SELECT * FROM test_pp", con=conn)
    df = df[df['month_name']==f'{month}']

    week_columns = [columns for columns in df if "week" in columns]
    for each in week_columns:
        if (df[each].values) == 0:
            return each
        else:
            ('**ERROR**-PLEASE CHECK MONTHS AND WEEKS IN SQL TABLE**')

def insert_weekly(port_count, vip_dict):
    """commit general weekly data into our local DB using pg2 SQLqueries"""

    conn = pgsql_connector()
    cur = conn.cursor()
    
    month = find_month()
    week = find_week(month)

    cur.execute(sql.SQL("UPDATE test_pp SET {} = %s WHERE month_name = %s").format(sql.Identifier(week)),(port_count,month,))
    conn.commit() #^^set weekly count

    query = """UPDATE test_pp SET month_total = month_total + (%s) WHERE month_name = (%s)"""
    cur.execute(query,(port_count,month,))
    conn.commit() #^^update month to date county

    query = """UPDATE test_pp SET ytd = (SELECT SUM(month_total) FROM test_pp) WHERE month_name = (%s)"""
    cur.execute(query,(month,))
    conn.commit() #^^update yearly count
    
    db_names_list = ['vow26193', 'weave20193', 'expectel59775','zang58', 'zen38640', 'signalwire52284','intulse47037']
    vip_val_list = list(vip_dict.values()) #convert to list of the values so match with DB names

    for dbname,vip_val in zip(db_names_list,vip_val_list): #insert values from vip_dict 
        cur.execute(sql.SQL("UPDATE test_vip SET {} = {} + %s WHERE month_name = %s;").format(sql.Identifier(dbname),sql.Identifier(dbname)),(vip_val,month,))   
    
    conn.commit()
    conn.close()

port_count,vip_dict = count()
insert_weekly(port_count, vip_dict)
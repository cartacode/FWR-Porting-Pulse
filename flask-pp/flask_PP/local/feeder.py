import datetime
from collections import Counter
import psycopg2 as pg2
from psycopg2 import sql

from credentials import REDSHIFT_SETTINGS
from credentials import pg_sql
import vip_ids

"""
===GET COUNT DATA FROM REDSHIFT/METABASE===
"""

def redshift_connector():

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

def get_week_range(): #Count query range weekly last Sun to this Sat

    today = datetime.date.today()
    idx = (today.weekday() + 1) 
    sun = today - datetime.timedelta(7+idx)
    date_range = [(sun + datetime.timedelta(day)) for day in range(0, 7)] 
    return date_range

def count_query(wildcard): # Query returns PONs and UIDs for each order
    
    query = """
SELECT "public"."trunking_portorder"."id" AS "id", "public"."trunking_portorder"."customer_id" AS "customer_id"
FROM "public"."trunking_portorder"
WHERE CAST("public"."trunking_portorder"."date_created" AS date) = %s
GROUP BY "public"."trunking_portorder"."id", "public"."trunking_portorder"."customer_id"
ORDER BY "public"."trunking_portorder"."id" ASC, "public"."trunking_portorder"."customer_id" """ 
    conn = redshift_connector()
    rs_cur = conn.cursor()
    rs_cur.execute(sql.SQL(query), (wildcard,))
    row = rs_cur.fetchall()
    result = ([i for i in row])
    rs_cur.close
    return tuple(result)

def get_count(): # Run query for each day in range and get our counts

    port_count = 0
    vip_dict = vip_ids.uids
    date_range = get_week_range()
    for date in date_range: #For each day in week, set SQL wildcard to date and run query for that date
        wildcard = date
        for pon, uid in count_query(wildcard):
          port_count += 1
          if uid in vip_dict:
            vip_dict[uid] += 1
    return port_count, vip_dict
    
"""
===GET 'ADVANCED' DATA FROM REDSHIFT/METABASE===
"""

def get_year_range(): # Find all dates star of year to today
    
    today = datetime.date.today()
    start_date = datetime.date(2019, 1, 1)
    diff = abs((start_date - today).days)+1 # Plus 1 for range
    date_range = [(today - datetime.timedelta(day)) for day in range(0, diff)] 
    return date_range

def get(wildcard, flag=True):
    """
    Run both our queries and return results, wildcard = date
    True for completion comp dates, False for CRDs
    """

    conn = redshift_connector()
    rs_cur = conn.cursor()
    if flag:
        query = """
        SELECT "public"."trunking_portorder"."date_created" AS "date_created","public"."trunking_portorder"."completion_date" AS "completion_date"
FROM "public"."trunking_portorder"
WHERE CAST("public"."trunking_portorder"."date_created" AS date) = CAST(%s AS date)
"""  
    else: 
        query ="""
    SELECT "public"."trunking_portorder"."desired_completion_date" AS "CRD","public"."trunking_portorder"."completion_date" AS "completion_date"
FROM "public"."trunking_portorder"
WHERE CAST("public"."trunking_portorder"."date_created" AS date) = CAST(%s AS date)
"""    
    rs_cur.execute(sql.SQL(query), (wildcard,))
    row = rs_cur.fetchall()
    result = ()
    for c, d in row:
        if c != None and d != None:
            result += (c, d)
    rs_cur.close
    return list(result)

def query_cycle(flag):
    """
    Func for running queries for dates and returning list of data for each date
    flag passed from the start of 'get' func
    """
    datelist = []
    for date in get_year_range():
        wildcard = date
        for each in get(wildcard, flag):
            datelist.append(each)
    return datelist

def get_average(): # Calculate average comp time from per date data list

    datelist = query_cycle(flag=True)
    created = datelist[0::2]
    completed = datelist[1::2]
    port_length=[abs((a-b).days) for a, b in zip(created, completed)]
    port_day = [day for day in port_length if day < 365] # Remove anomalies information
    total_days = sum(port_day)
    ports = int(len(datelist)/2)
    return round(total_days/ports, 2)

def get_crd_perc(): # Calculate average CRD hit from per date data list
    
    datelist = query_cycle(flag=False)
    crd = datelist[0::2]
    actual_comp = datelist[1::2]
    crd_diff=[abs((a-b).days) for a,b in zip(crd, actual_comp)]
    score = {'hit': 0, 'total': 0}
    for each in crd_diff:
        if int(each) == 1:
            score['hit'] += 1
            score['total'] += 1
        else:
            score['total'] += 1
    return round(score['hit']/score['total'], 2)

"""
===RECORD AND SAVE RESULTS===
"""

def pgsql_connector():

    try:
        local_conn = pg2.connect(database = pg_sql['db_name'], 
                                user = pg_sql['postgres_user'], 
                                password = pg_sql['postgres_pw'])
        return local_conn
    except:
        return "Local DB Connection is busted. **Investigate**"

def find_month(): # Find what month our save belongs in

    month_range = get_week_range() # Weekly sun-sat range
    month_range = [i.strftime('%m') for i in month_range]
    c = Counter(month_range)
    month = str(c.most_common(1))[3:5]
    month_dict = {'01': 'January', '02': 'Feburary', '03': 'March', '04': 'April', 
                    '05': 'May', '06': 'June', '07': 'July',
                    '08': 'August', '09': 'September', 
                    '10': 'October', '11': 'November', '12': 'December'}
    return month_dict[month]

def find_week(month): # Find correct week in our month to input

    conn = pgsql_connector()
    cur = conn.cursor()
    query = """SELECT week1, week2, week3, week4, week5 FROM _2019_pp WHERE month_name = (%s)"""
    cur.execute(query,(month,))
    get_weeks = cur.fetchall()
    clean_weeks = [i for i in get_weeks[0]]
    week_columns = ['week1', 'week2', 'week3', 'week4', 'week5']
    zip_weeks = tuple(zip(week_columns, clean_weeks))
    for week,quantity in zip_weeks:
        if quantity == 0:
            return week


def insert_sql(port_count, vip_dict, average, crd_perc): # Update and commit data to pgsql table

    month = find_month()
    week = find_week(month)

    conn = pgsql_connector()
    cur = conn.cursor()
    cur.execute(sql.SQL("UPDATE _2019_pp SET {} = %s WHERE month_name = %s").format(sql.Identifier(week)),(port_count,month,))
    conn.commit() #^^ Set weekly count

    query = """UPDATE _2019_pp SET month_total = month_total + (%s) WHERE month_name = (%s)"""
    cur.execute(query,(port_count,month,))
    conn.commit() #^^ Update month to date county

    query = """UPDATE _2019_pp SET ytd = (SELECT SUM(month_total) FROM _2019_pp) WHERE month_name = (%s)"""
    cur.execute(query,(month,))
    conn.commit() #^^ Update yearly count
    
    db_names_list = ['v', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6'] 
    vip_val_list = list(vip_dict.values()) # Convert to list of the values so match with DB names

    for dbname,vip_val in zip(db_names_list,vip_val_list): # Insert values from vip_dict 
        cur.execute(sql.SQL("UPDATE _2019_vip SET {} = {} + %s WHERE month_name = %s;").format(sql.Identifier(dbname),sql.Identifier(dbname)),(vip_val,month,))   
    conn.commit()

    query = """UPDATE _2019_pp SET ytd_comp_time = %s WHERE month_name = %s;"""
    cur.execute(query,(average,month,)) #^^ Update ytd completion time
    conn.commit()

    query = """UPDATE _2019_pp SET month_crd_hit = %s WHERE month_name = %s;"""
    cur.execute(query,(crd_perc,month,)) #^^ Update ytd CRD%
    conn.commit()
    conn.close()

def main():

    port_count,vip_dict = get_count() # Get week count, vip week count
    average = get_average() # Get ytd average comp time
    crd_perc = get_crd_perc() # Get ytd CRD%
    insert_sql(port_count, vip_dict, average, crd_perc) # Update and save all data
    
if __name__ == "__main__":
    main()
from credentials import REDSHIFT_SETTINGS
import datetime
import psycopg2
from psycopg2 import sql
from tqdm import tqdm
import credentials

def redshift_connector():
    """connect to redshift using credentials.py"""

    try:
      conn = psycopg2.connect(host=REDSHIFT_SETTINGS['HOST'],
                  port=REDSHIFT_SETTINGS['PORT'],
                  database=REDSHIFT_SETTINGS['DATABASE_NAME'],
                  user=REDSHIFT_SETTINGS['USERNAME'],
                  password=REDSHIFT_SETTINGS['PASSWORD'],
                  connect_timeout=5)
      return conn
    except:
      print("Redshift busted af. You on the VPN?")

def diff_get():
    """get amount of days from beggining of year til today"""

    end_date = datetime.date.today()#today
    start_date = datetime.date(2019, 1, 1)#beginning of year
    return start_date, abs((start_date - end_date).days)#amount of days between beginning of year and today

def get(wildcard):
    """get our query from redshift/metabase"""

    conn = redshift_connector()
    rs_cur = conn.cursor()
    query = """
    SELECT "public"."trunking_portorder"."date_created" AS "date_created","public"."trunking_portorder"."completion_date" AS "completion_date"
FROM "public"."trunking_portorder"
WHERE CAST("public"."trunking_portorder"."date_created" AS date) = CAST(%s AS date)
"""  
    rs_cur.execute(sql.SQL(query), (wildcard,))
    row = rs_cur.fetchall()
    result = ()
    for c,d in row:
        if c != None and d != None:
            result += (c,d)
    rs_cur.close
    result = list(result)
    return result


def get_wildcard(diff,start_date):
    """get our wildcard variable for query"""
    
    date_range=[]
    counter = 0
    while counter <= int(diff): #run until current day (diff and start date determined in 'if __name__')
        date_range.append(start_date) 
        start_date += datetime.timedelta (days = 1) #increase day by one
        counter += 1
    return date_range

def get_average(datelist):
    """get our average fromq queried list"""

    created = datelist[0::2] #creation dates
    completed = datelist[1::2] #completion dates
    port_length=[abs((a-b).days) for a,b in zip(created, completed)]
    port_day = [day for day in port_length if day<365] #remove some anomolous information
    
    total_days = sum(port_day)
    ports = int(len(datelist)/2)  #ports number is count of our creation and completion dates divided by two
    return round(total_days/ports, 2)


def insert_sql(avg,select_month): #select_month is passed from main.py version ONLY WORKS in connection with main.py
    """add our data to our tracking database"""

    conn = psycopg2.connect(database = credentials.db_name, user = credentials.postgres_user, password = credentials.postgres_pw)
    cur = conn.cursor()
    query = """
    UPDATE p_p SET ytd_comp_time = %s WHERE month_name = %s;
    """
    variables = (avg,select_month,)
    cur.execute(query,variables)
    conn.commit()
    conn.close()

def main(select_month): #this version is ONLY FOR USE IN PP, select_month is passed from main.py
    """return average days per S->C for port-ins since begininning of year to today 2019"""
    
    start_date, diff = diff_get()
    datelist = []
    for date in tqdm(get_wildcard(diff,start_date)): #run query for each day (ports created on that day are the ones queried)
        wildcard = date
        for each in get(wildcard):
            datelist.append(each) #append each days queried info to our list
    avg = get_average(datelist)
    insert_sql(avg,select_month)

if __name__ == "__main__":
    main(select_month)
 
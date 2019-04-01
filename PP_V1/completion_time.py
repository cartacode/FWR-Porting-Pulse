from credentials import REDSHIFT_SETTINGS
import psycopg2
import datetime
from psycopg2 import sql
from tqdm import tqdm

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

def get(wildcard, query):

    """get our query from redshift/metabase"""

    conn = redshift_connector()
    rs_cur = conn.cursor()
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

def get_average(datelist,diff):

    """get our average fromq queried list"""

    created = datelist[0::2] #creation dates
    completed = datelist[1::2] #completion dates
    port_length=[abs((a-b).days) for a,b in zip(created, completed)]
    
    port_day = []
    for day in port_length: #remove some anomolous information we will never have starting in ytd over 365 days completion time
        if day<365:         #^^^ one 365260 value in table 
            port_day.append(day)    
    
    total_days = 0 
    for num in port_day: #add up the completion times (in days) from our cleaned list
       total_days +=num 
    
    ports = int(len(datelist)/2)  #ports number is count of our creation and completion dates divided by two

    average_time = total_days/ports

    print(f'Total days:{total_days}\nPorts with completion dates:{ports}')
    print(f'YTD average days per port(weekends included): {round(average_time,3)}')
    return average_time

def main():

    query = """
    SELECT "public"."trunking_portorder"."date_created" AS "date_created","public"."trunking_portorder"."completion_date" AS "completion_date"
FROM "public"."trunking_portorder"
WHERE CAST("public"."trunking_portorder"."date_created" AS date) = CAST(%s AS date)
"""
    
    end_date = datetime.date.today()#today
    start_date = datetime.date(2019, 1, 1)#beginning of year
    diff = abs((start_date - end_date).days)#amount of days between beginning of year and today

    datelist = []
    for date in tqdm(get_wildcard(diff,start_date)): #run query for each day (ports created on that day are the ones queried)
        wildcard = date
        for each in get(wildcard, query):
            datelist.append(each) #append each days queried info to our list
    
    result = get_average(datelist,diff)

    return result

if __name__ == "__main__":
    main()
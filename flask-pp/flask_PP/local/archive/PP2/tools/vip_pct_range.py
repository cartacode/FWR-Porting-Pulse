from credentials import REDSHIFT_SETTINGS
import datetime
from datetime import date
import psycopg2
from psycopg2 import sql
from tqdm import tqdm
import matplotlib.pyplot as plt

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
    result = ([i for i in row])
    rs_cur.close
    result = tuple(result)
    print(result)
    return result

def get_wildcard():
    """get our date_range for query"""
    
    t = datetime.date.today().strftime('%m/%d/%Y') #todays date
    date_format = '%m/%d/%Y' #solve any potential formatting issues
    start = datetime.datetime.strptime('1/1/2018', date_format) #edit here for the end date of your query
    end = datetime.datetime.strptime(t, date_format) #today
    diff = end - start #counter for while loop based on days bewteen 'start' date and today

    counter = 0 #counter for while loop
    date_range = []
    today = datetime.date.today()
    while counter <= int(diff.days): 
        date_range.append(today)
        today -= datetime.timedelta (days = 1)
        counter += 1
    return date_range

def main():
    """run our query for given dates and return pct of ports from 'vips'"""
    
    with open("vip_range.txt", "r") as f: #text file for easy UID manipulation/editing
        uids = f.read()
        uids = uids.split("\n")
        uids = list(filter(None, uids))
    y = 0
    vip_dict = {str(x):y for x in uids}
    query = """
SELECT "public"."trunking_portorder"."id" AS "id", "public"."trunking_portorder"."customer_id" AS "customer_id"
FROM "public"."trunking_portorder"
WHERE CAST("public"."trunking_portorder"."date_created" AS date) = %s
GROUP BY "public"."trunking_portorder"."id", "public"."trunking_portorder"."customer_id"
ORDER BY "public"."trunking_portorder"."id" ASC, "public"."trunking_portorder"."customer_id" """
    port_count = 0 #counters for port-in counts
    vip_count = 0
    date_range = get_wildcard()
    for date in tqdm(date_range): #for each day in week, set SQL wildcard to date and run query for that date
        wildcard = date
        print(f'Date: {wildcard}')
        for pon,uid in get(wildcard, query):
            port_count += 1
            if str(uid) in vip_dict:
                vip_dict[str(uid)] += 1
    for each in vip_dict.values():
        vip_count += int(each)
    perc = (vip_count/port_count)*100
    print(f'VIP count: {vip_count}\nTotal count:{port_count}\n%: {round(perc,2)} ')

if __name__ == "__main__":
    main()
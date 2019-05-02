from credentials import REDSHIFT_SETTINGS
import psycopg2
import datetime
from psycopg2 import sql
from tqdm import tqdm
from porting_pulse import Porting_puls

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

    """get our wildcard variable for query"""
    
    today = datetime.date.today()
    idx = (today.weekday() + 1) % 7#get last sunday
    sun = today - datetime.timedelta(7+idx)
    #get each day sun through sat
    counter = 0
    date_range = []
    while counter <= 6:
        
        date = sun + datetime.timedelta(counter)
        date_range.append(date)
        counter += 1
        
    return date_range

def weekly_short(vip_dict):

    """simple VIP stats from weekly data gather, per request"""

    vip_names = []
    pres_tup = ()

    iter_dict = iter(vip_dict.values())
    for each in vip_names:
      pres_tup += (each, next(iter_dict))
    for item in pres_tup:
      print(f'{item}')

    

if __name__ == "__main__":

    query = """
SELECT "public"."trunking_portorder"."id" AS "id", "public"."trunking_portorder"."customer_id" AS "customer_id"
FROM "public"."trunking_portorder"
WHERE CAST("public"."trunking_portorder"."date_created" AS date) = %s
GROUP BY "public"."trunking_portorder"."id", "public"."trunking_portorder"."customer_id"
ORDER BY "public"."trunking_portorder"."id" ASC, "public"."trunking_portorder"."customer_id" """
    
    port_count = 0
    vip_dict = {}

    date_range = get_wildcard()
    for date in tqdm(date_range): #for each day in week, set SQL wildcard to date and run query for that date
        wildcard = date
        print(f'Date: {wildcard}')
        for pon,uid in get(wildcard, query):
          port_count += 1
          if uid in vip_dict:
            vip_dict[uid] += 1

    p = Porting_puls()
    p.write_um(port_count)       
    p.mtd()
    p.ytd()
    p.write_vip(vip_dict)
    print(f'Past week total: {port_count}\n--\nVIP week totals: ')
    weekly_short(vip_dict)
  
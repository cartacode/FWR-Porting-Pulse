from credentials import REDSHIFT_SETTINGS
import datetime
import psycopg2
from psycopg2 import sql

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
    print(result)
    return result

def get_wildcard():
    """determine what status we want to query"""

    wildcard_dict = {1:'A',2:'R',3:'S',4:'P'}
    while True:
        status = int(input('1. Accepted 2. Rejected 3. Submitted 4. Pending'))
        if status in range(0,5):
            wildcard = wildcard_dict[status]
            print(wildcard)
            break
        else:
            continue
    return wildcard

def main():
 """run our query using wildcar and report uid, pon count in given status"""
    query = """
    SELECT "public"."trunking_portorder"."customer_id" AS "customer_id"
FROM "public"."trunking_portorder"
WHERE "public"."trunking_portorder"."status" = %s
GROUP BY "public"."trunking_portorder"."customer_id"
ORDER BY "public"."trunking_portorder"."customer_id" ASC"""
    wildcard = get_wildcard()
    port_orders = get(wildcard,query)
    counter = 0
    uid = int(input('UID? '))
    for pons in port_orders:
        if uid in pons:
            counter +=1
    print(f'UID: {uid} has {counter} orders in {wildcard}.')

if __name__ == "__main__":
    main()
from credentials import REDSHIFT_SETTINGS
import datetime
import psycopg2
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

def get(wildcard):
    """get our query from redshift/metabase"""

    conn = redshift_connector()
    rs_cur = conn.cursor()

    query = """
    SELECT "public"."trunking_portorder"."desired_completion_date" AS "CRD","public"."trunking_portorder"."completion_date" AS "completion_date"
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
    return list(result)

def datefinder(select_month): #select month is from pp2 main.py, this version is only for PP use

    month_dict = {'January': 1, 'Feburary': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7,
                     'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
    m = month_dict[select_month] #translate select_month into an int for datetime
    end_date = datetime.date.today()#today
    start_date = datetime.date(2019, m, 1)#beginning of the month our report is going off of
    return abs((start_date - end_date).days), start_date#amount of days between beginning of year and today

def get_wildcard(span,start_date):
    """get our wildcard variable for query"""
    
    date_range=[]
    counter = 0
    while counter <= int(span): #run until current day (diff and start date determined in 'if __name__')
        date_range.append(start_date) 
        start_date += datetime.timedelta (days = 1) #increase day by one
        counter += 1
    return date_range

def get_perc(datelist):
    """get our % of completion dates requested hit"""

    crd = datelist[0::2] #requested completions dates
    actual_comp = datelist[1::2] #actual completion dates
    diff=[abs((a-b).days) for a,b in zip(crd, actual_comp)] #difference in days between requested and acutal
    score = {'hit': 0, 'total': 0}
    for each in diff:
        if int(each)==1:
            score['hit'] += 1
            score['total'] += 1
        else:
            score['total'] +=1
    return round(score['hit']/score['total'], 2)
    
def main(select_month):
    """main func ONLY INTENDED FOR USE IN PP find normal version in tools dir"""

    span, start_date = datefinder(select_month) #select month is from main.py
    datelist = []
    for date in tqdm(get_wildcard(span,start_date)): #run query for each day (ports crd on that day are the ones queried)
        wildcard = date
        for each in get(wildcard):
            datelist.append(each) #append each days queried info to our list
    return get_perc(datelist)
    
if __name__ == "__main__":
    main(select_month)
 
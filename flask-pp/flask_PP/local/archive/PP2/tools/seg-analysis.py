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
      print("Redshift is busted. You on the VPN?")

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

def get_wildcard():
    """get our date_range for query"""
    
    t = datetime.date.today().strftime('%m/%d/%Y') #todays date
    date_format = '%m/%d/%Y' #solve any potential formatting issues
    start = datetime.datetime.strptime('1/1/2016', date_format) #start date
    end = datetime.datetime.strptime(t, date_format) #today object for calc
    diff = end - start #counter for while loop based on days bewteen 'start' date and today
    counter = 0 #counter for while loop
    date_range = []
    today = datetime.date.today()
    while counter <= int(diff.days): 
        date_range.append(today)
        today -= datetime.timedelta (days = 1)
        counter += 1
    return date_range

def tiers(file_name):
    """get list of UIDs per customer tiers by monthly rev from provided files"""
    
    with open(file_name, "r") as f: #test file of UIDs per customer tier
        uids = f.read()
        uids = uids.split("\n")
        uids = list(filter(None, uids))
    y = 0
    vip_dict = {str(x):y for x in uids}
    return vip_dict

def run_query(vip_dict):
    """run query and return percentage, port_count"""

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
    return perc, port_count

def calc_totals(port_count,pct_list):
    """calc port numbers per customer"""
    
    totals_per = []
    for each in pct_list:
        i = port_count * (each*100)
        totals_per.append(i)
    return totals_per

def plotty(label_list, pct_list):
    """plot our results into accessible chart"""

    labels = label_list
    sizes = pct_list
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',shadow=False, startangle=90)
    ax1.axis('equal') 
    plt.show()

def report(label_list, pct_list, port_count):
    """write results in .txt"""
    
    indexer = 0 #easily index lists because we know the order
    totals_per = calc_totals(port_count, pct_list)
    cust_quant = [9, 6, 23, 148, 197, 1297, 14275, "NA"] #quantity of customers per tier
    with open(f"segmentation-analysis.txt", "w") as file:
        for name,number in zip(label_list, pct_list):
            file.write(f'Tier: {indexer + 1} Monthly Spend: {name} Number of customers: {cust_quant[indexer]}%\n'
            + f' Total number of ports: {totals_per[indexer]} Percentage: {round(number,2)}\n--\n')
            indexer += 1
            
def main():
    """main func gathers uids from each file, runs query per, analyzes and reports"""
    
    files = "tier_one.txt", "tier_two.txt", "tier_three.txt", "tier_four.txt", "tier_five.txt", "tier_six.txt", "tier_seven.txt"
    label_list = '10,000+', '6-10,000', '3-6,000', '1-3,000', '5-1,000', '100-500', '0-100', 'inactive' #tier definitions
    pct_list = []
    for file_name in files: # for each list of UIDs
        vip_dict = tiers(file_name) #create vip_dict for each list of UIDs
        perc, port_count = run_query(vip_dict) # run out query and return percentages and counts
        pct_list.append(perc) #add to our list of percentages
    sum_pct = 0 
    for each in pct_list: #inactive accounts not included in query so must find missing percentages
        sum_pct += each
    inactive = 100 - int(sum_pct) # % of inactive account POs
    pct_list.append(inactive)
    plotty(label_list,pct_list) #create our pie chart
    report(label_list, pct_list, port_count) #report for analysis

if __name__ == "__main__":
    main()
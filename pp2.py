import credentials
import datetime
from collections import Counter
import re
import psycopg2 as pg2
from psycopg2 import sql
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import pyplot as mp
import get

def connect_db():
    """connect to postgresql DB """
    try:
        conn = pg2.connect(database = credentials.db_name, user = credentials.postgres_user, password = credentials.postgres_pw)
        return conn
    except:
        "You're not connecting to the DB"

def find_month():
    """finds the month and what week we should be inputting into"""

    today = datetime.date.today() #sunday through saturday is our range for get query
    idx = (today.weekday() + 1) 
    sun = today - datetime.timedelta(7+idx)
    month_range = []

    for each in range(0,7):
        
        date = sun + datetime.timedelta(each)
        month_range.append(date.strftime('%m')) #only need month occurence to determine month
    
    c = Counter(month_range) #determine month by most common month entry in month_range
    month = str(c.most_common(1))

    month_dict = {'01': 'January', '02': 'Feburary', '03': 'March', '04': 'April', '05': 'May', '06': 'June', '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}
    select_month = month_dict[month[3:5]]
    
    return select_month

def find_week(select_month):
    """find which week column to input"""
    
    week_columns = ['week1','week2','week3','week4','week5']
    get_weeks_list = []

    conn = connect_db()
    cur = conn.cursor()
    query = """SELECT week1, week2, week3, week4, week5 FROM p_p WHERE month_name = (%s)"""
    cur.execute(query,(select_month,))
    get_weeks = cur.fetchall()
    
    get_weeks = str(get_weeks) 
    get_weeks = re.sub('[,''()]', '', get_weeks)
    get_weeks = get_weeks.strip('[]') #<^^ clean our SQL object to make it listable

    for each in get_weeks.split():
        get_weeks_list.append(each) #create cleaned list of values
    zipzip = tuple(zip(week_columns, get_weeks_list)) #zip together column names and values

    for weekx,quant in zipzip: #iterate tuple to find the 0 quantity and return week
        if quant == '0':
            week = weekx
            break
    conn.close()

    return week

def insert_weekly(week,port_count, select_month):
    """insert data into our SQL database for the week"""

    conn = connect_db()
    cur = conn.cursor()
    cur.execute(sql.SQL("UPDATE p_p SET {} = %s WHERE month_name = %s").format(sql.Identifier(week)),(port_count,select_month,))
    conn.commit() #^^set weekly count
    query = """UPDATE p_p SET month_total = month_total + (%s) WHERE month_name = (%s)"""
    cur.execute(query,(port_count,select_month,))
    conn.commit() #^^update month to date county
    query = """UPDATE p_p SET ytd = (SELECT SUM(month_total) FROM p_p) WHERE month_name = (%s)"""
    cur.execute(query,(select_month,))
    conn.commit() #^^update yearly count
    conn.close()

def insert_vip(select_month,vip_count):
    """write weekly vip stats in DB from get.py"""
    
    db_names_list = ['vow26193', 'weave20193', 'expectel59775','zang58', 'zen38640', 'signalwire52284','intulse47037']
    vip_val_list = list(vip_count.values()) #convert to list of the values so match with DB names

    conn = connect_db()
    cur = conn.cursor()
    for dbname,vip_val in zip(db_names_list,vip_val_list):
        cur.execute(sql.SQL("UPDATE vip_p_p SET {} = {} + %s WHERE month_name = %s;").format(sql.Identifier(dbname),sql.Identifier(dbname)),(vip_val,select_month,))   
    conn.commit()
    conn.close()

def get_byweek_stats(select_month):
    """get list of week by week stats for months since beginning of year"""

    month_list = ['January', 'Feburary', 'March', 'April', 'May', 'June', 'July'
    + 'August', 'September', 'October', 'November', 'December']
    our_month_list = []

    for i in month_list:
        if i != select_month:
            our_month_list.append(i)
    our_month_list.append(select_month) #get list of past months including this month

    conn = pg2.connect(database = 'porting_pulse', user = 'postgres', password = 'wmacleod0')
    cur = conn.cursor()
    values = []
    for m in our_month_list:
        query = """SELECT week1,week2,week3,week4,week5 FROM p_p WHERE month_name = (%s)"""
        cur.execute(query,(m,)) #query each month for all weeks
        obj = cur.fetchone()
        values.append((obj))
    conn.close()

    values = str(values) 
    values = re.sub('[,''()]', '', values) #clean up sql object
    values = values.strip('[]')
    final_values = []
    for items in values.split(): #make list of all values do not include 0 weeks because month only has 4 weeks
        if items not in ('0', 'None'):
            final_values.append(int(items))
    return final_values

def find_mtd(select_month):
    """find MTD value for report"""
    
    conn = connect_db()
    cur = conn.cursor()
    query = """SELECT month_total FROM p_p WHERE month_name = (%s)"""
    cur.execute(query,(select_month,))
    mtd = cur.fetchone()
    mtd = str(mtd[0])
    conn.close()

    return mtd

def totals(final_values):
    total = 0
    for weeks in final_values: #find ytd port-ins
            total += weeks
    return total

def avg(total,final_values):
    avg_ports = total/len(final_values) #find avg port-ins per week
    return avg_ports

def write_weekly(select_month,port_count,avg,mtd,total,vip_count):
    """write our weekly report"""

    today = datetime.date.today()
    vips = ['Vow(26193)', 'Weave(20193)', 'Expectel(59775)', 'Zang(58)', 'Zen(14449)', 'Signalwire(52284)', 'Intulse(47037)']
    vip_count = list(vip_count.values())
    
    with open(f"PortReport{select_month}/report.txt", "w") as file:
        file.write(f'{today}\nThis past weeks brief stats\n--\nPort-ins past week total: {port_count}\n'
        + f'Average per week year to date: {avg}\n--\nMonth to date:{mtd}\n'
        + f'Year to date: {total}\n--\nVIP week totals: ')
        for name,number in zip(vips,vip_count):
            file.write(f'{name}:\n')
            file.write(f'{number}\n')

def prev_month(select_month):
    """find previous month for monthly report and comparison/analysis"""
    
    if select_month == 'January':
        previous_month = 'December'
    else:
        month_dict = {'January': 1, 'Feburary': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
        pm_num = month_dict[select_month] - 1
        month_dict = {1: 'January', 2: 'Feburary', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
        previous_month = month_dict[pm_num]
    return previous_month

def month_trending(previous_month,select_month):
    """find trends using SQL data and previously gathered data"""
    
    mtd = int(find_mtd(select_month))
    conn = connect_db()
    cur = conn.cursor()
    query = """SELECT month_total FROM p_p WHERE month_name = (%s)"""
    cur.execute(query,(previous_month,))
    p_mtd = cur.fetchone()
    p_mtd = int(p_mtd[0])
    month_trend = ((mtd-p_mtd)/mtd)*100

    db_names_list = ['vow26193', 'weave20193', 'expectel59775','zang58', 'zen38640', 'signalwire52284','intulse47037']
    trend_list = []
    vip_this_last = ()
    for each in db_names_list:
        cur.execute(sql.SQL("SELECT {} FROM vip_p_p WHERE month_name = %s").format(sql.Identifier(each)),(select_month,))
        vip_this_month = cur.fetchone()
        vip_this_month = int(vip_this_month[0])
        cur.execute(sql.SQL("SELECT {} FROM vip_p_p WHERE month_name = %s").format(sql.Identifier(each)),(previous_month,))
        vip_pm = cur.fetchone()
        vip_pm = int(vip_pm[0])
        vip_month_trend = ((vip_this_month-vip_pm)/vip_this_month)*100
        trend_list.append(vip_month_trend) #list of VIP trends
        vip_this_last += (vip_this_month,vip_pm) #tuple of VIP this month quantity, last month quantity
    return month_trend, trend_list, vip_this_last

def write_monthly(select_month,total,comp_time,avg,mtd):
    """write monthly report"""

    previous_month = prev_month(select_month)
    month_trend, trend_list, vip_this_last = month_trending(previous_month,select_month)
    vips = ['Vow(26193)', 'Weave(20193)', 'Expectel(59775)', 'Zang(58)', 'Zen(14449)', 'Signalwire(52284)', 'Intulse(47037)']
    with open(f"PortReport{select_month}/{select_month}-report.txt", "w") as file:
        file.write(f'YTD total port ins: {total}\nYTD average days per port(weekends included): {round(comp_time,2)}\n'
        + f'Average per week year to date: {avg}\n--\n{select_month} total: {mtd}\nTrend compared to'
        + f' last month: {round(month_trend,2)}\n--\n')
        x = 1
        y = 0
        z = 0
        for each in vips:
            file.write(f'{each}\nPrevious Month: {vip_this_last[x]}, {select_month}: {vip_this_last[y]} '
            + f'Trend: {round(trend_list[z],2)}%\n--\n')
            x += 2
            y += 2
            z += 1

def plotty_monthly(total,avg,final_values,select_month):
    """create plot for monthly report"""

    plt.plot([i for i in final_values], '--bo') #generate graph line graph for pulse on incoming port ins
    plt.axis([0,int(len(final_values)), 0, 500])
    plt.title(f'Port-In Pulse\nYTD port-ins:{total}\nAverage per week: {round(avg,2)}')
    plt.ylabel('Port Count')
    plt.xlabel('Weeks YTD')
    mp.savefig(f'PortReport{select_month}/PortReport_YTD.pdf')

def main():
    """main func to be called in weekly get script"""
    
    select_month = find_month()
    week = find_week(select_month)
    port_count,vip_count = get.main()
    insert_weekly(week,port_count, select_month)
    insert_vip(select_month,vip_count)
    return port_count, vip_count
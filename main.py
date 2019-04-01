import os
import pp2
import completion_time

if __name__ == "__main__":

    port_count,vip_count = pp2.main() #get and insert data into SQL
    select_month = pp2.find_month() #find month for report
    os.makedirs(f'PortReport{select_month}', exist_ok=True) #create directory for report
    final_values =  pp2.get_byweek_stats(select_month) #find week stats for report
    total = pp2.totals(final_values) #total ytd
    avg = pp2.avg(total,final_values) #average weekly ytd
    mtd = pp2.find_mtd(select_month) #mtd
    pp2.write_weekly(select_month,port_count,avg,mtd,total,vip_count) #write our weekly report p1
    
    month_choice = str(input('Month Report? [y/n]'))
    if month_choice.lower() == 'y':
        comp_time = completion_time.main()
        pp2.write_monthly(select_month,total,comp_time,avg,mtd)
        pp2.plotty_monthly(total,avg,final_values,select_month)
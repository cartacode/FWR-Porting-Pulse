import numpy as np
import pandas as pd

from flask_PP import db

db.Model.metadata.reflect(db.engine)

class General(db.Model):
    __table__ = db.Model.metadata.tables['p_p']

    def get_df(): #pull, clean, create datapoints

        data = db.session.query(General).all()
        df = pd.DataFrame([(d.month_name, d.week1, d.week2, d.week3, d.week4, d.week5,
                             d.month_total, d.ytd, d.month_index, d.ytd_comp_time, d.month_crd_hit) for d in data], 
                  columns=['Month Name', 'Week 1', 'Week 2', 'Week 3', 'Week 4', 
                            'Week 5','Month Total', 'Year to Date', 'Month Index', 'YTD Completion Time',
                             'CRD Per Hit'])
        df = df.sort_values(by='Month Index', ascending=True).set_index('Month Index')
        df['ytd_total'] = df['Month Total'].sum()
        df = df.replace(0, np.NaN)
        df['YTD Completion Time'] = round(df['YTD Completion Time'].mean(), 2)
        df['YTD CRD'] = round(df['CRD Per Hit'].mean(), 2)*100
        df['YTD Avg Month'] = round(df['Month Total'].mean(), 2)
        df = df.replace(np.NaN, '-')
        return df

    def clean_data(month): #for months

        df = General.get_df()
        if month != 'All':
            df = df[df['Month Name']==f'{month}']
        for index, row in df.iterrows():
            df = { 'Month': f'{month}', 'Week 1': row['Week 1'], 'Week 2': row['Week 2'], 'Week 3': row['Week 3'], 
                'Week 4': row['Week 4'], 'Week 5': row['Week 5'], 
                'Month Total': row['Month Total'], 'Year To Date': row['Year to Date'], 
                'YTD Completion Time': row['YTD Completion Time'], 
                'CRD Per Hit': row['CRD Per Hit'], 'ytd_total': row['ytd_total'], 
                'YTD CRD': row['YTD CRD'], 'YTD Avg Month': row['YTD Avg Month']}
        return df

    def all_data(flag=True): #for general/all

        data = db.session.query(General).all()
        df = pd.DataFrame([(d.month_name, d.week1, d.week2, d.week3, d.week4, d.week5,
                    d.month_total, d.ytd, d.month_index, d.ytd_comp_time, d.month_crd_hit) for d in data], 
                  columns=['Month Name', 'Week 1', 'Week 2', 'Week 3', 'Week 4', 
                            'Week 5','Month Total', 'Year to Date', 'Month Index', 'YTD Completion Time',
                             'Request Date% Hit'])
        df = df.sort_values(by='Month Index', ascending=True).set_index('Month Name')
        df = df.replace(0, '-')
        if flag:
            df = df.drop(columns=['Month Index', 'Year to Date', 'YTD Completion Time'])
        else:
            df = df.drop(columns=[('Month Index')])
        df = df[df['Week 1']!='-']
        return df
        
class Vip(db.Model):
    __table__ = db.Model.metadata.tables['test_vip']

    def get_vip():

        data = db.session.query(Vip).all()
        df_dict = {}

        vips = ['Vow', 'Weave', 'Expectel', 'Zang', 'Zen','SignalWire', 'Intulse']
        vips = ['Vow', 'Weave', 'Expectel', 'Zang', 'Zen','SignalWire', 'Intulse']
        for v in vips:
            data = db.session.query(Vip).all()
            df = pd.DataFrame([(d.month_name, d.vow26193, d.weave20193, d.expectel59775, d.zang58, d.zen38640, 
                                d.signalwire52284, d.intulse47037, d.month_index) for d in data], 
                                columns=['Month Name', 'Vow', 'Weave', 'Expectel', 'Zang', 
                                        'Zen','SignalWire', 'Intulse', 'Month Index'])
            df = df.replace(0, np.NaN)
            df = df.dropna()
            df = df.sort_values(by='Month Index', ascending=False).set_index('Month Index')
            df = df.groupby(['Month Name', "Month Index"], sort=False)[f'{v}'].max()
            df = pd.DataFrame(df)
            df.loc['Total'] = df[f'{v}'].sum()
            df.loc['Average'] = df[f'{v}'].mean()
            df_dict[v] 
        return df_dict

    def selector(vip):

        df_dict = get_vip()
        select = df_dict[f'{vip}']
        average = select[f'{vip}']['Average']
        total = select[f'{vip}']['Total']
        curr_month = select[f'{vip}'][0]
        past_month = select[f'{vip}'][1]
        diff = round(((curr_month-past_month)/curr_month)*100,2)
        return select, average, total, curr_month, past_month, diff
import numpy as np
import pandas as pd

from flask_PP import db
from flask_PP.local import vip_ids

db.Model.metadata.reflect(db.engine)

class General(db.Model):
    __table__ = db.Model.metadata.tables['p_p']

    def gen_pull(): #Pull data and organize data from DB

        data = db.session.query(General).all()
        df = pd.DataFrame([(d.month_name, d.week1, d.week2, d.week3, 
                            d.week4, d.week5, d.month_total, d.ytd, d.month_index, 
                            d.ytd_comp_time, d.month_crd_hit) for d in data], 
                  columns=['Month Name', 'Week 1', 'Week 2', 'Week 3', 'Week 4', 
                            'Week 5','Month Total', 'Year to Date', 'Month Index', 
                            'YTD Completion Time','CRD Per Hit'])
        return df

    def all_data(flag=True):
        """
        For general/all and report,
        True for general page df, False for report df
        """
        df = General.gen_pull()
        df = df.sort_values(by='Month Index', ascending=True).set_index('Month Name').replace(0, '-')
        if flag:
            df = df.drop(columns=['Month Index', 'Year to Date', 'CRD Per Hit'])
        else:
            df = df.drop(columns=[('Month Index')])
        df = df[df['Week 1']!='-']
        return df
    
    def get_df(): #Pull, clean, create datapoints

        df = General.gen_pull()
        df = df.sort_values(by='Month Index', ascending=True).set_index('Month Index')
        df['ytd_total'] = df['Month Total'].sum()
        df = df.replace(0, np.NaN)
        df['YTD Completion Time'] = round(df['YTD Completion Time'].mean(), 2)
        df['YTD CRD'] = round(df['CRD Per Hit'].mean(), 2)*100
        df['YTD Avg Month'] = round(df['Month Total'].mean(), 2)
        df = df.replace(np.NaN, '-')
        return df
        
    def clean_data(month): #For months
        
        df = General.get_df()
        if month != 'All':
            df = df[df['Month Name']==f'{month}']
        else:
            df = General.all_data(flag=True) #If user selects '--'
            return df                        
        for index, row in df.iterrows():
            df = { 'Month': f'{month}', 'Week 1': row['Week 1'],
                'Week 2': row['Week 2'], 'Week 3': row['Week 3'], 
                'Week 4': row['Week 4'], 'Week 5': row['Week 5'], 
                'Month Total': row['Month Total'], 'Year To Date': row['Year to Date'], 
                'YTD Completion Time': row['YTD Completion Time'], 
                'CRD Per Hit': row['CRD Per Hit'], 'ytd_total': row['ytd_total'], 
                'YTD CRD': row['YTD CRD'], 'YTD Avg Month': row['YTD Avg Month']}
        return df

    def bar_gen(): #Bar plot generator for general page

        data = db.session.query(General).all()
        df = pd.DataFrame([(d.month_name, d.week1, d.week2, d.week3, 
                    d.week4, d.week5, d.month_total, d.month_index) for d in data], 
          columns=['Month Name', 'Week 1', 'Week 2', 'Week 3', 'Week 4', 
                    'Week 5','Month Total', 'Month Index'])
        df = df.sort_values(by='Month Index', ascending=True).set_index('Month Index')
        df = df[df['Week 1']!=0]
        bar_colors = [
        "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
        "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
        "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
        bar_labels = df['Month Name'].values.tolist()
        bar_values = df['Month Total'].tolist()
        return bar_labels, bar_values, bar_colors
    
    def month_bar_gen(month): #Bar plot generator for months

        data = db.session.query(General).all()
        df = pd.DataFrame([(d.month_name, d.week1, d.week2, d.week3, 
                            d.week4, d.week5, d.month_total, d.month_index) for d in data], 
                columns=['Month Name', 'Week 1', 'Week 2', 'Week 3', 'Week 4', 
                            'Week 5','Month Total', 'Month Index'])
        df = df.sort_values(by='Month Index', ascending=True).set_index('Month Index')
        df = df[df['Week 1']!=0]
        df = df[df['Month Name']==f'{month}']
        df = df.drop(columns=['Month Name', 'Month Total'])
        bar_colors = [
        "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
        "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
        "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
        bar_labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5',]
        bar_values = df.values.tolist()
        bar_values = [val for sublist in bar_values for val in sublist] #Flatten nested list
        return bar_labels, bar_values, bar_colors

class Vip(db.Model):
    __table__ = db.Model.metadata.tables['vip_p_p']

    def vip_pull(): #Pulls and formats data into preferred DF used for all func

        data = db.session.query(Vip).all()
        df = pd.DataFrame([(d.month_name, d.v, d.v1, 
                        d.v2, d.v3, d.v4, d.v5, d.v6, d.month_index) for d in data], 
                        columns=[vip_ids.df_columns['mn'], vip_ids.df_columns['v'],
                                vip_ids.df_columns['v1'], vip_ids.df_columns['v2'],
                                vip_ids.df_columns['v3'], vip_ids.df_columns['v4'],
                                vip_ids.df_columns['v5'], vip_ids.df_columns['v6'],
                                vip_ids.df_columns['mi']])
        df = df.replace(0, np.NaN)
        df = df.dropna()
        return df

    def vip_main(flag):
        """
        For Main VIP page and Report generating.
        True for Report DF, False for Main page general metrics.
        """
        df = Vip.vip_pull()
        if flag:
            df = df.sort_values(by='Month Index', ascending=True).set_index('Month Index')
            df.loc['Average'] = df.mean(numeric_only=True)
            df.loc['Total'] = df.sum(numeric_only=True)-df.loc['Average']
            return df
        else:
            df = df.sort_values(by='Month Index', ascending=False).set_index('Month Index')
            df['total'] = df.sum(axis=1)
            df.loc['Average'] = df.mean(numeric_only=True)
            df.loc['Total'] = df.sum(numeric_only=True) 
            curr_month = df['total'][0]
            past_month = df['total'][1]
            diff = round(((curr_month-past_month)/curr_month)*100,2)
            df = df.reset_index()
            average = int(df[df['Month Index']=='Average']['total'])
            total = int(df[df['Month Index']=='Total']['total'])-average 
            name = 'VIP Total'
            return curr_month, past_month, diff, average, total, name
    
    def get_vip(): #Get our data dict, only fetches for other models

        df_dict = {}

        vips = vip_ids.list_names['list']
        for v in vips:
            df = Vip.vip_pull()
            df = df.sort_values(by='Month Index', ascending=False).set_index('Month Index')
            df = df.groupby(['Month Name', 'Month Index'], sort=False)[f'{v}'].max()
            df = pd.DataFrame(df)
            df.loc['Average'] = df[f'{v}'].mean()
            df.loc['Total'] = df[f'{v}'].sum()-df.loc['Average'].sum()
            df_dict[v]  = df
        return df_dict

    def selector(vip): #Get DF and metrics per vip_choice

        df_dict = Vip.get_vip()
        select = df_dict[f'{vip}']
        average = select[f'{vip}']['Average']
        total = select[f'{vip}']['Total']
        curr_month = select[f'{vip}'][0]
        past_month = select[f'{vip}'][1]
        diff = round(((curr_month-past_month)/curr_month)*100,2)
        name = [col for col in df_dict[f'{vip}'].columns]
        name = name[0]
        return select, average, total, curr_month, past_month, diff, name
    
    def main_pie_gen(): #Pie plot generator for main VIP page

        df = Vip.vip_pull()
        df = df.sort_values(by='Month Index', ascending=True).set_index('Month Index')
        df.loc['Total'] = df.sum(numeric_only=True)
        df = df.reset_index()
        df = df[df["Month Index"]=='Total']
        df = df.drop(columns=['Month Name', 'Month Index'])
        pie_list = df.values.tolist()
        values = [val for sublist in pie_list for val in sublist]
        labels = vip_ids.list_names['list']
        colors = [
            "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
            "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
            "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
        return values, labels, colors
    
    def vip_bar_gen(vip): 
        """
        Takes in passed vip for vip-choice,
        Generates Bar plots for each Vip
        """
        df = Vip.vip_pull()
        df = df.groupby(['Month Name', "Month Index"], sort=False)[f'{vip}'].max().reset_index()
        bar_labels = df['Month Name'].values.tolist()
        bar_values = df[f'{vip}'].values.tolist()
        bar_colors = [
            "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
            "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
            "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
        return bar_labels, bar_values, bar_colors
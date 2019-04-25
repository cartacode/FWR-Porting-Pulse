from flask import render_template, url_for, redirect, flash, send_file, session
from flask_PP import app
from flask_PP.models import General, Vip
from flask_PP.forms import InputBar, VipButtons

from io import BytesIO
import numpy as np 
import pandas as pd
import xlsxwriter

"""
GENERAL/ALL
"""   

@app.route('/', methods = ['GET','POST'])
@app.route('/general', methods = ['GET','POST'])
def general():

    form = InputBar()
    choice = form.field.data
    df = General.all_data(flag=True) # For main table
    data = General.clean_data(month="January") # For side "YTD METRICS"
    if choice != 'All':
        session['month_var'] = f'{choice}' # Pass choice to 'month_choice' func
        return redirect(url_for('month_choice'))
    return render_template('general.html', form=form, 
                            df = df.to_html(header=False), data=data)

@app.route('/ytd-report', methods = ['GET','POST'])
def ytd_report():
    
    df = General.all_data(flag=False)
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, startrow = 0, merge_cells = False, sheet_name = "Sheet_1")
    workbook = writer.book
    worksheet = writer.sheets["Sheet_1"]
    writer.close()
    output.seek(0)
    return send_file(output, attachment_filename="not-a-test.xlsx", as_attachment=True)
    return redirect(url_for('general'))

"""
MONTHS JAN-DEC
"""   

@app.route('/month-choice', methods = ['GET','POST'])
def month_choice():
    
    month = session.get('month_var', None)
    form = InputBar()
    choice = form.field.data
    df = General.clean_data(month)# Get dataframe from last input of InputBar(selectfield)
    if choice != 'All':       
        session['month_var'] = f'{choice}' # Pass choice to next iter of 'month_choice' func
        return redirect(url_for('month_choice'))
    return render_template('months.html', data = df, form=form)

"""
VIP
"""   

@app.route('/vip', methods = ['GET','POST'])
def vip():

    form = InputBar()
    btns = VipButtons()
    choice = form.field.data
    curr_month, past_month, diff, average, total, name = Vip.vip_main(flag=False)
    if btns.weave.data: # Really want to turn this into a dict
        session['vip_var'] = 'Weave' # Pass choice to 'vip_choice' func
        return redirect(url_for('vip_choice')) 
    elif btns.zang.data:
        session['vip_var'] = 'Zang'
        return redirect(url_for('vip_choice'))
    elif btns.signalwire.data:
        session['vip_var'] = 'SignalWire'
        return redirect(url_for('vip_choice'))
    elif btns.vow.data:
        session['vip_var'] = 'Vow'
        return redirect(url_for('vip_choice'))
    elif btns.zen.data:
        session['vip_var'] = 'Zen'
        return redirect(url_for('vip_choice'))
    elif btns.expectel.data:
        session['vip_var'] = 'Expectel'
        return redirect(url_for('vip_choice'))
    elif btns.intulse.data:
        session['vip_var'] = 'Intulse'
        return redirect(url_for('vip_choice'))
    elif choice != 'All':
        session['month_var'] = f'{choice}'
        return redirect(url_for('month_choice'))
    return render_template('vip.html', data = { 
                            'curr_month': curr_month, 'past_month': past_month, 
                            'diff': diff, 'average': average, 'total': total,'name': name}, 
                            form=form, btns=btns)

@app.route('/vip-report', methods = ['GET','POST'])
def vip_report():

    df = Vip.vip_main(flag=True)
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, startrow = 0, merge_cells = False, sheet_name = "Sheet_1")
    workbook = writer.book
    worksheet = writer.sheets["Sheet_1"]
    writer.close()
    output.seek(0)
    return send_file(output, attachment_filename="vip-not-a-test.xlsx", as_attachment=True)
    return redirect(url_for('vip'))

@app.route('/vip-choice', methods = ['GET','POST'])  
def vip_choice():

    btns = VipButtons()
    form = InputBar()    
    choice = form.field.data
    vip = session.get('vip_var', None)                 
    select, average, total, curr_month, past_month, diff, name = Vip.selector(vip)
    if btns.weave.data: ###Really want to turn this into a dict
        session['vip_var'] = 'Weave' # Pass choice to next iter of 'vip_choice' func
        return redirect(url_for('vip_choice'))
    elif btns.zang.data:
        session['vip_var'] = 'Zang'
        return redirect(url_for('vip_choice'))
    elif btns.signalwire.data:
        session['vip_var'] = 'SignalWire'
        return redirect(url_for('vip_choice'))
    elif btns.vow.data:
        session['vip_var'] = 'Vow'
        return redirect(url_for('vip_choice'))
    elif btns.zen.data:
        session['vip_var'] = 'Zen'
        return redirect(url_for('vip_choice'))
    elif btns.expectel.data:
        session['vip_var'] = 'Expectel'
        return redirect(url_for('vip_choice'))
    elif btns.intulse.data:
        session['vip_var'] = 'Intulse'
        return redirect(url_for('vip_choice'))
    if choice != 'All':
        return redirect(url_for('month_choice'))
    return render_template('vip.html', data = {'select': select, 'average': average, 
                            'total': total, 'curr_month': curr_month, 'past_month': past_month, 
                            'diff': diff, 'name': name}, form=form, btns=btns)
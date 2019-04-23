from flask import render_template, url_for, redirect, flash, send_file
from flask_PP import app
from flask_PP.models import General, Vip
from flask_PP.forms import InputBar

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
    df = General.all_data(flag=True) #for main table
    data = General.clean_data(month="January") #for side "YTD METRICS"
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('general.html', df = df.to_html(header=False), form=form, data=data)

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
VIP
"""   

@app.route('/vip', methods = ['GET','POST'])
def vip():
    form = InputBar()
    choice = form.field.data
    df_dict = Vip.get_vip()
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('vip.html', data = df_dict, form=form)

@app.route('/vipchoice', methods = ['GET','POST'])  
def vipchoice():
    form = InputBar()    
    choice = form.field.data                    #figure out how pass "vip" variable from page to this func
    select, average, total, curr_month, past_month, diff = selector(vip)
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('vip.html', data = df_dict, form=form)

"""
MONTHS JAN-DEC
"""   

@app.route('/January', methods = ['GET','POST'])
def January():
    form = InputBar()
    choice = form.field.data
    df = General.clean_data(month = 'January')
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('months.html', data = df, form=form)

@app.route('/February', methods = ['GET','POST'])
def Feburary():
    form = InputBar()
    choice = form.field.data
    df = General.clean_data(month = 'Feburary')
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('months.html', data = df, form=form)

@app.route('/March', methods = ['GET','POST'])
def March():
    form = InputBar()
    choice = form.field.data
    df = General.clean_data(month = 'March')
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('months.html', data = df, form=form)

@app.route('/April', methods = ['GET','POST'])
def April():
    form = InputBar()
    choice = form.field.data
    df = General.clean_data(month = 'April')
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('months.html', data = df, form=form)

@app.route('/May', methods = ['GET','POST'])
def May():
    form = InputBar()
    choice = form.field.data
    df = General.clean_data(month = 'May')
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('months.html', data = df, form=form)

@app.route('/June', methods = ['GET','POST'])
def June():
    form = InputBar()
    choice = form.field.data
    df = General.clean_data(month = 'June')
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('months.html', data = df, form=form)

@app.route('/July', methods = ['GET','POST'])
def July():
    form = InputBar()
    choice = form.field.data
    df = General.clean_data(month = 'July')
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('months.html', data = df, form=form)

@app.route('/August', methods = ['GET','POST'])
def August():
    form = InputBar()
    choice = form.field.data
    df = General.clean_data(month = 'August')
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('months.html', data = df, form=form)

@app.route('/September', methods = ['GET','POST'])
def September():
    form = InputBar()
    choice = form.field.data
    df = General.clean_data(month = 'September')
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('months.html', data = df, form=form)

@app.route('/October', methods = ['GET','POST'])
def October():
    form = InputBar()
    choice = form.field.data
    df = General.clean_data(month = 'October')
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('months.html', data = df, form=form)

@app.route('/November', methods = ['GET','POST'])
def November():
    form = InputBar()
    choice = form.field.data
    df = General.clean_data(month = 'November')
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('months.html', data = df, form=form)

@app.route('/December', methods = ['GET','POST'])
def December():
    form = InputBar()
    choice = form.field.data
    df = General.clean_data(month = 'December')
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('months.html', data = df, form=form)
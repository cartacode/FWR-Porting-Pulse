from io import BytesIO 
import pandas as pd
import xlsxwriter

from flask import render_template, url_for, redirect, send_file, session
from flask_PP import app
from flask_PP.models import General, Vip
from flask_PP.forms import InputBar, VipButtons
from flask_PP.local import vip_ids

"""
GENERAL/ALL
"""   

@app.route('/', methods=['GET', 'POST'])
@app.route('/general', methods=['GET', 'POST'])
def general():

    form = InputBar() #Drop down
    choice = form.field.data
    df = General.all_data(flag=True) # For main table
    data = General.clean_data(month="January") # For side "YTD METRICS"
    bar_labels, bar_values = General.bar_gen() # Bar graph
    if choice != '--':
        session['month_var'] = f'{choice}' # Pass choice to 'month_choice' func
        return redirect(url_for('month_choice'))
    return render_template('general.html', form=form, 
                            df=df.to_html(header=False), data=data,
                            title='Port Ins Per Month', max=1200, 
                            labels=bar_labels, values=bar_values)

@app.route('/ytd-report', methods=['GET', 'POST'])
def ytd_report():# Write and send report
    
    df = General.all_data(flag=False)
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, startrow=0, merge_cells=False, sheet_name="Sheet_1")
    workbook = writer.book
    worksheet = writer.sheets["Sheet_1"]
    writer.close()
    output.seek(0)
    return send_file(output, attachment_filename="ytd-report.xlsx", 
                    as_attachment=True)
    return redirect(url_for('general'))

"""
MONTHS JAN-DEC
"""   

@app.route('/month-choice', methods=['GET', 'POST'])
def month_choice():
    
    month = session.get('month_var', None) # Passed from general()
    if month == 'All':
        return redirect(url_for('general'))
    form = InputBar()
    choice = form.field.data
    df = General.clean_data(month)# Get dataframe from last input of InputBar(selectfield)
    bar_labels, bar_values = General.month_bar_gen(month=month)
    if choice != '--':       
        session['month_var'] = f'{choice}' # Pass choice to next iter of 'month_choice' func
        return redirect(url_for('month_choice'))
    return render_template('months.html', data=df, form=form,
                            title=f'{month}', max=400, 
                            labels=bar_labels, values=bar_values)

"""
VIP
"""   

@app.route('/vip', methods=['GET', 'POST'])
def vip():

    form = InputBar()
    choice = form.field.data
    btns = VipButtons() # Buttons for each Vip
    values, labels, colors = Vip.main_pie_gen()
    curr_month, past_month, diff, average, total, name = Vip.vip_main(flag=False)
    if btns.v1.data: # Really want to turn this into a dict
        session['vip_var'] = vip_ids.vips['v1'] # Pass choice to 'vip_choice' func
        return redirect(url_for('vip_choice')) 
    elif btns.v3.data:
        session['vip_var'] = vip_ids.vips['v3']
        return redirect(url_for('vip_choice'))
    elif btns.v5.data:
        session['vip_var'] = vip_ids.vips['v5']
        return redirect(url_for('vip_choice'))
    elif btns.v.data:
        session['vip_var'] = vip_ids.vips['v']
        return redirect(url_for('vip_choice'))
    elif btns.v4.data:
        session['vip_var'] = vip_ids.vips['v4']
        return redirect(url_for('vip_choice'))
    elif btns.v2.data:
        session['vip_var'] = vip_ids.vips['v2']
        return redirect(url_for('vip_choice'))
    elif btns.v6.data:
        session['vip_var'] = vip_ids.vips['v6']
        return redirect(url_for('vip_choice'))
    elif choice != '--':
        session['month_var'] = f'{choice}'
        return redirect(url_for('month_choice'))
    return render_template('vip.html', data={ 
                            'curr_month': curr_month, 'past_month': past_month, 
                            'diff': diff, 'average': average, 'total': total,'name': name}, 
                            form=form, btns=btns, set=zip(values, labels, colors))

@app.route('/vip-report', methods=['GET', 'POST'])
def vip_report(): # Write and send report

    df = Vip.vip_main(flag=True)
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, startrow = 0, merge_cells=False, sheet_name="Sheet_1")
    workbook = writer.book
    worksheet = writer.sheets["Sheet_1"]
    writer.close()
    output.seek(0)
    return send_file(output, attachment_filename="vip-report.xlsx",
                    as_attachment=True)
    return redirect(url_for('vip'))

@app.route('/vip-choice', methods=['GET', 'POST'])  
def vip_choice():

    btns = VipButtons()
    form = InputBar()    
    choice = form.field.data
    vip = session.get('vip_var', None) # Passed from vip()
    bar_labels, bar_values = Vip.vip_bar_gen(vip=vip)                 
    select, average, total, curr_month, past_month, diff, name = Vip.selector(vip)
    if btns.v1.data: ###Really want to turn this into a dict
        session['vip_var'] = vip_ids.vips['v1'] # Pass choice to next iter of 'vip_choice' func
        return redirect(url_for('vip_choice'))
    elif btns.v3.data:
        session['vip_var'] = vip_ids.vips['v3']
        return redirect(url_for('vip_choice'))
    elif btns.v5.data:
        session['vip_var'] = vip_ids.vips['v5']
        return redirect(url_for('vip_choice'))
    elif btns.v.data:
        session['vip_var'] = vip_ids.vips['v']
        return redirect(url_for('vip_choice'))
    elif btns.v4.data:
        session['vip_var'] = vip_ids.vips['v4']
        return redirect(url_for('vip_choice'))
    elif btns.v2.data:
        session['vip_var'] = vip_ids.vips['v2']
        return redirect(url_for('vip_choice'))
    elif btns.v6.data:
        session['vip_var'] = vip_ids.vips['v6']
        return redirect(url_for('vip_choice'))
    if choice != '--':
        return redirect(url_for('month_choice'))
    return render_template('vip-choice.html', data={'select': select, 'average': average, 
                            'total': total, 'curr_month': curr_month, 'past_month': past_month, 
                            'diff': diff, 'name': name}, form=form, btns=btns, 
                             max=50, labels=bar_labels, values=bar_values)
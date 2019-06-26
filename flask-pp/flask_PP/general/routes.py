from io import BytesIO 
import pandas as pd
import xlsxwriter

from flask import render_template, url_for, redirect, send_file, session, Blueprint, current_app 
from flask_PP.models import General
from flask_PP.general.forms import InputBar

general = Blueprint('general', __name__)

@general.route('/', methods=['GET', 'POST'])
@general.route('/general', methods=['GET', 'POST'])
def gen():

    form = InputBar() #Drop down
    choice = form.field.data
    df = General.all_data(flag=True) # For main table
    data = General.clean_data(month="January") # For side "YTD METRICS"
    bar_labels, bar_values = General.bar_gen() # Bar graph
    if choice != '--':
        session['month_var'] = f'{choice}' # Pass choice to 'month_choice' func
        return redirect(url_for('general.month_choice'))
    return render_template('general.html', form=form, 
                            df=df.to_html(header=False), data=data,
                            title='Port Ins Per Month', max=1200, 
                            labels=bar_labels, values=bar_values)

@general.route('/ytd-report', methods=['GET', 'POST'])
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
    return redirect(url_for('general.gen'))

@general.route('/month-choice', methods=['GET', 'POST'])
def month_choice():
    
    month = session.get('month_var', None) # Passed from general()
    if month == 'All':
        return redirect(url_for('general.gen'))
    form = InputBar()
    choice = form.field.data
    df = General.clean_data(month)# Get dataframe from last input of InputBar(selectfield)
    bar_labels, bar_values = General.month_bar_gen(month=month)
    if choice != '--':       
        session['month_var'] = f'{choice}' # Pass choice to next iter of 'month_choice' func
        return redirect(url_for('general.month_choice'))
    return render_template('months.html', data=df, form=form,
                            title=f'{month}', max=400, 
                            labels=bar_labels, values=bar_values)
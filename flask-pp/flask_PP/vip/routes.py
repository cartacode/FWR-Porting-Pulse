from io import BytesIO 
import pandas as pd
import xlsxwriter

from flask import render_template, url_for, redirect, send_file, session, Blueprint, current_app
from flask_PP.models import Vip
from flask_PP.vip.forms import InputBar, VipButtons
from flask_PP.local import vip_ids

vip = Blueprint('vip', __name__)

@vip.route('/vip', methods=['GET', 'POST'])
def vip_landing():

    form = InputBar()
    choice = form.field.data
    btns = VipButtons() # Buttons for each Vip
    values, labels, colors = Vip.main_pie_gen()
    curr_month, past_month, diff, average, total, name = Vip.vip_main(flag=False)
    if btns.v1.data: # Really want to turn this into a dict
        session['vip_var'] = vip_ids.vips['v1'] # Pass choice to 'vip_choice' func
        return redirect(url_for('vip.vip_choice')) 
    elif btns.v3.data:
        session['vip_var'] = vip_ids.vips['v3']
        return redirect(url_for('vip.vip_choice'))
    elif btns.v5.data:
        session['vip_var'] = vip_ids.vips['v5']
        return redirect(url_for('vip.vip_choice'))
    elif btns.v.data:
        session['vip_var'] = vip_ids.vips['v']
        return redirect(url_for('vip.vip_choice'))
    elif btns.v4.data:
        session['vip_var'] = vip_ids.vips['v4']
        return redirect(url_for('vip.vip_choice'))
    elif btns.v2.data:
        session['vip_var'] = vip_ids.vips['v2']
        return redirect(url_for('vip.vip_choice'))
    elif btns.v6.data:
        session['vip_var'] = vip_ids.vips['v6']
        return redirect(url_for('vip.vip_choice'))
    elif choice != '--':
        session['month_var'] = f'{choice}'
        return redirect(url_for('general.month_choice'))
    return render_template('vip.html', data={ 
                            'curr_month': curr_month, 'past_month': past_month, 
                            'diff': diff, 'average': average, 'total': total,'name': name}, 
                            form=form, btns=btns, set=zip(values, labels, colors))

@vip.route('/vip-report', methods=['GET', 'POST'])
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
    return redirect(url_for('vip.vip_landing'))

@vip.route('/vip-choice', methods=['GET', 'POST'])  
def vip_choice():

    btns = VipButtons()
    form = InputBar()    
    choice = form.field.data
    vip = session.get('vip_var', None) # Passed from vip()
    bar_labels, bar_values = Vip.vip_bar_gen(vip=vip)                 
    select, average, total, curr_month, past_month, diff, name = Vip.selector(vip)
    if btns.v1.data: ###Really want to turn this into a dict
        session['vip_var'] = vip_ids.vips['v1'] # Pass choice to next iter of 'vip.vip_choice' func
        return redirect(url_for('vip.vip_choice'))
    elif btns.v3.data:
        session['vip_var'] = vip_ids.vips['v3']
        return redirect(url_for('vip.vip_choice'))
    elif btns.v5.data:
        session['vip_var'] = vip_ids.vips['v5']
        return redirect(url_for('vip.vip_choice'))
    elif btns.v.data:
        session['vip_var'] = vip_ids.vips['v']
        return redirect(url_for('vip.vip_choice'))
    elif btns.v4.data:
        session['vip_var'] = vip_ids.vips['v4']
        return redirect(url_for('vip.vip_choice'))
    elif btns.v2.data:
        session['vip_var'] = vip_ids.vips['v2']
        return redirect(url_for('vip.vip_choice'))
    elif btns.v6.data:
        session['vip_var'] = vip_ids.vips['v6']
        return redirect(url_for('vip.vip_choice'))
    if choice != '--':
        return redirect(url_for('general.month_choice'))
    return render_template('vip-choice.html', data={'select': select, 'average': average, 
                            'total': total, 'curr_month': curr_month, 'past_month': past_month, 
                            'diff': diff, 'name': name}, form=form, btns=btns, 
                             max=50, labels=bar_labels, values=bar_values)
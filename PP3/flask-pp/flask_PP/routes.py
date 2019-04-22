from flask import render_template, url_for, redirect, flash
from flask_PP import app
from flask_PP.models import General, Vip
from flask_PP.forms import InputBar, PlotGen

@app.route('/', methods = ['GET','POST'])
@app.route('/general', methods = ['GET','POST'])
def general():
    month = 'All'
    form = InputBar()
    choice = form.field.data
    btn = PlotGen()
    df = General.all_data()
    data = General.clean_data(month="January")
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('general.html', df = df.to_html(header=False), form=form, data=data, btn=btn)

@app.route('/vip', methods = ['GET','POST'])
def vip():
    form = InputBar()
    choice = form.field.data
    df = 'Placeholder'
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('vip.html', data = df, form=form)

@app.route('/January', methods = ['GET','POST'])
def January():
    form = InputBar()
    choice = form.field.data
    btn = PlotGen()
    df = General.clean_data(month = 'January')
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('months.html', data = df, form=form, btn=btn)

@app.route('/February', methods = ['GET','POST'])
def Feburary():
    form = InputBar()
    choice = form.field.data
    btn = PlotGen()
    df = General.clean_data(month = 'Feburary')
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('months.html', data = df, form=form, btn=btn)

@app.route('/March', methods = ['GET','POST'])
def March():
    form = InputBar()
    choice = form.field.data
    btn = PlotGen()
    df = General.clean_data(month = 'March')
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('months.html', data = df, form=form, btn=btn)

@app.route('/April', methods = ['GET','POST'])
def April():
    form = InputBar()
    choice = form.field.data
    btn = PlotGen()
    df = General.clean_data(month = 'April')
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('months.html', data = df, form=form, btn=btn)

@app.route('/May', methods = ['GET','POST'])
def May():
    form = InputBar()
    choice = form.field.data
    btn = PlotGen()
    df = General.clean_data(month = 'May')
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('months.html', data = df, form=form, btn=btn)

@app.route('/June', methods = ['GET','POST'])
def June():
    form = InputBar()
    choice = form.field.data
    btn = PlotGen()
    df = General.clean_data(month = 'June')
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('months.html', data = df, form=form, btn=btn)

@app.route('/July', methods = ['GET','POST'])
def July():
    form = InputBar()
    choice = form.field.data
    btn = PlotGen()
    df = General.clean_data(month = 'July')
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('months.html', data = df, form=form, btn=btn)

@app.route('/August', methods = ['GET','POST'])
def August():
    form = InputBar()
    choice = form.field.data
    btn = PlotGen()
    df = General.clean_data(month = 'August')
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('months.html', data = df, form=form, btn=btn)

@app.route('/September', methods = ['GET','POST'])
def September():
    form = InputBar()
    choice = form.field.data
    btn = PlotGen()
    df = General.clean_data(month = 'September')
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('months.html', data = df, form=form, btn=btn)

@app.route('/October', methods = ['GET','POST'])
def October():
    form = InputBar()
    choice = form.field.data
    btn = PlotGen()
    df = General.clean_data(month = 'October')
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('months.html', data = df, form=form, btn=btn)

@app.route('/November', methods = ['GET','POST'])
def November():
    form = InputBar()
    choice = form.field.data
    btn = PlotGen()
    df = General.clean_data(month = 'November')
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('months.html', data = df, form=form, btn=btn)

@app.route('/December', methods = ['GET','POST'])
def December():
    form = InputBar()
    choice = form.field.data
    btn = PlotGen()
    df = General.clean_data(month = 'December')
    if choice != 'All':
        flash('Success!', 'success')
        return redirect(url_for(f'{choice}'))
    return render_template('months.html', data = df, form=form, btn=btn)


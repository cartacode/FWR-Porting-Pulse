from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

class InputBar(FlaskForm):
    choices = choices = [('All', 'All'), ('January', 'January'), ('Feburary', 'Feburary'), ('March', 'March'), 
                ('April', 'April'), ('May', 'May'), ('June', 'June'), 
                ('July', 'July'), ('August', 'August'), ('September', 'September'), 
                ('October', 'October'), ('November', 'November'), ('December', 'December')]
    field = SelectField(u'Month', choices = choices, coerce=str, default='All')
    submit = SubmitField('Go!')

class VipButtons(FlaskForm):

    weave = SubmitField('Weave')
    zang = SubmitField('Zang')
    signalwire = SubmitField('SignalWire')
    zen = SubmitField('Zen')
    vow = SubmitField('Vow')
    intulse = SubmitField('Intulse')
    expectel = SubmitField('Expectel')

from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

from flask_PP.local import vip_ids

class InputBar(FlaskForm):
    
    choices = choices = [('All', '--'), ('January', 'January'), ('Feburary', 'Feburary'), ('March', 'March'), 
                ('April', 'April'), ('May', 'May'), ('June', 'June'), 
                ('July', 'July'), ('August', 'August'), ('September', 'September'), 
                ('October', 'October'), ('November', 'November'), ('December', 'December')]
    field = SelectField(u'Month', choices = choices, coerce=str, default='All')
    submit = SubmitField('Go!')

class VipButtons(FlaskForm):

    v1 = SubmitField(vip_ids.vips['v1'])
    v3 = SubmitField(vip_ids.vips['v3'])
    v5 = SubmitField(vip_ids.vips['v5'])
    v4 = SubmitField(vip_ids.vips['v3'])
    v = SubmitField(vip_ids.vips['v'])
    v6 = SubmitField(vip_ids.vips['v6'])
    v2 = SubmitField(vip_ids.vips['v2'])
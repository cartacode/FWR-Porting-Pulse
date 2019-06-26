from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

class InputBar(FlaskForm):
    
    choices = choices = [('--', '--'), ('All', 'All'), ('January', 'January'), ('Feburary', 'Feburary'), ('March', 'March'), 
                ('April', 'April'), ('May', 'May'), ('June', 'June'), 
                ('July', 'July'), ('August', 'August'), ('September', 'September'), 
                ('October', 'October'), ('November', 'November'), ('December', 'December')]
    field = SelectField(u'Month', choices = choices, coerce=str, default='--')
    submit = SubmitField('Go!')
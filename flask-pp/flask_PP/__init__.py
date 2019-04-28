from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_PP.local import credentials

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@localhost:5432/{}'.format(
                                    credentials.pg_sql['postgres_user'], 
                                    credentials.pg_sql['postgres_pw'], 
                                    credentials.pg_sql['db_name']
                                    )
app.config['SECRET_KEY'] = '{}'.format(credentials.secret_key)
db = SQLAlchemy(app)

from flask_PP import routes
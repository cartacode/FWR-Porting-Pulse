from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_PP.local import credentials

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@localhost:5432/{}'.format(
                                        credentials.pg_sql['postgres_user'], 
                                        credentials.pg_sql['postgres_pw'], 
                                        credentials.pg_sql['db_name']
                                        )
    app.config['SECRET_KEY'] = '{}'.format(credentials.secret_key)
    
    db.init_app(app)
    with app.app_context():
        db.Model.metadata.reflect(db.engine)
        from flask_PP import models

    from flask_PP.general.routes import general
    app.register_blueprint(general)
    from flask_PP.vip.routes import vip
    app.register_blueprint(vip)

    return app

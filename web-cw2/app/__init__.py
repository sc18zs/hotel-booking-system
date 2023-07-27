from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from sqlalchemy import MetaData
from flask_admin import Admin,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler
import logging
from flask_mail import Mail,Message
app = Flask(__name__)


#set the secret key
app.config.from_object('config')
app.config['SECRET_KEY'] = 'a secret key'

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
#initialise database
db = SQLAlchemy(app=app,metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate(app,db,render_as_batch=True)


# initialize flask-bootstrap
bootstrap=Bootstrap(app)

# initialise email
mail = Mail(app)


#create login manager for index
login_manager = LoginManager()
login_manager.login_view = 'index'
login_manager.init_app(app)

# logging
handler = RotatingFileHandler("flask.log",maxBytes=1024000, backupCount=10)
logging_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)

from app import views,models
from .models import orders,hotels,rooms


# add administrative view here
admin = Admin(app,name='Administration',template_mode='bootstrap3',
              index_view=AdminIndexView(template='adminIndex.html'))


admin.add_view(ModelView(orders, db.session,name='Order'))
admin.add_view(ModelView(hotels, db.session,name='Hotel'))
admin.add_view(ModelView(rooms, db.session,name='Room'))
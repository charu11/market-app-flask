from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_breadcrumbs import Breadcrumbs
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///webapp.db'
app.config['SECRET_KEY'] = 'b36572e91cc4fd12ea88e36f'
# app.config['GOOGLE_CLIENT_ID'] = '555514960694-2mcrsf2h9ad4dupun2ba8q9r0pg8sbb6.apps.googleusercontent.com'
db = SQLAlchemy(app)
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.init_app(app)
Breadcrumbs(app=app)
login_manager.login_view = 'login'
mail = Mail(app)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''


from customer import routes
from customer import admin_routes

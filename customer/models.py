from customer import db, bcrypt, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    credit = db.relationship('Credit', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}')"

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)



    @property
    def password_hash(self):
        return self.password_hash

    @password_hash.setter
    def password_hash(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        if bcrypt.check_password_hash(self.password, attempted_password):
            return True


class Credit(db.Model, UserMixin):

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    balance = db.Column(db.String(20), nullable=False, unique=False)
    coupon_type = db.Column(db.String(30), nullable=False, unique=True)
    coupon_code = db.Column(db.String(60), nullable=False)
    valid_date = db.Column(db.DateTime())
    gift_time = db.Column(db.DateTime())
    owner_id = db.Column(db.Integer(), db.ForeignKey('user.id'))





class Seller(db.Model, UserMixin):
    seller_id = db.Column(db.Integer(), nullable=False, primary_key=True)
    market_place = db.Column(db.String(20), nullable=False, unique=True)
   # asin_report = db.Column(db.String(20), nullable=False, unique=False)
    country = db.Column(db.String(30), nullable=False, unique=False)
    status = db.Column(db.String(30), nullable=False, unique=False)
    submit_date = db.Column(db.DateTime)
    store_name = db.Column(db.String(30), nullable=False, unique=True)
    submit_data = db.Column(db.String(60), nullable=False)
    credit = db.Column(db.Integer(), nullable=False)

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from flask_login import UserMixin
from datetime import datetime

# create user table
class users(UserMixin,db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200))
    phone = db.Column(db.String(200))
    password_hash = db.Column(db.String(128))
    orders = db.relationship('orders', backref='users')

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash,password)

    def changePassword(self,new_password):
        self.password_hash = generate_password_hash(new_password)

    def get_id(self):
        return self.user_id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))


# create hotel table
class hotels(db.Model):
    __tablename__ = 'hotels'
    hotel_id = db.Column(db.Integer, primary_key=True, nullable=False)
    hotel_name = db.Column(db.String(100), nullable=False ,index=True)
    hotel_star = db.Column(db.Integer)
    image_url = db.Column(db.String(300))
    address = db.Column(db.String(500))
    hotel_description = db.Column(db.Text)
    room_number = db.Column(db.Integer)
    rooms = db.relationship('rooms', backref='hotels')

# create order table
class orders(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True, nullable=False)
    quantity = db.Column(db.Integer)
    total = db.Column(db.Float)
    start_time = db.Column(db.Date)
    end_time = db.Column(db.Date)
    name = db.Column(db.String(100))
    ID_type = db.Column(db.String(100))
    ID_number = db.Column(db.String(200))
    order_email = db.Column(db.String(200))
    order_phone = db.Column(db.String(200))
    note = db.Column(db.Text)
    complete = db.Column(db.Boolean)
    set_time = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    ID_number_hash = db.Column(db.String(200))
    # define the foreign key
    order_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    @property
    def ID_number(self):
        raise AttributeError('ID number is not a readable attribute.')

    @ID_number.setter
    def ID_number(self,ID_number):
        self.ID_number_hash = generate_password_hash(ID_number)

    def verity_ID_number(self,ID_number):
        return check_password_hash(self.ID_number_hash, ID_number)


# define the relationship table
booking = db.Table('booking',
                   db.Column('roomId', db.Integer,db.ForeignKey('rooms.room_id')),
                   db.Column('orderId', db.Integer,db.ForeignKey('orders.order_id')))


# create room table
class rooms(db.Model):
    __tablename__ = 'rooms'
    room_id = db.Column(db.Integer, primary_key=True, nullable=False)
    room_name = db.Column(db.String(200))
    room_description = db.Column(db.Text)
    type = db.Column(db.String(100))
    room_code = db.Column(db.String(100))
    available = db.Column(db.Boolean)
    price = db.Column(db.Float)
    orders = db.relationship('orders',
                                secondary=booking,
                                backref=db.backref('rooms',lazy='dynamic'),
                                lazy='dynamic')
    # define the foreign key
    room_hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.hotel_id'))
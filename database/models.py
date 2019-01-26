from app import db
from marshmallow import Schema, fields, ValidationError, pre_load

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_description = db.Column(db.String(5), unique=True)
    description = db.Column(db.String(100), unique=True)

    @property
    def serializable(self):
        return { 'id': self.id, 'short_description': self.short_description, 'description': self.description}

    def __init__(self, id, short_description, description):
        self.id = id
        self.short_description = short_description
        self.description = description

    def __repr__(self):
        return '<Country %r>' % self.description

class CountrySchema(Schema):
    id = fields.Int(dump_only=True)
    short_description = fields.Str()
    description = fields.Str()

class Promo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), unique=False)
    url = db.Column(db.String(400), unique=False)
    splash_message = db.Column(db.String(100), unique=False)

    @property
    def serializable(self):
        return {
            'id': self.id,
            'description': self.description,
            'url': self.url,
            'splash_message': self.splash_message
        }

    def __init__(self, id, description, url, splash_message):
        self.id = id
        self.description = description
        self.url = url
        self.splash_message = splash_message

    def __repr__(self):
        return '<User %r>' % self.description

class PromoSchema(Schema):
    id = fields.Int(dump_only=True)
    description = fields.Str()
    url = fields.Str()
    splash_message = fields.Str()

class Voucher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(80), unique=True)
    amount = db.Column(db.Float)
    currency = db.Column(db.String(10))

    def __init__(self, id, image, amount, currency):
        self.id = id
        self.image = image
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return '<Voucher %r>' % self.amount

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.String, unique=True)
    email_address = db.Column(db.String(100), unique=True)
    login_type = db.Column(db.String(20))
    country_id = db.Column(db.Integer())
    affiliate_url = db.Column(db.String(500))
    transactions = db.relationship('Transaction', backref='purchased')

    def __init__(self, id, guest_id, login_type, country_id, email_address, affiliate_url):
        self.id = id
        self.guest_id = guest_id
        self.email_address = email_address
        self.login_type = login_type
        self.country_id = country_id
        self.affiliate_url = affiliate_url

    def __repr__(self):
        return '<User %r>' % self.id

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    guest_id = fields.Str()
    email_address = fields.Str()
    login_type = fields.Str()
    country_id = fields.Int()
    affiliate_url = fields.Str()

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer())
    date = db.Column(db.Date())
    description = db.Column(db.String(200))
    amount = db.Column(db.Float())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, id, user_id, date, description, amount):
        self.id = id
        self.user_id = user_id
        self.date = date
        self.description = description
        self.amount = amount

class TransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    date = fields.Date()
    description = fields.Str()
    amount = fields.Float()
    purchase_id = fields.Integer()

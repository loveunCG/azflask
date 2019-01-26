import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from settings import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
db = SQLAlchemy(app)


from database.models import PromoSchema, Promo, User, UserSchema, Voucher, Country, CountrySchema, Transaction, TransactionSchema
from functools import wraps
from flask import request, abort


promo_schema = PromoSchema()
promos_schema = PromoSchema(many=True)
country_schema = CountrySchema()
countries_schema = CountrySchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)

@app.route('/az/api/v1.0/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    result = transactions_schema.dump(transactions)
    return jsonify({'transactions': result})

@app.route('/az/api/v1.0/transaction/<int:pk>')
def get_transaction(pk):
    try:
        #transaction_1 = Transaction.query.filter(Transaction.user_id == pk).first()
        transaction_1 = Transaction.query.filter_by(user_id = pk)
    except IntegrityError:
        return jsonify({'message': 'Transaction could not be found'}), 400
    transaction_result = transaction_schema.dump(transaction_1)
    return jsonify({'transaction': transaction_result})

@app.route('/az/api/v1.0/promos', methods = ['GET'])
def get_promos():
    promos = Promo.query.all()
    result = promos_schema.dump(promos)
    return jsonify({'promos': result})

@app.route('/az/api/v1.0/countries', methods = ['GET'])
def get_countries():
    countries = Country.query.all()
    result = countries_schema.dump(countries)
    return jsonify({'countries': result})

@app.route('/az/api/v1.0/country/<int:pk>')
def get_country(pk):
    try:
        country = Country.query.get(pk)
    except IntegrityError:
        return jsonify({'message': 'Country could not be found'}), 400
    country_result = country_schema.dump(country)
    return jsonify({'country': country_result})

@app.route('/az/api/v1.0/users', methods=['GET','POST'])
def get_users():
    if request.method == 'GET':
        users = User.query.all()
        result = users_schema.dump(users)
        return jsonify({'users': result})
    else:
        if not request.json or not 'user_id' in request.json:
            abort(400)
        user1 = {
            'guest_id': request.json['guest_id'],
            'login_type': request.json['login_type'],
            'country_id': request.json['country_id']
        }
        user = User(request.json['guest_id'], request.json['login_type'], request.json['country_id'], 'no', 'no')
        db.session.add(user)
        db.session.commit()
        return jsonify({'user': user1}), 201

@app.route('/az/api/v1.0/user/<int:pk>')
def get_user(pk):
    try:
        user = User.query.get(pk)
    except IntegrityError:
        return jsonify({'message': 'User could not be found'}), 400
    user_result = user_schema.dump(user)
    return jsonify({'users': user_result})

@app.route('/')
def hello_world():
    app.logger.info('Hello World - hit')
    return 'Hello World!'

@app.route('/az/api/v1.0/status', methods=['GET'])
def get_status():
    return jsonify({'status': status})

@app.route('/az/api/v1.0/user_profiles/<int:profile_id>', methods=['GET'])
def get_task(profile_id):
    profile = [profile for profile in user_profile if profile['id'] == profile_id]
    if len(profile) == 0:
        abort(404)
    return jsonify({'user_profile': profile[0]})

@app.route('/az/api/v1.0/user_profiles', methods=['POST'])
def create_user_profile():
    if not request.json or not 'country' in request.json:
        abort(400)
    profile = {
        'id': user_profile[-1]['id'] + 1,
        'type_of_login': request.json['type_of_login'],
        'country': request.json.get('country', ""),
        'default_email_address': False
    }
    user_profile.append(profile)
    return jsonify({'user_profiles': user_profile}), 201

if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()

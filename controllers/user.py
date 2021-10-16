from flask import Blueprint, request, jsonify
from models.extension import db
from models.user import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

user = Blueprint('user', __name__)

@user.route('/sign-in', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # for the post requests for the /login route
        user_name = request.json['user_name']
        password = str(request.json['password'])
        # make search for the user by the email column value
        user = User.query.filter_by(user_name=user_name).first()
        # if the user email is existed
        if user:
            if user==current_user:
                return jsonify({'message': 'This user is already signed currently, you can sign-out to re-sign again with another user !'}),200
            # compare the stored hash pass with the given password
            elif check_password_hash(user.password, password):
                login_user(user, remember=False)
                return jsonify({'message': 'Corrected user credentials and the signed user name is {}'.format(user.user_name)}),200
            else:
                return jsonify({'message': 'Incorrect password, try again'}), 400
        else:
            return jsonify({'message': 'User is not existed !'}), 404
    else:
        # for the get requests for the the /login route
        return jsonify({'message': 'Hit this request with http post not get method to sign in !'}),200

@user.route('/sign-out', methods=['POST', 'GET'])
@login_required
def logout():
    if request.method == 'GET':
        user_name = current_user.user_name
        logout_user()  # will automatically log out the current user
        return jsonify({'message': '{} has been signed out'.format(user_name)})
    else:
        # for the get requests for the the /login route
        return jsonify({'message': 'Hit this request with http get not post method to sign-out !'}),200

@user.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        user_data = request.get_json()
        user_name = user_data['user_name']
        password = str(user_data['password'])
        admin = user_data['admin']
        user = User.query.filter_by(user_name=user_name).first()
        # checks for the existance of the user before store the received user data into db
        if user:
            return jsonify({'message': 'This user is already existed !'}),200
        # do the validation operations on the received form values before storing into db
        elif (len(user_name) < 2):
            return jsonify({'message': 'Sorry, user name must be greater than 2 chars !'}),400
        elif (len(password) < 3):
            return jsonify({'message': 'Sorry, password must be greater than 3 chars !'}),400
        else:
            # create a new user row in the db with a hashed password
            hashed_pass = generate_password_hash(password, method='sha256')
            new_user = User(user_name=user_name,
                            password=hashed_pass, admin=admin)
            db.session.add(new_user)
            db.session.commit()
            # make the signed up account is the currently account
            login_user(new_user, remember=False)
            return jsonify({'message': '{} your account has been created successfully'.format(user_name)}),201
    else:
        # for the get requests for the the /login route
        return jsonify({'message': 'Hit this request with http post not get method to sign up !'}),200

# default endpoint for all non-logined user routes
@user.route('/login_firstly')
def login_firstly():
    return jsonify({'message': 'You must be logined before access this endpoint'}),405

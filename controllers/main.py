from flask import Blueprint, jsonify, request
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if current_user.is_active:
        return jsonify({'message ': 'Hello in this simple restful flask web app based',
                        'currently signed user ': current_user.user_name,
                        'supported message ': 'You can discover the customers routes like cutomer/all, /add, /update, /delete'
                        })
    else:
        return jsonify({'message ': 'Hello in this simple restful flask web app based',
                        'currently signed user ': 'No user is logined',
                        'supported message 1': 'You can login from send user data as json body to /user/sign-in or sign-up from /user/sign-up',
                        'supported message 2': 'After be logined, you can discover the customers via routes like cutomer/all, /add, /update, /delete'
                        })

from models.extension import db
from flask_login import UserMixin

# create a model to describe the schema for the User table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean , default=False)

    def __init__(self,user_name,password,admin=False):
        self.user_name=user_name
        self.password=password
        self.admin=admin

from models.extension import db
from datetime import datetime

# create a model to describe the schema for the Customer table
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    address = db.Column(db.String(150))
    country = db.Column(db.String(50))
    zip_code = db.Column(db.String(10))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
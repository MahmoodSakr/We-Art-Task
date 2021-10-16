from flask import Flask 
from controllers.main import main
from controllers.user import user
from controllers.customer import customer
from models.extension import db
from models.user import User
from flask_login import LoginManager

app = Flask(__name__)

# Setup the app config
app.config.from_pyfile('config.py')

# Registering the app blueprints
app.register_blueprint(main, url_prefix='/')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(customer, url_prefix='/customer')

# Integrate SQLAlchemy layer with the Flask app
db.init_app(app)
with app.app_context():
    db.create_all()
    print('DB is created successfully')

# cutomization the loggin manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='user.login_firstly' # the default endpoint for all non-logined user routes

# tell flask how you load a user
# we load, reference, search for the user based on its PK
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id)) 

# Run the server
if __name__ == '__main__':
    app.run(port= 5000)
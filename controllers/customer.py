from flask import Blueprint, request, jsonify
from models.extension import db
from models.customer import Customer
from flask_login import login_required,  current_user

customer = Blueprint('customer', __name__)


@customer.route('/all', methods=['GET', 'POST'])
@login_required
def show_customers():
    if request.method == 'GET':
        customers = Customer.query.all()
        customers_list = []
        for customer_row in customers:
            customer={}
            customer['id'] = customer_row.id
            customer['first_name'] = customer_row.first_name
            customer['last_name'] = customer_row.last_name
            customer['email'] = customer_row.email
            customer['address'] = customer_row.address
            customer['country'] = customer_row.country
            customer['zip_code'] = customer_row.zip_code
            customer['created_date'] = customer_row.created_date
            customers_list.append(customer)
        if len(customers_list) > 0:
            return jsonify({'All customers number ': len(customers_list),
                            'Customers data': customers_list}),200
        else:
            return jsonify({'message ': 'There are not existed customers !'}),404
    else:
        return jsonify({'message': 'Hit this request with http post not get method !'}),200


@customer.route('/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    if request.method == 'POST':
        # only the admin user can add customers
        if current_user.admin:
            customer_data = request.get_json()
            first_name = customer_data['first_name']
            last_name = customer_data['last_name']
            email = customer_data['email']
            address = customer_data['address']
            country = customer_data['country']
            zip_code = customer_data['zip_code']
            customer = Customer.query.filter_by(
                first_name=first_name, last_name=last_name, email=email).first()
            if customer:
                return jsonify({'message': 'This customer is already existed !'}),200
            # Validate the request data before being storing
            elif (len(first_name) < 3):
                return jsonify({'message': 'Sorry, customer first name must be greater than 2 chars !'}),400
            elif (len(last_name) < 3):
                return jsonify({'message': 'Sorry, customer last name must be greater than 2 chars !'}),400
            elif (len(email) < 9):
                return jsonify({'message': 'Sorry, customer email must be greater than 8 chars !'}),400
            elif (email.find('@') == -1 or email.find('.com') == -1):
                return jsonify({'message': 'Sorry, customer email format is not correct !'}),400
            elif (len(address) < 5):
                return jsonify({'message': 'Sorry, customer address must be greater than 4 chars !'}),400
            elif (len(country) < 5):
                return jsonify({'message': 'Sorry, customer country must be greater than 4 chars !'}),400
            elif (len(zip_code) < 5):
                return jsonify({'message': 'Sorry, customer zip_code must be greater than 4 chars !'}),400
            else:
                # create a new user row in the db with a hashed password
                new_customer = Customer(first_name=first_name,
                                        last_name=last_name,
                                        email=email,
                                        address=address,
                                        country=country,
                                        zip_code=zip_code)
                db.session.add(new_customer)
                db.session.commit()
                return jsonify({'message': '{} account has been created successfully.'.format(first_name)}),201
        else:
            return jsonify({'status': "{} you are not authorized user to create a new customer !".format(current_user.user_name)}),401
    else:
        # for the get requests for the the /login route
        return jsonify({'message': 'Hit this request with http post not get method !'}),200


@customer.route('/find', methods=['GET', 'POST'])
@login_required
def find_customer():
    if request.method == 'POST':
        customer_data = request.get_json()
        first_name = customer_data['first_name']
        last_name = customer_data['last_name']
        email = customer_data['email']
        if (len(first_name) < 3):
            return jsonify({'message': 'Sorry, customer first name must be greater than 2 chars !'}),400
        elif (len(last_name) < 3):
            return jsonify({'message': 'Sorry, customer last name must be greater than 2 chars !'}),400
        elif (len(email) < 9):
            return jsonify({'message': 'Sorry, customer email must be greater than 8 chars !'}),400
        elif (email.find('@') == -1 or email.find('.com') == -1):
            return jsonify({'message': 'Sorry, customer email format is not correct !'}),400
        else:
            customer = Customer.query.filter_by(
            first_name=first_name, last_name=last_name, email=email).first()
            if customer:
                return jsonify({'message' : 'User is existed, and its created since {}'.format(customer.created_date)}),200
            else:
                return jsonify({'message' : 'User is not existed in the DB !'}),404
    else:
        return jsonify({'message': 'Hit this request with http post not get method !'}),200


@customer.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        # only the admin user can update customers
        if current_user.admin:
            customer_data = request.get_json()
            first_name = customer_data['first_name']
            last_name = customer_data['last_name']
            email = customer_data['email']
            address = customer_data['address']
            country = customer_data['country']
            zip_code = customer_data['zip_code']
            customer = Customer.query.filter_by(
                first_name=first_name, last_name=last_name, email=email).first()
            if customer:
                if (len(address) < 5):
                    return jsonify({'message': 'Sorry, customer address must be greater than 4 chars !'}),400
                elif (len(country) < 5):
                    return jsonify({'message': 'Sorry, customer country must be greater than 4 chars !'}),400
                elif (len(zip_code) < 5):
                    return jsonify({'message': 'Sorry, customer zip_code must be greater than 4 chars !'}),400
                customer.address = address
                customer.country = country
                customer.zip_code = zip_code
                db.session.add(customer)
                db.session.commit()
                return jsonify({'status': 'Customer data has been updated successfully.'}),200
            else:
                return jsonify({'status': "This customer is not founded on the DB !"}),404
        else:
            return jsonify({'status': "{} you are not authorized user to update a customer !".format(current_user.user_name)}),401
    else:
        return jsonify({'message': 'Hit this request with http post not get method !'}),200


@customer.route('/delete', methods=['GET', 'POST'])
@login_required
def delete_customer():
    if request.method == 'POST':
        # only the admin user can delete customers
        if current_user.admin:
            customer_data = request.get_json()
            first_name = customer_data['first_name']
            last_name = customer_data['last_name']
            email = customer_data['email']
            customer = Customer.query.filter_by(
                first_name=first_name, last_name=last_name, email=email).first()
            if customer:
                db.session.delete(customer)
                db.session.commit()
                return jsonify({'status': 'Customer data has been deleted successfully.'}),200
            else:
                return jsonify({'status': "This customer is not founded on the DB !"}),404
        else:
            return jsonify({'status': "{} you are not authorized user to delete a customer !".format(current_user.user_name)}),401
    else:
        return jsonify({'message': 'Hit this request with http post not get method !'}),200

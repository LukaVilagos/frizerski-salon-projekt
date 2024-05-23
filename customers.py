from flask import Blueprint, render_template, request, redirect, url_for
from pony.orm import db_session
from database.models import Customer
from operator import attrgetter

customers = Blueprint('customers', __name__)


@customers.route('/', methods=['GET'])
@db_session
def read_customers():
    name = request.args.get('name')
    surname = request.args.get('surname')
    number = request.args.get('number')
    email = request.args.get('email')
    order_by = request.args.get('order-by')

    customers_all = list(Customer.select())

    if name != "null" and (name is not None) and name:
        customers_all = [c for c in customers_all if c.name == str(name)]
    if surname != "null" and (surname is not None) and surname:
        customers_all = [c for c in customers_all if c.surname == str(surname)]
    if number != "null" and (number is not None) and number:
        customers_all = [c for c in customers_all if c.number == str(number)]
    if email != "null" and (email is not None) and email:
        customers_all = [c for c in customers_all if c.email == str(email)]

    if order_by == "added-first":
        customers_all.sort(key=attrgetter('id'))
    elif order_by == "added-last":
        customers_all.sort(key=attrgetter('id'), reverse=True)

    return render_template('customers/customers.html',
                           customers=customers_all, name=name, surname=surname,
                           number=number, email=email, order_by=order_by)


@customers.route('/<int:customer_id>', methods=['GET', 'PUT'])
@db_session
def read_customer(customer_id: int):
    customer = Customer.get(id=customer_id)

    if customer is None:
        return {"error": "Customer not found"}, 404

    if request.method == 'PUT':
        if customer is None:
            return {"error": "Customer not found"}, 404

        data = request.form

        if 'name' in data:
            customer.name = data['name']
        if 'surname' in data:
            customer.surname = data['surname']
        if 'number' in data:
            customer.number = data['number']
        if 'email' in data:
            customer.email = data['email']

        return {"success": "Customer was updated"}, 200

    return render_template('customers/customer.html', customer=customer)


@customers.route('/create')
@db_session
def create_customer():
    return render_template('customers/create.html')


@customers.route('/<int:customer_id>/update', methods=['GET'])
@db_session
def update_customer(customer_id: int):
    customer = Customer.get(id=customer_id)
    if customer is None:
        return {"error": "Customer not found"}, 404

    return render_template('customers/update.html', customer=customer)


@customers.route('/created', methods=['POST'])
@db_session
def created_customer():
    data = request.form

    name = data['name']
    surname = data['surname']
    number = data['number']
    email = data['email']

    Customer(name=name, surname=surname, number=number, email=email)

    return redirect(url_for('customers.read_customers'))


@customers.route('/<int:customer_id>/deleted', methods=['DELETE'])
@db_session
def delete_customer(customer_id: int):
    customer = Customer.get(id=customer_id)

    if customer is None:
        return {"error": "Customer not found"}, 404

    customer.delete()

    return {"success": "Customer was deleted"}, 200

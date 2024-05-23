from flask import Blueprint, render_template, request, redirect, url_for
from pony.orm import db_session
from database.models import Employee
from operator import attrgetter

employees = Blueprint('employees', __name__)


@employees.route('/', methods=['GET'])
@db_session
def read_customers():
    name = request.args.get('name')
    surname = request.args.get('surname')
    number = request.args.get('number')
    email = request.args.get('email')
    title = request.args.get('title')
    order_by = request.args.get('order-by')

    employees_all = list(Employee.select())

    if name != "null" and (name is not None) and name:
        employees_all = [e for e in employees_all if e.name == str(name)]
    if surname != "null" and (surname is not None) and surname:
        employees_all = [e for e in employees_all if e.surname == str(surname)]
    if number != "null" and (number is not None) and number:
        employees_all = [e for e in employees_all if e.number == str(number)]
    if email != "null" and (email is not None) and email:
        employees_all = [e for e in employees_all if e.email == str(email)]
    if title != "null" and (title is not None) and title:
        employees_all = [e for e in employees_all if e.title == str(title)]

    if order_by == "added-first":
        employees_all.sort(key=attrgetter('id'))
    elif order_by == "added-last":
        employees_all.sort(key=attrgetter('id'), reverse=True)

    return render_template('employees/employees.html',
                           employees=employees_all, name=name, surname=surname,
                           number=number, email=email, title=title, order_by=order_by)


@employees.route('/<int:employee_id>', methods=['GET', 'PUT'])
@db_session
def read_customer(employee_id: int):
    employee = Employee.get(id=employee_id)

    if employee is None:
        return {"error": "Employee not found"}, 404

    if request.method == 'PUT':
        if employee is None:
            return {"error": "Employee not found"}, 404

        data = request.form

        if 'name' in data:
            employee.name = data['name']
        if 'surname' in data:
            employee.surname = data['surname']
        if 'number' in data:
            employee.number = data['number']
        if 'email' in data:
            employee.email = data['email']
        if 'title' in data:
            employee.title = data['title']

        return {"success": "Employee was updated"}, 200

    return render_template('employees/employee.html', employee=employee)


@employees.route('/create')
@db_session
def create_customer():
    return render_template('employees/create.html')


@employees.route('/<int:employee_id>/update', methods=['GET'])
@db_session
def update_customer(employee_id: int):
    employee = Employee.get(id=employee_id)
    if employee is None:
        return {"error": "Employee not found"}, 404

    return render_template('employees/update.html', employee=employee)


@employees.route('/created', methods=['POST'])
@db_session
def created_customer():
    data = request.form

    name = data['name']
    surname = data['surname']
    number = data['number']
    email = data['email']
    title = data['title']

    Employee(name=name, surname=surname, number=number, email=email, title=title)

    return redirect(url_for('employees.read_customers'))


@employees.route('/<int:employee_id>/deleted', methods=['DELETE'])
@db_session
def delete_customer(employee_id: int):
    employee = Employee.get(id=employee_id)

    if employee is None:
        return {"error": "Employee not found"}, 404

    employee.delete()

    return {"success": "Employee was deleted"}, 200

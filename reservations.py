from flask import Blueprint, render_template, request, redirect, url_for
from pony.orm import db_session, flush
from database.models import Reservation, Customer, Service, Employee
from datetime import datetime
from operator import attrgetter

reservations = Blueprint('reservations', __name__)


@reservations.route('/', methods=['GET'])
@db_session
def read_reservations():
    id_employee = request.args.get('id_employee')
    id_customer = request.args.get('id_customer')
    id_service = request.args.get('id_service')
    active = request.args.get('active')
    order_by = request.args.get('order-by')

    reservations_all = list(Reservation.select())

    if id_employee != "null" and (id_employee is not None):
        reservations_all = [r for r in reservations_all if r.id_employee.id == int(id_employee)]
    if id_customer != "null" and (id_customer is not None):
        reservations_all = [r for r in reservations_all if r.id_customer.id == int(id_customer)]
    if id_service != "null" and (id_service is not None):
        reservations_all = [r for r in reservations_all if r.id_service.id == int(id_service)]
    if active == "on":
        current_date = datetime.now()
        reservations_all = [r for r in reservations_all if r.reservation_date > current_date]

    if order_by == "earliest":
        reservations_all.sort(key=attrgetter('reservation_date'))
    elif order_by == "latest":
        reservations_all.sort(key=attrgetter('reservation_date'), reverse=True)

    employees = Employee.select()
    customers = Customer.select()
    services = Service.select()

    return render_template('reservations/reservations.html',
                           reservations=reservations_all, employees=employees, customers=customers, services=services,
                           id_employee=id_employee, id_customer=id_customer, id_service=id_service, order_by=order_by,
                           active=active)


@reservations.route('/<int:reservation_id>', methods=['GET', 'PUT'])
@db_session
def read_reservation(reservation_id: int):
    reservation = Reservation.get(id=reservation_id)

    if reservation is None:
        return {"error": "reservation not found"}, 404

    if request.method == 'PUT':
        if reservation is None:
            return {"error": "reservation not found"}, 404

        data = request.form

        if 'id_employee' in data:
            reservation.id_employee = data['id_employee']
        if 'id_customer' in data:
            reservation.id_customer = data['id_customer']
        if 'reservation_date' in data:
            reservation.reservation_date = data['reservation_date']
        if 'created_at' in data:
            reservation.created_at = reservation.created_at
        if 'id_service' in data:
            reservation.id_service = data['id_service']

        return {"success": "reservation was updated"}, 200

    return render_template('reservations/reservation.html', reservation=reservation)


@reservations.route('/create')
@db_session
def create_reservation():
    employees_all = Employee.select()
    customers_all = Customer.select()
    services_all = Service.select()
    return render_template('reservations/create.html', employees=employees_all,
                           customers=customers_all, services=services_all)


@reservations.route('/<int:reservation_id>/update', methods=['GET'])
@db_session
def update_reservation(reservation_id: int):
    reservation = Reservation.get(id=reservation_id)
    employees_all = Employee.select()
    customers_all = Customer.select()
    services_all = Service.select()

    if reservation is None:
        return {"error": "reservation not found"}, 404

    return render_template('reservations/update.html', reservation=reservation, employees=employees_all,
                           customers=customers_all, services=services_all)


@reservations.route('/created', methods=['POST'])
@db_session
def created_reservation():
    data = request.form

    id_employee = data['id_employee']
    id_customer = data['id_customer']
    reservation_date = data['reservation_date']
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    id_service = data['id_service']

    reservation = Reservation(id_employee=id_employee, id_customer=id_customer,
                              reservation_date=reservation_date, created_at=created_at, id_service=id_service)

    flush()

    return redirect(url_for('send_mail', reservation_id=reservation.id, update=False))


@reservations.route('/<int:reservation_id>/deleted', methods=['DELETE'])
@db_session
def delete_reservation(reservation_id: int):
    reservation = Reservation.get(id=reservation_id)

    if reservation is None:
        return {"error": "reservation not found"}, 404

    reservation.delete()

    return {"success": "reservation was deleted"}, 200

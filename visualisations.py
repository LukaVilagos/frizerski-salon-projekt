from flask import Blueprint, render_template
from pony.orm import db_session
from database.models import Reservation, Employee
from collections import OrderedDict
from json import dumps

visualizations = Blueprint('visualizations', __name__)

header_links = [
    {
        "link": "reservations-per-month",
        "endpoint": "reservations_per_month",
        "title": "Rezervacije po mjesecu"
    },
    {
        "link": "revenue-per-month",
        "endpoint": "revenue_per_month",
        "title": "Prihodi po mjesecu"
    },
    {
        "link": "reservations-per-employee",
        "endpoint": "reservations_per_employee",
        "title": "Rezervacije po frizeru"
    }
]


@visualizations.route('/')
def read_visualizations():
    return render_template('visualizations/visualizations.html', header_links=header_links)


@visualizations.route('/reservations-per-month', methods=['GET'])
@db_session
def reservations_per_month():
    reservations = list(Reservation.select())

    reservations_by_month = {}
    for reservation in reservations:
        month = reservation.reservation_date.strftime('%Y-%m')
        if month in reservations_by_month:
            reservations_by_month[month] += 1
        else:
            reservations_by_month[month] = 1

    reservations_by_month = OrderedDict(sorted(reservations_by_month.items()))

    reservations_by_month_json = dumps(reservations_by_month)

    return render_template('visualizations/reservations_per_month.html',
                           header_links=header_links, reservations=reservations_by_month_json)


@visualizations.route('/revenue-per-month', methods=['GET'])
@db_session
def revenue_per_month():
    reservations = list(Reservation.select())

    revenue_by_month = {}
    for reservation in reservations:
        month = reservation.reservation_date.strftime('%Y-%m')
        if month in revenue_by_month:
            revenue_by_month[month] += reservation.id_service.price
        else:
            revenue_by_month[month] = reservation.id_service.price

    revenue_by_month = OrderedDict(sorted(revenue_by_month.items()))

    reservations_by_month_json = dumps(revenue_by_month)

    return render_template('visualizations/revenue_per_month.html',
                           header_links=header_links, reservations=reservations_by_month_json)


@visualizations.route('/reservations-per-employee', methods=['GET'])
@db_session
def reservations_per_employee():
    employees = list(Employee.select())

    reservations_by_employee = {}
    for employee in employees:
        reservations_by_employee[employee.name] = len(employee.reservations)

    reservations_by_employee_json = dumps(reservations_by_employee)

    return render_template('visualizations/reservations_per_employee.html',
                           header_links=header_links, reservations=reservations_by_employee_json)

from flask import Blueprint, render_template, request, redirect, url_for
from pony.orm import db_session
from database.models import Service

services = Blueprint('services', __name__)


@services.route('/', methods=['GET'])
@db_session
def read_services():
    name = request.args.get('name')
    order_by = request.args.get('order-by')

    if name:
        services_all = Service.select(name=name)
    else:
        services_all = Service.select()

    if order_by == "least-expensive":
        services_all = services_all.order_by(Service.price)
    elif order_by == "most-expensive":
        services_all = services_all.order_by(Service.price.desc())

    return render_template('services/services.html', services=services_all, name=name, order_by=order_by)


@services.route('/<int:service_id>', methods=['GET', 'PUT'])
@db_session
def read_service(service_id: int):
    service = Service.get(id=service_id)

    if service is None:
        return {"error": "Service not found"}, 404

    if request.method == 'PUT':
        if service is None:
            return {"error": "Service not found"}, 404

        data = request.form

        if 'name' in data:
            service.name = data['name']
        if 'price' in data:
            service.price = data['price']

        return {"success": "Service was updated"}, 200

    return render_template('services/service.html', service=service)


@services.route('/create')
@db_session
def create_service():
    return render_template('services/create.html')


@services.route('/<int:service_id>/update', methods=['GET'])
@db_session
def update_service(service_id: int):
    service = Service.get(id=service_id)
    if service is None:
        return {"error": "Service not found"}, 404

    return render_template('services/update.html', service=service)


@services.route('/created', methods=['POST'])
@db_session
def created_service():
    data = request.form

    name = data['name']
    price = data['price']

    Service(name=name, price=price)

    return redirect(url_for('services.read_services'))


@services.route('/<int:service_id>/deleted', methods=['DELETE'])
@db_session
def delete_service(service_id: int):
    service = Service.get(id=service_id)

    if service is None:
        return {"error": "Service not found"}, 404

    service.delete()

    return {"success": "Service was deleted"}, 200

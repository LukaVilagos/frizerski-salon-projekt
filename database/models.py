from datetime import datetime
from pony.orm import PrimaryKey, Required, Database, Set

db = Database()


class Employee(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    surname = Required(str)
    number = Required(str)
    email = Required(str, unique=True)
    title = Required(str)
    reservations = Set("Reservation")


class Customer(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    surname = Required(str)
    number = Required(str)
    email = Required(str, unique=True)
    reservations = Set("Reservation")


class Service(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    price = Required(float)
    reservations = Set("Reservation")


class Reservation(db.Entity):
    id = PrimaryKey(int, auto=True)
    id_employee = Required(Employee)
    id_customer = Required(Customer)
    reservation_date = Required(datetime)
    created_at = Required(datetime, default=datetime.now())
    id_service = Required(Service)


db.bind(provider="sqlite", filename="hair_salon.sqlite", create_db=True)
db.generate_mapping(create_tables=True)
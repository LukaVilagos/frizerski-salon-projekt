from flask import Flask, render_template, redirect, url_for, request
from services import services as services_blueprint
from reservations import reservations as reservations_blueprint
from customers import customers as customers_blueprint
from employees import employees as employees_blueprint
from visualisations import visualizations as visualizations_blueprint
from flask_font_awesome import FontAwesome
from flask_mail import Mail, Message
from dotenv import load_dotenv
from os import getenv
from database.models import Reservation
from pony.orm import db_session

load_dotenv(dotenv_path=".env.local")

app = Flask(__name__)
font_awesome = FontAwesome(app)
app.register_blueprint(services_blueprint, url_prefix='/services')
app.register_blueprint(reservations_blueprint, url_prefix='/reservations')
app.register_blueprint(visualizations_blueprint, url_prefix='/visualizations')
app.register_blueprint(customers_blueprint, url_prefix='/customers')
app.register_blueprint(employees_blueprint, url_prefix='/employees')

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/sendMail", methods=["GET"])
@db_session
def send_mail():
    if getenv('SEND_MAIL') == 'true':
        reservation_id = request.args.get('reservation_id')
        update = request.args.get('update')
        reservation = Reservation.get(id=int(reservation_id))

        msg = Message(f"{'Promjena - ' if update == 'True' else ''}"
                      f"Rezervacija termina za {reservation.id_service.name} - {reservation.reservation_date}",
                      sender=getenv('MAIL_USERNAME'), recipients=[reservation.id_customer.email])

        msg.html = (f"<h1>{'Promjena - ' if update == 'True' else ''}Rezervacija za {reservation.id_service.name}</h1>"
                    f"<p>Poštovani, obavještavamo vas da ste rezervirali uslugu {reservation.id_service.name}, "
                    f"datuma {reservation.reservation_date} po cijeni {reservation.id_service.price} €"
                    f"u salonu Frizerski Salon. <br> Radujemo se vašem dolasku.</p>")

        mail.send(msg)

        if update == "True":
            return redirect(url_for('reservations.read_reservation', reservation_id=reservation_id))

    return redirect(url_for('reservations.read_reservations'))


if __name__ == '__main__':
    app.run(port=5000)

from flask import Flask, render_template, redirect
from flask_migrate import Migrate
from models.Seats import db
from routes.booking import booking_bp
import logging
app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
with app.app_context():
    db.create_all()
migrate = Migrate(app, db, compare_type=True)
app.register_blueprint(booking_bp, url_prefix='/')
logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8081)
from flask import Blueprint
from controllers.BookingController import index, book, reset
booking_bp = Blueprint('booking_bp', __name__)
booking_bp.route('/', methods=['GET'])(index)
booking_bp.route('/book', methods=['POST'])(book)
booking_bp.route('/reset', methods=['GET'])(reset)
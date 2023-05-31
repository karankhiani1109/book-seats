from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Seats(db.Model):
    __tablename__ = 'seats_booked'
    id = db.Column(db.Integer, primary_key=True)
    seat_number = db.Column(db.Integer, unique=True, nullable=False)
    is_booked = db.Column(db.Boolean, unique=False, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now())
    @property
    def serialize(self):
        return {
            'id': self.id,
            'seat_number': self.seat_number,
            'is_booked': self.is_booked,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
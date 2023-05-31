import sys
from flask import render_template, request, render_template_string, redirect, url_for
from models.Seats import Seats
from variables import Seat
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from datetime import datetime
import math
db = SQLAlchemy()

def index(): # get API to fetch seats and display input field
    all_seats = fetch_all_seats_with_status()
    max_row = Seat.MAX_SEAT_ROW_COUNT.value
    total_seats = Seat.TOTAL_SEATS.value
    data = structure_seats_data(all_seats)
    return render_template("seats.html", seats=data['seats'], max_row=max_row, total_seats = total_seats)

def book(): # POST API to book seats
    if request.method == 'POST':
        data = request.form
        if (data["total_seats"]).isalnum() is False: #Validations
            return render_template_string("Invalid input")
        seat_count_to_book = int(data["total_seats"])
        if seat_count_to_book > Seat.MAX_SEAT_TO_BOOK.value:
            return render_template_string("Max number of seats can be booked is {{ count }}", count=Seat.MAX_SEAT_TO_BOOK.value)
        all_seats = fetch_all_seats_with_status()
        data = structure_seats_data(all_seats)
        if data["empty_count"] == 0:
            return render_template_string("No seats left")
        elif data["empty_count"] < seat_count_to_book:
            return render_template_string("Only {{ count }} seats left", count=data["empty_count"])
        seat_numbers_to_book = compute_nearby_seats(data, seat_count_to_book)
        print(seat_numbers_to_book)
        fetch_particular_seats(seat_numbers_to_book)
        return redirect(url_for('booking_bp.index'))

def reset(): #get API to reset data
    seats = fetch_all_seats_with_status()
    for seat in seats:
        seat.is_booked = False
        db.session().commit()
    return redirect(url_for('booking_bp.index'))

def compute_nearby_seats(data, number_of_seats_to_book): #Algo to compute nearby seats by priority rules
    row_count = 0
    seats_to_book = []
    row_flag = False
    for seat_row in data['seats']:
        row_count += 1
        if data['rows_count'][row_count] >= number_of_seats_to_book:
            row_flag = True
            for seat in seat_row:
                if len(seats_to_book) >= number_of_seats_to_book:
                    break
                elif seat[1] == 'False':
                    seats_to_book.append(seat[0])
    if row_flag is False:
        row_count = 0
        for seat_row in data['seats']:
            row_count += 1
            if data['rows_count'][row_count] > 0:
                for seat in seat_row:
                    if len(seats_to_book) >= number_of_seats_to_book:
                        break
                    if seat[1] == 'False':
                        seats_to_book.append(seat[0])
    return seats_to_book

def fetch_all_seats_with_status(): #fetch query to get all seats
    query = Seats.query.all()
    return query

def fetch_particular_seats(seat_numbers): #fetch query to get particular seats
    query = Seats.query.filter(Seats.seat_number.in_(seat_numbers)).update({"is_booked":True})
    db.session.commit()

def structure_seats_data(all_seats_data): #convert object data to structure data with row_count
    max_seat_in_row = Seat.MAX_SEAT_ROW_COUNT.value
    total_seats = Seat.TOTAL_SEATS.value
    n = math.ceil(total_seats/max_seat_in_row)
    row = []
    seats_data = []
    row_empty_count = {i:0 for i in range(1,n+1)}
    row_count = 1

    for i in all_seats_data:
        
        if len(row) < max_seat_in_row:
            row.append((str(i.seat_number), str(i.is_booked)))
            if i.is_booked is False:
                if row_count in row_empty_count:
                    row_empty_count[row_count] += 1
                else:
                    row_empty_count[row_count] = 1
        else:
            row_count += 1
            seats_data.append(row)
            row = [(str(i.seat_number), str(i.is_booked))]
            if i.is_booked is False:
                if row_count in row_empty_count:
                    row_empty_count[row_count] += 1
                else:
                    row_empty_count[row_count] = 1
    seats_data.append(row)
    return_data = {}
    return_data['seats'] = seats_data
    return_data['rows_count'] = row_empty_count
    total_empty_count = 0
    for seats_count in row_empty_count.values():
        total_empty_count += seats_count
    return_data['empty_count'] = total_empty_count

    return return_data

def create_new_cabin_with_seats(): #temp function to create entrine in table
    total_seat = Seat.TOTAL_SEATS.value
    for i in range(total_seat):
        seat = Seats()
        seat.seat_number = i + 1
        db.session.add(seat)
        db.session.commit()

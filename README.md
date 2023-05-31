## Assignment 

## Project Goal
Create an seats booking application

### Functionality
Book seats in a cabin with mentioned restrictions:
    - user input to take seats count to book
    - max seats is 80
    - max seats in a row is 7
    - limit to book n number of seats
    - booking priority
        - book seats available in row
        - if not, book nearby seats

### Development

1. Clone the project

`git clone https://github.com/karankhiani1109/book-seats`

3. Run
### Running with Docker Compose

To run the application
` docker-compose up `

To again build the image
` docker-compose build `

To stop the application
` docker-compose down `



4. Navigate to `http://127.0.0.1:5000:5000` to see the app live

5. RUN the API ` http://127.0.0.1:5000 ` displays booked and available seats

6. RUN the GET API ` http://127.0.0.1:5000/reset ` to reset the data in db


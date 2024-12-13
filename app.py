from flask import Flask, render_template, request
import pymysql as sql

app = Flask(__name__)
my_connection = sql.connect(
    host="localhost",
    user="root",
    password="Password#123",
    database="project3"
)
my_cursor = my_connection.cursor()
table_query = """ 
        create table if not exists events (event_id int primary key auto_increment,
        event_name varchar(45), event_type varchar(45),
        event_desc varchar(200), org_email varchar(45),
        org_num varchar(15), max_seats int);
    """
my_cursor.execute(table_query)

book_table_query = """ 
        create table if not exists bookings (bookind_id int primary key auto_increment,
        booking_date date, seats_req int, contanct_email varchar(50)
        );
    """
my_cursor.execute(book_table_query)


@app.route("/", methods=["GET"])
def homepage():
    return render_template("index.html")

@app.route("/register_event", methods=["GET", "POST"])
def register_event():
    if request.method == "POST":
        event_name = request.form["event_name"]
        event_type = request.form["event_type"]
        event_desc = request.form["event_desc"]
        org_email = request.form["org_email"]
        org_num = request.form["org_num"]
        max_seats = request.form["max_seats"]

        insert_query = """ 
        insert into events (event_name, event_type, event_desc, org_email, org_num, max_seats) 
        values (%s, %s, %s, %s, %s, %s);
            """ 
        values = [event_name, event_type, event_desc, org_email, org_num, max_seats]
        my_cursor.execute(insert_query, values)
        my_connection.commit()
        return "sample"
    else:
        return render_template("register_event.html")

@app.route("/view_events", methods=["GET"])
def view_events():
    read_query = """ 
        select * from events;
    """
    my_cursor.execute(read_query)
    raw = my_cursor.fetchall()
    print(raw)
    return render_template("view_events.html", output=raw)

@app.route("/book_event", methods=["GET", "POST"])
def book_event():
    if request.method == "POST":
        event_id = int(request.form["event_id"])
        seats_req = int(request.form["seats"])
        booking_date = request.form["booking_date"]
        contact_email = request.form["contact_email"]
        
        get_event_query = """ 
            select max_seats from events where event_id = %s;
        """
        values = [event_id]
        my_cursor.execute(get_event_query, values)
        fetched = my_cursor.fetchall()

        if not fetched:
            return f"Invalid EventID {event_id}"
        else:
            max_seats = fetched[0][0]
            if seats_req > max_seats:
                return f"Cannot book more than {max_seats}"
            else:
                insert_query = """ 
                    insert into bookings (booking_date, seats_req, contact_email)
                    values (%s, %s, %s);
                """
                values = [booking_date, seats_req, contact_email]
                my_cursor.execute(insert_query, values)
                my_connection.commit()
                return "Booking Succesfull"
    else:
        return render_template("book_event.html")

app.run(debug=True)
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
    return render_template("register_event.html")

app.run(debug=True)
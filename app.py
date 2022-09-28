from flask import Flask, request, render_template, g, redirect
import sqlite3

DATABASE = "coffee.db"

tables_db = {
    "person" : [], 
    "payment" : [], 
    "purchase" : [], 
    "items" : []}

app = Flask(__name__)

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
        for idx, value in enumerate(row))

# Returns database connection
def get_db():
    db = getattr(g, "_database", None)

    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    db.row_factory = make_dicts # Makes Sqlite3 return dicts instead of just results
    return db

# Execute and returns a query in the database
def query_db(query):
    cur = get_db().execute(query)
    rv = cur.fetchall()
    cur.close()
    return rv

# Execute and commits a insert command in the database
def insert_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    cur.close()
    db.commit()

def get_user_payments(name : str = "") -> dict:
    query = "SELECT person.id as id, person.name as name FROM person" + (f" WHERE person.name LIKE '%{name}%'" if name != "" else "")
    people = query_db(query)
    print(people)
    for person in people:
        query = f"SELECT strftime('%m', payment.date) as month, payment.value, payment.discount FROM person, payment WHERE person.id == payment.person_id and person.id = {person['id']} ORDER BY Month"
        pays = query_db(query)
        person["months"] = [
            {"month" : i, 
            "value" : '-',
            "discount" : 0} for i in range(1, 13)]
        
        for pay in pays:
            person["months"][int(pay["month"]) - 1] = pay
            
    return people

# Close database when closing the app
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)

    if db is not None:

        db.close()

# API Contexts
@app.route("/API/get_user_payments/<name>", methods=["GET"]) # Apply a filter to find any name that contains 'name'
@app.route("/API/get_user_payments/", methods=["GET"])
def API_get_user_payments(name : str = ""):
    print(name)
    return get_user_payments(name)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name").strip()
        if name:
            return render_template("index.html", users = get_user_payments(name))
     
    return render_template("index.html", users = get_user_payments())
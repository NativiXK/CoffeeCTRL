from flask import jsonify, request, Blueprint, flash
from app import db
from datetime import date

bp = Blueprint('API', __name__, url_prefix='/API')

# API Contexts
@bp.route("/get_user_payments/<name>", methods=["GET"]) # Apply a filter to find any name that contains 'name'
@bp.route("/get_user_payments/", methods=["GET"])
def API_get_user_payments(name : str = ""):
    return db.get_user_payments(name)

@bp.route("/get_user_by_id", methods=["POST"])
def API_get_user_by_id():
    id = int(request.get_json()["id"])
    user = db.get_db().execute(f"SELECT * FROM person WHERE id={id}").fetchone()

    return jsonify(user)

# Edit user information with json provided
@bp.route("/edit_user", methods=["POST"])
def API_edit_user():
    user = request.get_json()

    cursor = db.get_db()
    query = f"UPDATE person SET name = \"{user['name']}\", email = \"{user['email']}\", area = \"{user['area']}\" WHERE id = {user['id']}"
    cursor.execute(query)
    cursor.commit()

    flash (f"User {user['name']} edited", "message")
    return "1", 200

@bp.route("/add_new_user", methods=["POST"])
def API_add_new_user():
    user = request.get_json()

    cursor = db.get_db()
    query = f"INSERT INTO person (name, email, area) VALUES (\"{user['name']}\", \"{user['email']}\", \"{user['area']}\")"
    cursor.execute(query)
    cursor.commit()

    return "1", 200

@bp.route("/add_user_payment", methods=["POST"])
def API_add_user_payment():

    payment = request.get_json();
    print(payment)

    payment["date"] = '-'.join(payment["date"].split('/')[::-1])

    cursor = db.get_db()
    query = f"INSERT INTO payment (date, value, discount, person_id) VALUES (\"{payment['date']}\", {payment['value']}, {payment['discount']}, {payment['user_id']})"
    print(query)
    cursor.execute(query)
    cursor.commit()

    return "1", 200

# Insert purchase
# 1 first insert items
# INSERT INTO items (coffee_amount, coffee_value, sugar_amount, sugar_value, crackers_amount, crackers_value) VALUES (?, ?, ?, ?, ?, ?)
# 2 second insert purchase with items id
# INSERT INTO purchase (date, value, description, items_id, person_id) VALUES (?, ?, ?, ?, ?)
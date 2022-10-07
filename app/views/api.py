from tkinter.messagebox import NO
from flask import jsonify, request, Blueprint
from app import db

bp = Blueprint('API', __name__, url_prefix='/API')

# API Contexts
@bp.route("/get_user_payments/<name>", methods=["GET"]) # Apply a filter to find any name that contains 'name'
@bp.route("/get_user_payments/", methods=["GET"])
def API_get_user_payments(name : str = ""):
    return db.get_user_payments(name)

# Insert payment for id
@bp.route("/add_user_payment", methods=["POST"])
def API_add_user_payment():
    user_id = request.get_json();
    print (f"Payment added for user {user_id}")
    return jsonify({"Todo" : "Answer"})

# Edit user information with json provided
@bp.route("/edit_user", methods=["POST"])
def API_edit_user():
    user_id = request.get_json();
    print (f"User {user_id} edited")
    return jsonify({"Todo" : "Answer"})

# Insert purchase
# 1 first insert items
# INSERT INTO items (coffee_amount, coffee_value, sugar_amount, sugar_value, crackers_amount, crackers_value) VALUES (?, ?, ?, ?, ?, ?)
# 2 second insert purchase with items id
# INSERT INTO purchase (date, value, description, items_id, person_id) VALUES (?, ?, ?, ?, ?)
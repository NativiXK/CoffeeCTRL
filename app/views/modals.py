from flask import render_template
from app import db

def render_purchase():
    return render_template("modals/purchase.html", people = db.get_people())

def render_coffee(parameters):
    pass

def render_user_payments(parameters):

    user_id = int(parameters["user_id"])
    user = db.get_person_by_id(user_id)
    return render_template("modals/user_payments.html", user_id = user_id, user = user)
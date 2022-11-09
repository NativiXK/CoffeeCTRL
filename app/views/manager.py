from flask import render_template, request, Blueprint, session, redirect
from app import db
from app.views.auth import login_required

bp = Blueprint("manager", __name__, url_prefix="/")

@bp.route("/", methods=["GET", "POST"])
def index():
    if session:
        return redirect("/edit")

    if request.method == "POST":
        name = request.form.get("name").strip()

        if name:
            return render_template("manager/index.html", users = db.get_user_payments_by_name(name))
     
    return render_template("manager/index.html", users = db.get_user_payments_by_name())

@bp.route("/edit", methods=["GET", "POST"])
@login_required
def edit_payments():
    if request.method == "POST":
        name = request.form.get("name").strip()

        if name:
            return render_template("manager/edit.html", users = db.get_user_payments_by_name(name), filter = True)
    
    income = db.get_income()
    spent = db.get_cash_spent()
    return render_template("manager/edit.html", users = db.get_user_payments_by_name(), coffee_price = 15.0,income = income, spent = spent)

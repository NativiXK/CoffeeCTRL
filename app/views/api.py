from flask import jsonify, render_template, request, Blueprint, flash, redirect, session
from app import db
from app.views import modals, auth
import calendar

bp = Blueprint('API', __name__, url_prefix='/API')

# API Contexts
@bp.route("/get_user_payments/<name>", methods=["GET"]) # Apply a filter to find any name that contains 'name'
@bp.route("/get_user_payments/", methods=["GET"])
def API_get_user_payments(name : str = ""):
    return db.get_user_payments_by_name(name)

@bp.route("/get_user_by_id", methods=["POST"])
def API_get_user_by_id():
    id = int(request.get_json()["id"])
    user = db.get_person_by_id(id)

    return jsonify(user)

# Edit user information with json provided
@bp.route("/edit_user", methods=["POST"])
def API_edit_user():
    user = request.get_json()
    db.edit_user(user)

    flash (f"User {user['name']} edited", "message")
    return "1", 200

@bp.route("/add_new_user", methods=["POST"])
def API_add_new_user():
    user_data = request.get_json()

    db.add_new_user(user_data)

    return "1", 200

@bp.route("/add_user_payment", methods=["POST"])
def API_add_user_payment():

    payment = request.get_json();
    # print(payment)

    payment["date"] = '-'.join(payment["date"].split('/')[::-1])

    # if db.is_month_paid(payment["date"], payment["user_id"]):
    #     flash("PAYMENT NOT REGISTERED! There is already a payment for the given month", "error")
    #     return "0", 400

    db.add_payment(payment)
    flash(f"R${ (float(payment['value']) - float(payment['discount'])) } PAYMENT REGISTERED! ", "message")

    return "1", 200

@bp.route("/update_payment", methods=["POST"])
def API_update_payment():
    payment = dict(request.form)
    payment["payment-date"] = '-'.join(payment["payment-date"].split('/')[::-1])

    db.update_payment(payment)
    flash("Payment updated!", "message")
    return redirect("/")

@bp.route("remove_payment", methods=["POST"])
def API_remove_payment():
    pay_id = request.form.get("payment-id")
    db.remove_payment_by_id(pay_id)

    flash("Payment deleted!", "message")
    return redirect("/")

@bp.route("/add_user_purchase", methods=["POST"])
def API_add_user_purchase():
    # ('user_id', '1'), ('purchase-value', '15'), ('purchase-date', '02/11/2022'), ('purchase-description', 'cafe')
    purchase = dict(request.form)
    
    if db.add_purchase(purchase):
        flash("Purchase registered!", "message")
    else:
        flash("Purchase was not registered!", "error")

    return redirect("/")

@bp.route("/save_group_info", methods=["POST"])
def API_save_group_info():
    group = dict(request.form)

    if db.save_group_info(group):
        flash("Group info saved!", "message")
    else:
        flash("It wasn't possible to save group info", "error")

    return redirect("/")

@bp.route("/remove_user_by_id", methods=["POST"])
@auth.login_required
def API_remove_user_by_id():
    user_id = int(request.get_json()["user_id"])
    db.remove_person_by_id(user_id)
    return "1", 200

@bp.route("/cash_report", methods=["POST"])
def API_cash_report():
    table = ""
    cash = 0
    data = request.get_json()

    report_type = data["type"]
    month_num = int(data["month"])
    month_name = calendar.month_name[month_num - 1].upper()
    
    if report_type == "income":
        table = "payment"
    elif report_type == "spent":
        table = "purchase"
    else:
        table = ""

    cursor = db.get_db()
    
    query = f"SELECT person.name as name, {table}.date as date, {table}.value as value" + (f", {table}.discount as discount" if table == 'payment' else "") + f" FROM person, {table} WHERE person.id == {table}.person_id AND person.id IN (SELECT id FROM person WHERE admin_id == {session.get('admin_id')})"

    if (month_num != 13):
        query += f" AND strftime('%m', {table}.date) == '{('0' + str(month_num) if month_num < 10 else str(month_num))}'"
    
    query += f" ORDER BY {table}.date ASC"
    print(query)
    logs = cursor.execute(query).fetchall()

    if (report_type == "income"):
        cash = db.get_income(month_num)
    elif (report_type == "spent"):
        cash = db.get_cash_spent(month_num)
    elif (report_type == "total"):
        cash = db.get_income(month_num) - db.get_cash_spent(month_num)
    else:
        cash = 0

    return jsonify({"html" : render_template("modals/report.html", report_type = report_type, title = (report_type.upper() + " CASH REPORT"), month = month_name, cash = cash, logs = logs)})

@bp.route("/get_modal", methods=["POST"])
def API_get_modal():
    modals_available = {
        "purchase"      : modals.render_purchase, # Render new purchase modal
        "coffee"        : modals.render_coffee, # Renders coffee settings modal
        "user-payments" : modals.render_user_payments # Render user payments list modal
    }
    json = request.get_json()

    modal_type = json["type"]
    parameters = json["parameters"] if "parameters" in json.keys() else None

    if modal_type in modals_available:
        modal_html = modals_available[modal_type](parameters) if parameters else modals_available[modal_type]()

        return jsonify({"html" : modal_html})
    
    else:
        return '0', 400

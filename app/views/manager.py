from flask import render_template, request, Blueprint
from app import db
from app.views.auth import login_required

bp = Blueprint("manager", __name__, url_prefix="/")

@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name").strip()

        if name:
            return render_template("manager/index.html", users = db.get_user_payments(name))
     
    return render_template("manager/index.html", users = db.get_user_payments())

@bp.route("/edit")
@login_required
def edit_payments():
    return render_template("manager/index.html")

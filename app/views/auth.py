import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        print(request.form)
        username = request.form['username']
        password = request.form['password']
        password_repeat = request.form['password-repeat']
        email = request.form['email']
        group_name = request.form['group-name']

        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password or not password_repeat:
            error = f"Password {'confirmation ' if not password_repeat else ''}is required."
        elif password != password_repeat:
            error = "Passwords must be equal."
        elif not email:
            error = "Email is required."
        elif not group_name:
            error = "Group name is required."

        if error is None:
            try:
                query = f"INSERT INTO admin (username, password, email, group_name) VALUES ('{username}', '{generate_password_hash(password)}', '{email}', '{group_name}')"
                print(query)
                db.execute(query)
                db.commit()
            except db.IntegrityError as e:
                error = f"User {username} is already registered. ERRPR:{e}"
            else:
                return redirect(url_for("auth.login"))

        flash(error, 'error')

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None
        admin = db.execute(
            'SELECT * FROM admin WHERE username = ?', (username,)
        ).fetchone()

        if admin is None:
            error = 'Incorrect username.'
        elif not check_password_hash(admin['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['admin_id'] = admin['id']
            
            return redirect(url_for("index"))
        
        flash(error, 'error')

    return render_template("auth/login.html")

@bp.before_app_request
def load_logged_in_user():
    admin_id = session.get('admin_id')

    if admin_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM admin WHERE id = ?', (admin_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

import sqlite3

import click
from flask import current_app, g

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
        for idx, value in enumerate(row))

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = make_dicts #or sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def get_user_payments(name : str = "") -> dict:
    db = get_db()
    query = "SELECT person.id as id, person.name as name, person.email as email, person.area as area FROM person" + (f" WHERE person.name LIKE '%{name}%'" if name != "" else "")
    people = db.execute(query).fetchall()

    for person in people:
        query = f"SELECT strftime('%m', payment.date) as month, payment.value, payment.discount FROM person, payment WHERE person.id == payment.person_id and person.id = {person['id']} ORDER BY Month"
        pays = db.execute(query).fetchall()
        person["months"] = [
            {"month" : i, 
            "value" : 0,
            "discount" : 0} for i in range(1, 13)]
        
        for pay in pays:
            person["months"][int(pay["month"]) - 1] = pay
            
    return people

def get_income(month = 13):

    db = get_db()
    query = f"SELECT SUM(payment.value - payment.discount) as income FROM payment" + (f" WHERE strftime('%m', payment.date) == {month}" if month >= 1 and month <= 12 else "")
    print(query)
    income = db.execute(query).fetchone()["income"]
    print(income)

    return income

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
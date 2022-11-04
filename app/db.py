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

def get_income(month : int = 13): # 13 means yearly filter

    db = get_db()
    query = f"SELECT SUM(payment.value - payment.discount) as income FROM payment" + (f" WHERE strftime('%m', payment.date) == '{('0' + str(month) if month < 10 else str(month))}'" if month >= 1 and month <= 12 else "")
    print(query)
    income = db.execute(query).fetchone()["income"]

    return int(income) if income else 0

def get_cash_spent(month : int = 13): # 13 means yearly filter
    
    db = get_db()
    query = f"SELECT SUM(purchase.value) as spent FROM purchase" + (f" WHERE strftime('%m', purchase.date) == '{('0' + str(month) if month < 10 else str(month))}'" if month >= 1 and month <= 12 else "")
    print(query)
    spent = db.execute(query).fetchone()["spent"]

    return int(spent) if spent else 0

def get_person_by_id(user_id : int):
    db = get_db()
    query = f"SELECT id, name FROM person WHERE id == {user_id}"
    print(query)
    person = db.execute(query).fetchone()

    return person

def get_people():

    db = get_db()
    query = f"SELECT id, name FROM person"
    print(query)
    people = db.execute(query).fetchall()

    return people

def add_purchase(purchase : dict):
    # Purchase dict must have the following keys
    # user_id, value, date and description
    purchase["purchase-date"] = '-'.join(purchase["purchase-date"].split('/')[::-1])
    
    db = get_db()
    query = f"INSERT INTO purchase (date, value, description, person_id) VALUES ('{purchase['purchase-date']}', {purchase['purchase-value']}, '{purchase['purchase-description']}', {purchase['purchase-user_id']})"
    print(query)
    id = db.execute(query)
    db.commit()
    print(id)

    return 1

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
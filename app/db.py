import sqlite3
import click
from flask import current_app, g, session

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

def is_month_paid(date : str, user_id : int):

    db = get_db()
    # Check if there is a payment on the month strftime('%m', payment.date)
    query = f"SELECT * FROM payment WHERE strftime('%m', payment.date) == strftime('%m', '{date}') AND payment.person_id == {user_id}"
    print(query)
    pays = db.execute(query).fetchall()

    return True if pays else False

def add_payment(payment : dict):
    
    db = get_db()
    query = f"INSERT INTO payment (date, value, discount, person_id) VALUES (\"{payment['date']}\", {payment['value']}, {payment['discount']}, {payment['user_id']})"
    print(query)
    db.execute(query)
    db.commit()

    return 1

def remove_payment_by_id(id):

    db = get_db()
    query = f"DELETE FROM payment WHERE id == {id}"
    print(query)
    db.execute(query)
    db.commit()
    return 1

def update_payment(payment):
    db = get_db()
    print(payment)
    query = f"UPDATE payment SET date = '{payment['payment-date']}', value = {payment['payment-value']}, discount = {payment['payment-discount']} WHERE id == {payment['payment-id']}"
    print(query)
    db.execute(query)
    db.commit()

    return 1

def get_user_payments_by_name(name : str = "") -> dict:
    db = get_db()
    query = f"SELECT person.id as id, person.name as name, person.email as email, person.area as area FROM person WHERE admin_id == {session.get('admin_id')}" + (f" AND person.name LIKE '%{name}%'" if name != "" else "")
    print(query)
    people = db.execute(query).fetchall()
    coffee_price = get_coffee_price()

    for person in people:
        query = f"SELECT strftime('%m', payment.date) as month, payment.value, payment.discount FROM payment WHERE person_id == {person['id']} ORDER BY Month"
        pays = db.execute(query).fetchall()

        # print(pays)
        credit = sum([pay['value'] for pay in pays])
        print(credit)

        # person["months"] = [
        #     {"month" : i, 
        #     "value" : 0,
        #     "discount" : 0} for i in range(1, 13)]

        # Apply monthly payments 
        person["months"] = []
        for i in range(1, 13):

            month = {
                "month"     : i, 
                "value"     : 0,
                "discount"  : 0}

            if credit >= coffee_price:
                credit -= coffee_price
                month["value"] = coffee_price
            elif credit < coffee_price and credit:
                month["value"] = credit
                credit -= credit

            person['months'].append(month)
        
        # for pay in pays:
        #     person["months"][int(pay["month"]) - 1] = pay

        for pay in pays:
            person["months"][int(pay["month"]) - 1]['discount'] = pay["discount"]

    return people

def get_groups_by_name(name):
    db = get_db()
    query = f"SELECT id, username, group_name FROM admin WHERE UPPER(group_name) LIKE '%{name.upper()}%'"
    print(query)
    groups = db.execute(query).fetchall()

    for group in groups:
        query = f"SELECT COUNT(*) as people FROM person WHERE admin_id == {group['id']}"
        
        people = db.execute(query).fetchone()["people"]
        group["people"] = people

    return groups

def get_user_payments_by_id(user_id : int = None) -> dict:
    db = get_db()

    query = f"SELECT payment.id as id, payment.date as date, payment.value, payment.discount FROM person, payment WHERE person.id == payment.person_id and person.id = {user_id} ORDER BY date"
    print(query)
    user_payments = db.execute(query).fetchall()

    for pay in user_payments:
        pay["date"] = '/'.join(str(pay["date"]).split('-')[::-1])

    return user_payments

def get_income(month : int = 13): # 13 means yearly filter

    db = get_db()
    query = f"SELECT SUM(payment.value - payment.discount) as income FROM payment WHERE person_id IN (SELECT id FROM person WHERE admin_id == {session.get('admin_id')})" + (f" AND strftime('%m', payment.date) == '{('0' + str(month) if month < 10 else str(month))}'" if month >= 1 and month <= 12 else "")
    print(query)
    income = db.execute(query).fetchone()["income"]

    return int(income) if income else 0

def get_cash_spent(month : int = 13): # 13 means yearly filter
    
    db = get_db()
    query = f"SELECT SUM(purchase.value) as spent FROM purchase WHERE person_id IN (SELECT id FROM person WHERE admin_id == {session.get('admin_id')})" + (f" AND strftime('%m', purchase.date) == '{('0' + str(month) if month < 10 else str(month))}'" if month >= 1 and month <= 12 else "")
    print(query)
    spent = db.execute(query).fetchone()["spent"]

    return int(spent) if spent else 0

def get_person_by_id(user_id : int):
    db = get_db()
    query = f"SELECT * FROM person WHERE id == {user_id}"
    print(query)
    person = db.execute(query).fetchone()

    return person

def get_people():

    db = get_db()
    query = f"SELECT id, name FROM person WHERE admin_id == {session.get('admin_id')}"
    print(query)
    people = db.execute(query).fetchall()

    return people

def add_new_user(user_data : dict):
    db = get_db()
    query = f"INSERT INTO person (name, email, area, admin_id) VALUES (\"{user_data['name']}\", \"{user_data['email']}\", \"{user_data['area']}\", {session.get('admin_id')})"
    print(query)
    db.execute(query)
    db.commit()

    return 1

def edit_user(user : dict):

    cursor = get_db()
    query = f"UPDATE person SET name = \"{user['name']}\", email = \"{user['email']}\", area = \"{user['area']}\" WHERE id = {user['id']}"
    cursor.execute(query)
    cursor.commit()

def remove_person_by_id(user_id : int):

    db = get_db()
    query = f"DELETE FROM payment WHERE person_id == {user_id}"
    print(query)
    db.execute(query)
    query = f"DELETE FROM person WHERE id == {user_id}"
    print(query)
    db.execute(query)
    db.commit()

    return 1

def add_purchase(purchase : dict):
    # Purchase dict must have the following keys
    # user_id, value, date and description
    purchase["purchase-date"] = '-'.join(purchase["purchase-date"].split('/')[::-1])
    
    db = get_db()
    query = f"INSERT INTO purchase (date, value, description, person_id) VALUES ('{purchase['purchase-date']}', {purchase['purchase-value']}, '{purchase['purchase-description']}', {purchase['purchase-user_id']})"
    print(query)
    id = db.execute(query).fetchall()
    db.commit()
    print(id)

    return 1

def get_coffee_price(): #to do
    db = get_db()
    query = f"SELECT monthly_price as price FROM admin WHERE id == {session.get('admin_id')}"
    print(query)
    price = db.execute(query).fetchone()["price"]

    return price if price else 0

def get_group_info():
    db = get_db()
    query = f"SELECT * FROM admin WHERE id == {session.get('admin_id')}"
    print(query)
    group = db.execute(query).fetchone()

    return group

def save_group_info(group : dict):
    db = get_db()
    query = f"UPDATE admin SET group_name = '{group['group-name']}', email = '{group['email']}', monthly_price = {group['monthly-price']} WHERE id == {session.get('admin_id')}"
    print(query)
    try:
        db.execute(query)
        db.commit()
        return 1
    except:
        return 0

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
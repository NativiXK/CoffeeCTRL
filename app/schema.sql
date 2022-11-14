DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS payment;
DROP TABLE IF EXISTS purchase;
DROP TABLE IF EXISTS person;

CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT,
    group_name TEXT UNIQUE,
    monthly_price REAL
);

-- Create table person
CREATE TABLE IF NOT EXISTS person ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    area TEXT,
    admin_id INTEGER NOT NULL,
    FOREIGN key (admin_id) REFERENCES admin (id)
);

-- Create table payment
CREATE TABLE IF NOT EXISTS payment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    value REAL NOT NULL,
    discount REAL NOT NULL,
    person_id INTEGER NOT NULL,
    FOREIGN KEY (person_id) REFERENCES person (id)
);

-- Create table purchase
CREATE TABLE IF NOT EXISTS purchase (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    value REAL NOT NULL,
    description TEXT NOT NULL,
    person_id INTEGER NOT NULL,
    FOREIGN KEY (person_id) REFERENCES person (id)
);

INSERT INTO admin (username, password, group_name) VALUES
    ("admin", "pbkdf2:sha256:260000$hF5MCPGWuihDgxJV$ec34b1b2f7b18bd07838c9c115b1fd936da8574f00fff4467b64635973c299b9", "PSA");

INSERT INTO person (name, email, admin_id) VALUES
    ("Alan Vitor Gomes", "alanvg@ti.net", 1),
    ("Alexandre Endler", "aendler@ti.net", 1),
    ("Anderson Montiel Rodrigues", "montiel@ti.net", 1),
    ("Anderson Luis Hanemann Junior", "andersonlj@ti.net", 1),
    ("Bruno Eduardo Esteves de Lima", "brunoeduardo@ti.net", 1),
    ("Cristiano Deoracki", "deoracki@ti.net", 1),
    ("Daniel Mayer Faria", "faria@ti.net", 1),
    ("Dener Matei", "denerm@ti.net", 1),
    ("Eduardo Leopoldo da Silva", "esilva@ti.net", 1),
    ("Elton Ubiratan Dutra", "eltond@ti.net", 1),
    ("Felipe Silva de Paula", "felipepaula@ti.net", 1),
    ("Gabriel Filipe Scharf Krieger", "gkrieger@ti.net", 1),
    ("Gustavo Tadin Bruno", "gustavotb@ti.net", 1),
    ("Henrique Wolf", "henriquewolf@ti.local", 1);

INSERT INTO payment (date, value, discount, person_id) VALUES
    ("2022-09-27", 5.0, 5.0, 1),
    ("2022-06-23", 10.0, 0.0, 1),
    ("2022-08-27", 5.0, 5.0, 1),
    ("2022-09-27", 10.0, 0.0, 2),
    ("2022-10-05", 10.0, 0.0, 5);

INSERT INTO purchase (date, value, description, person_id) VALUES 
    ("2022-09-17", 88.56, "CAFÉ", 1),
    ("2022-10-25", 6.3, "AÇÚCAR", 1),
    ("2022-10-14", 67.5, "CAFÉ", 1);

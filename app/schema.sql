DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS payment;
DROP TABLE IF EXISTS purchase;
DROP TABLE IF EXISTS person;

CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

-- Create table person
CREATE TABLE IF NOT EXISTS person ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    area TEXT
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

INSERT INTO user (username, password) VALUES
    ("admin", "pbkdf2:sha256:260000$hF5MCPGWuihDgxJV$ec34b1b2f7b18bd07838c9c115b1fd936da8574f00fff4467b64635973c299b9");

INSERT INTO person (name, email) VALUES
    ("Alan Vitor Gomes", "alanvg@weg.net"),
    ("Alexandre Endler", "aendler@weg.net"),
    ("Anderson Montiel Rodrigues", "montiel@weg.net"),
    ("Anderson Luis Hanemann Junior", "andersonlj@weg.net"),
    ("Bruno Eduardo Esteves de Lima", "brunoeduardo@weg.net"),
    ("Cristiano Deoracki", "deoracki@weg.net"),
    ("Daniel Mayer Faria", "faria@weg.net"),
    ("Dener Matei", "denerm@weg.net"),
    ("Eduardo Leopoldo da Silva", "esilva@weg.net"),
    ("Elton Ubiratan Dutra", "eltond@weg.net"),
    ("Felipe Silva de Paula", "felipepaula@weg.net"),
    ("Gabriel Filipe Scharf Krieger", "gkrieger@weg.net"),
    ("Gustavo Tadin Bruno", "gustavotb@weg.net"),
    ("Henrique Wolf", "henriquewolf@weg.local");

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
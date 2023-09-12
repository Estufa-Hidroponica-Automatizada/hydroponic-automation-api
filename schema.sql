CREATE TABLE limit_value (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  value REAL
);

CREATE TABLE user (
  username TEXT,
  password TEXT
);

CREATE TABLE session (
  jwt TEXT
);

CREATE TABLE light_schedule (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  hour INTEGER,
  minute INTEGER,
  state BOOLEAN -- true -> on | false -> off
);

INSERT INTO limit_value (name, value)
VALUES ('temperature_min', 25),
       ('temperature_max', 33),
       ('humidity_min', 30),
       ('humidity_max', 80),
       ('ph_min', 6.5),
       ('ph_max', 7.5),
       ('ec_min', 500),
       ('ec_max', 700),
       ('water_temperature_min', 23),
       ('water_temperature_max', 28);

INSERT INTO light_schedule (hour, minute, state)
VALUES (8, 15, 1),
       (20, 30, 0);

INSERT INTO user (username, password)
VALUES ("admin", "1234");

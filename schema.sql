CREATE TABLE limit_value (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  value REAL
);

CREATE TABLE nutrient_proportion (
  nutrientA INTEGER,
  nutrientB INTEGER
);

CREATE TABLE profile (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  temperature_min TEXT, -- Eg.: 22,25,27 - Para cada semana um valor
  temperature_max TEXT,
  humidity_min TEXT,
  humidity_max TEXT,
  ph_min TEXT,
  ph_max TEXT,
  ec_min TEXT,
  ec_max TEXT,
  water_temperature_min TEXT,
  water_temperature_max TEXT,
  light_schedule TEXT, -- Eg.: [(8,20,1),(20,0,0)],[(7,0,1),(21,0,0)],[(7,40,1),(20,45,0)] - Para cada semana um [] grupo de valores
  nutrient_proportion TEXT -- Eg.: (2,3),(1,1),(2,1)
);

CREATE TABLE profile_actual (
  id_selected INTEGER,
  days_passed INTEGER
);

CREATE TABLE light_schedule (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  hour INTEGER,
  minute INTEGER,
  state BOOLEAN -- true -> on | false -> off
);

CREATE TABLE user (
  username TEXT,
  password TEXT
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

INSERT INTO nutrient_proportion (nutrientA, nutrientB)
VALUES (3, 2);

INSERT INTO profile (name, temperature_min, temperature_max, humidity_min, humidity_max, ph_min, ph_max, ec_min, ec_max, water_temperature_min, water_temperature_max, light_schedule, nutrient_proportion)
VALUES ("ProfileA", "22,25,27", "27,29,31", "40,50,55", "75,80,85", "6,6.5,6.6", "7,7.1,7.2", "500,450,600", "650,600,800", "20,23,25", "25,28,30", "[[(8,20,1),(20,0,0)],[(7,0,1),(21,0,0)],[(7,40,1),(20,45,0)]]", "[(2,3),(1,1),(2,1)]"),
       ("ProfileB", "21,22,25", "25,27,30", "30,55,55", "50,70,80", "6,6.3,6.3", "7.1,7,7.3", "550,450,650", "680,590,830", "20,23,25", "25,28,30", "[[(8,15,1),(19,0,0)],[(7,30,1),(21,15,0)],[(8,40,1),(18,45,0)]]", "[(2,3),(1,1),(2,1)]");

INSERT INTO profile_actual (id_selected, days_passed)
VALUES (1, 0)
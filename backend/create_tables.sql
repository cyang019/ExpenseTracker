-- Creation of currency table
CREATE TABLE IF NOT EXISTS currency (
  id serial PRIMARY KEY,
  name VARCHAR (50) UNIQUE NOT NULL
);

# ExpenseTracker

## Table of Contents
- [Introduction](#introduction)
- [Motivation](#motivation)
- [Tech Stack](#tech-stack)
- [Installation Instruction](#installation-instruction)
- [Testing Instruction](#testing-instruction)
- [Roles and Permissions](#roles-and-permissions)
- [APIs](#apis)
- [Heroku Link](#heroku-link)

## Introduction

**ExpenseTracker** is a backend web project for managing spending records. The tool can help budgeting and understanding spendings with ease. In addition to transaction amount and time, related info such as credit cards, spending categories, currencies and users can be stored and retrieved as well, making it valuable in planning. The project also demonstrates the use of [Flask][1] to run on [Docker][2] with [Postgres][3] and [Auth0][4].


## Motivation

Organizing transactions is an important first step for analyzing spending patterns. By taking the chance to think through the data model of the task, the information flow among different pieces becomes clearer. At least personally, I find this helpful to understand more about the impact of web technologies on data engineering.


## Tech Stack
- Full [Docker][2] Integration with the help of [docker-compose][5]
- Python [Flask][1]
- [SQLAlchemy][6]
- [Flask-Migrate][7] to handle database migratinos by using [Alembic][8]
- [PostgreSQL][9]
- [Auth0][4]
- [Heroku][10]

## Installation Instruction

The project depends on [python3.9][11]. [pip][12] was used for installing python packages.
- ```requirements.txt``` and ```Procfile``` are provided in the project root directory to enable deploying to heroku.
- For installation on a local machine:
  1. Create a ```.env``` file with content copied from .env.example, with valid ```access_token``` values in place.
  2. Adjust ```APPLICATION_CONFIG``` value to either "production" or "development".
  3. In the root directory of the project, ```python manage.py compose up -d``` would build docker images and start docker containers using either production or development configuration, depending on the value of ```APPLICATION_CONFIG```.
  4. ```python manage.py compose down --volume``` would completely stop and remove the containers, and also delete the volume for postgresql database.


## Testing Instruction

In the root directory of the project, ```python manage.py test tests``` would build postgresql database container and perform tests. The command line helper ```manage.py``` would also stop and remove the database container and volume once finished.


## Roles and Permissions

- Role **head-of-household**
  permissions:
    + ```view:cards```,```create:cards```, ```delete:cards```, 
    + ```view:categories```,```create:categories```, ```delete:categories```
    + ```view:currencies```,```create:currencies```, ```delete:currencies```
    + ```view:transactions```,```create:transactions```, ```delete:transactions```, ```update:transactions```
    + ```view:users```,```create:users```, ```delete:users```

- Role **dependent**
  permissions:
    + ```view:cards```
    + ```view:categories```
    + ```view:currencies```
    + ```view:transactions```
    + ```view:users```


## APIs

### Transactions
#### GET '/transactions'

Sample curl request:
```
curl -X GET http://127.0.0.1:5000/transactions
```

Sample response:
```
{

}
```

#### GET 'transactions/int:transaction_id`

Sample curl request:
```
curl -X GET http://127.0.0.1:5000/transactions/2
```

Sample response:
```
```


[1]: https://flask.palletsprojects.com/en/2.0.x/
[2]: https://www.docker.com/
[3]: https://www.postgresql.org/
[4]: https://auth0.com/
[5]: https://docs.docker.com/compose/
[6]: https://www.sqlalchemy.org/
[7]: https://flask-migrate.readthedocs.io/en/latest/
[8]: https://alembic.sqlalchemy.org/en/latest/
[9]: https://www.postgresql.org/
[10]: https://www.heroku.com/
[11]: https://www.python.org/downloads/
[12]: https://pip.pypa.io/en/stable/

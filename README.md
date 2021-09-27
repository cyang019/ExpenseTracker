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
- [Flask-Migrate][7] to handle database migrations by using [Alembic][8]
- [PostgreSQL][9]
- [Auth0][4]
- [Heroku][10]

## Installation Instruction

[python3.9][11] was used. Packages can be installed with [pip][12].

- ```requirements.txt``` and ```Procfile``` are provided in the project root directory to enable deploying to heroku.
- For local machine:
  1. Create a ```.env``` using the content from .env.example, with a valid ```access_token``` value in place.
  2. Adjust ```APPLICATION_CONFIG``` value to either "production" or "development".
  3. In the root directory of the project, ```python manage.py compose up -d``` would build docker images and start docker containers using either production or development configuration, depending on the value of ```APPLICATION_CONFIG```.
  4. ```python manage.py compose down --volume``` would completely stop and remove the containers, and also delete the volume for postgresql database.


## Testing Instruction

In the root directory of the project, ```python manage.py test tests``` would build postgresql database container and perform tests. The container and associated pgdata volume would also get removed upon testing finish.


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

#### GET '/transactions'

- Retrieves all transaction records.
- Request Arguments: None
- Returns: A JSON object with keys "amount", "card_id", "category_id", "currency_id", "description", "id", "receipt_no", and "time". "amount" is in cents.

Sample curl request:
```
curl -X GET http://127.0.0.1:5000/transactions -H "Authorization: Bearer $USER_TOKEN"
```

Sample response:
```
{
  "success": true,
  "transactions": [
    {
      "amount": 70196,
      "card_id": 12,
      "category_id": 10,
      "currency_id": 5,
      "description": "Suggest suffer once once parent.",
      "id": 1,
      "receipt_no": "1-208-00209-0",
      "time": "Thu, 27 May 2021 00:00:00 GMT"
    },
    {
      "amount": 33039,
      "card_id": 10,
      "category_id": 1,
      "currency_id": 3,
      "description": "About pull future on too.",
      "id": 2,
      "receipt_no": "0-8461-5574-5",
      "time": "Fri, 27 Nov 2020 00:00:00 GMT"
    },
    {
      "amount": 50624,
      "card_id": 2,
      "category_id": 9,
      "currency_id": 4,
      "description": "Likely choose at fill pattern environment.",
      "id": 3,
      "receipt_no": "0-7266-1883-7",
      "time": "Wed, 31 Mar 2021 00:00:00 GMT"
    },
    {
      "amount": 26027,
      "card_id": 15,
      "category_id": 7,
      "currency_id": 4,
      "description": "Second above west thought.",
      "id": 4,
      "receipt_no": "0-933770-30-8",
      "time": "Mon, 22 Mar 2021 00:00:00 GMT"
    },
    {
      "amount": 92601,
      "card_id": 11,
      "category_id": 1,
      "currency_id": 4,
      "description": "Time age model foreign work month.",
      "id": 5,
      "receipt_no": "0-296-70549-7",
      "time": "Wed, 07 Jul 2021 00:00:00 GMT"
    },
    {
      "amount": 39211,
      "card_id": 15,
      "category_id": 8,
      "currency_id": 4,
      "description": "Old news movie life science time.",
      "id": 6,
      "receipt_no": "1-5205-4532-0",
      "time": "Sat, 20 Mar 2021 00:00:00 GMT"
    }
  ]
}
```

#### GET '/transactions/int:transaction_id`

- Retrieves a single transaction record
- Request arguments: None
- Returns: a JSON object that contains a status code and the corresponding transaction (with keys "amount", "card_id", "category_id", "currency_id", "description", "id", "receipt_no", and "time").

Sample curl request:
```
curl -X GET http://127.0.0.1:5000/transactions/2 -H "Authorization: Bearer $USER_TOKEN"
```

Sample response:
```
{
  "success": true,
  "transaction": {
    "amount": 33039,
    "card_id": 10,
    "category_id": 1,
    "currency_id": 3,
    "description": "About pull future on too.",
    "id": 2,
    "receipt_no": "0-8461-5574-5",
    "time": "Fri, 27 Nov 2020 00:00:00 GMT"
  }
}
```

#### GET '/cards'

- Retrieves all credit cards with details.
- Request arguments: None
- Returns: on success, a JSON object with status code and a list of credit cards, each with keys "code", "expire", "id", "number", "processor", and "user_id". 

Sample curl request:
```
curl -X GET http://127.0.0.1:5000/cards -H "Authorization: Bearer $USER_TOKEN"
```

Sample response:
```
{
  "cards": [
    {
      "code": "900",
      "expire": "01/23",
      "id": 1,
      "number": "38450820075151",
      "processor": "jcb 15 digit",
      "user_id": 1
    },
    {
      "code": "434",
      "expire": "11/28",
      "id": 2,
      "number": "501801459865",
      "processor": "american express",
      "user_id": 3
    },
    {
      "code": "187",
      "expire": "06/25",
      "id": 3,
      "number": "4861914022612",
      "processor": "american express",
      "user_id": 8
    },
    {
      "code": "8125",
      "expire": "12/24",
      "id": 4,
      "number": "4249823487693170543",
      "processor": "visa 19 digit",
      "user_id": 6
    },
    {
      "code": "268",
      "expire": "09/25",
      "id": 5,
      "number": "3529922830376654",
      "processor": "american express",
      "user_id": 4
    }
  ],
  "success": true
}
```

#### GET '/cards/int:card_id'

- Retrieves a single credit card information by ```card_id```.
- Request argument: None
- Returns: on success, a JSON object with status code and the credit card info ("code", "expire", "id", "number", "processor", and "user_id"), otherwise 404 if the quried card_id does not exist

Sample curl request:
```
curl -X GET http://127.0.0.1:5000/cards/1 -H "Authorization: Bearer $USER_TOKEN"
```

Sample response:
```
{
  "card": {
    "code": "900",
    "expire": "01/23",
    "id": 1,
    "number": "38450820075151",
    "processor": "jcb 15 digit",
    "user_id": 1
  },
  "success": true
}

```

#### GET '/categories'

- Retrieves all existing categories to organize transactions.
- Request Argument: None
- Returns: a JSON object with the status code and a list of categories.

Sample curl request:
```
curl -X GET http://127.0.0.1:5000/categories -H "Authorization: Bearer $USER_TOKEN"
```

Sample response:
```
{
  "categories": [
    {
      "id": 1,
      "name": "grocery"
    },
    {
      "id": 2,
      "name": "catering"
    },
    {
      "id": 3,
      "name": "home improvement"
    },
    {
      "id": 4,
      "name": "entertainment"
    },
    {
      "id": 5,
      "name": "utility"
    },
    {
      "id": 6,
      "name": "rent"
    },
    {
      "id": 7,
      "name": "mortgage"
    },
    {
      "id": 8,
      "name": "education"
    },
    {
      "id": 9,
      "name": "auto"
    }
  ],
  "success": true
}
```

#### GET '/categories/int:category_id'

- Retrieves a category item by category_id.
- Request Argument: None
- Returns: a JSON object with the status code and the corresponding category object.

Sample curl request:
```
curl -X GET http://127.0.0.1:5000/categories/1 -H "Authorization: Bearer $USER_TOKEN"
```

Sample response:
```
{
  "category": {
    "id": 1,
    "name": "grocery"
  },
  "success": true
}
```


#### GET '/currencies'

- Retrieves all existing currencies used for transactions.
- Request Argument: None
- Returns: a JSON object with the status code and a list of currencies.

Sample curl request:
```
curl -X GET http://127.0.0.1:5000/currencies -H "Authorization: Bearer $USER_TOKEN"
```

Sample response:
```
{
  "currencies": [
    {
      "id": 1,
      "name": "USD"
    },
    {
      "id": 2,
      "name": "EUR"
    },
    {
      "id": 3,
      "name": "CHF"
    },
    {
      "id": 4,
      "name": "JPY"
    },
    {
      "id": 5,
      "name": "CNY"
    }
  ],
  "success": true
}
```

#### GET '/currencies/int:currency_id'

- Retrieves a currency item by currency_id.
- Request Argument: None
- Returns: a JSON object with the status code and the corresponding currency object.

Sample curl request:
```
curl -X GET http://127.0.0.1:5000/currencies/1 -H "Authorization: Bearer $USER_TOKEN"
```

Sample response:
```
{
  "currency": {
    "id": 1,
    "name": "USD"
  },
  "success": true
}
```


#### GET '/users'

- Retrieves all existing credit card users.
- Request Argument: None
- Returns: a JSON object with the status code and a list of users.

Sample curl request:
```
curl -X GET http://127.0.0.1:5000/users -H "Authorization: Bearer $USER_TOKEN"
```

Sample response:
```
{
  "success": true,
  "users": [
    {
      "email": "laurie35@fields.com",
      "id": 1,
      "name": "Michael Wright"
    },
    {
      "email": "gpoole@brown.org",
      "id": 2,
      "name": "Kimberly Brooks"
    },
    {
      "email": "melanie54@roy.com",
      "id": 3,
      "name": "Deanna Robinson"
    },
    {
      "email": "victoriaellis@yahoo.com",
      "id": 4,
      "name": "Daniel Duarte"
    }
  ]
}
```

#### GET '/users/int:user_id'

- Retrieves a credit card user by user_id.
- Request Argument: None
- Returns: a JSON object with the status code and the corresponding user object.

Sample curl request:
```
curl -X GET http://127.0.0.1:5000/users/1 -H "Authorization: Bearer $USER_TOKEN"
```

Sample response:
```
{
  "success": true,
  "user": {
    "email": "laurie35@fields.com",
    "id": 1,
    "name": "Michael Wright"
  }
}
```

#### POST '/transactions'

- Creates a transaction in the database
- Request arguments:
  + card_id: id of an existing credit card id
  + category_id: id of an existing category
  + amount: integer in cents
  + currency_id: id of an existing currency
  + time: transaction time with format "%m/%d/%y %H:%M:%S.%f"
  + description: optional short description for the transaction
  + receipt_no: optional receipt info
- Returns: a JSON object with status code true when success.

Sample curl request:
```
curl -d '{"card_id":1, "category_id": "1", "amount": 9990, "currency_id": 1, "time": "1/1/21 12:00:00.0", "description": "book", "receipt_no": "12345"}' -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN" -X POST http://127.0.0.1:5000/transactions
```

Sample response:
```
{
  "success": True
}
```

#### POST '/cards'

- Creates a credit card in the database
- Request arguments:
  + user_id: id of an existing credit card user
  + number: credit card number
  + code: security code
  + expire: expire month/year
  + processor: credit card processor
- Returns: a JSON object with status code true when success.

Sample curl request:
```
curl -d '{"user_id":1, "number": "5034567890123456", "code": 001, "expire": "12/24", "processsor": "mastercard"}' -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN" -X POST http://127.0.0.1:5000/cards
```

Sample response:
```
{
  "success": True
}
```

#### POST '/categories'

- Creates a purchase category in the database
- Request arguments:
  + name: category name
- Returns: a JSON object with status code true when success.

Sample curl request:
```
curl -d '{"name": "grocery"}' -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN" -X POST http://127.0.0.1:5000/categories
```

Sample response:
```
{
  "success": True
}
```

#### POST '/currencies'

- Creates an allowed currency in the database
- Request arguments:
  + name: currency name
- Returns: a JSON object with status code true when success.

Sample curl request:
```
curl -d '{"name": "USD"}' -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN" -X POST http://127.0.0.1:5000/currencies
```

Sample response:
```
{
  "success": True
}
```

#### POST '/users'

- Creates a credit card user in the database
- Request arguments:
  + name: user name
- Returns: a JSON object with status code true when success.

Sample curl request:
```
curl -d '{"name": "Robert James"}' -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN" -X POST http://127.0.0.1:5000/users
```

Sample response:
```
{
  "success": True
}
```

#### DELETE '/transactions/int:transaction_id'

- Deletes a transaction by transaction_id
- Request parameters: None
- Returns: a JSON object with "success" status true and transaction_id when deletion was successful

Sample curl request:
```
curl -X DELETE http://127.0.0.1:5000/transactions/1 -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN"
```

Sample response:
```
{
  "success": True,
  'deleted': 1
}
```

#### DELETE '/cards/int:card_id'

- Deletes a credit card and its corresponding transactions
- Request parameters: None
- Returns: a JSON object with "success" status true and card_id when deletion was successful

Sample curl request:
```
curl -X DELETE http://127.0.0.1:5000/cards/2 -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN"
```

Sample response:
```
{
  "success": True,
  'deleted': 2
}
```

#### DELETE '/categories/int:category_id'

- Deletes a transaction category by category_id and its corresponding transactions
- Request parameters: None
- Returns: a JSON object with "success" status true and category_id when deletion was successful

Sample curl request:
```
curl -X DELETE http://127.0.0.1:5000/categories/3 -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN"
```

Sample response:
```
{
  "success": True,
  'deleted': 3
}
```

#### DELETE '/currencies/int:currency_id'

- Deletes a currency by currency_id and its corresponding transactions
- Request parameters: None
- Returns: a JSON object with "success" status true and currency_id when deletion was successful

Sample curl request:
```
curl -X DELETE http://127.0.0.1:5000/currencies/2 -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN"
```

Sample response:
```
{
  "success": True,
  'deleted': 2
}
```

#### DELETE '/users/int:user_id'

- Deletes a credit card user by user_id and her or his credit cards and transactions
- Request parameters: None
- Returns: a JSON object with "success" status true and user_id when deletion was successful

Sample curl request:
```
curl -X DELETE http://127.0.0.1:5000/users/2 -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN"
```

Sample response:
```
{
  "success": True,
  'deleted': 2
}
```

#### PATCH '/transactions/<int:transaction_id>'

- Updates an existing transaction
- Request arguments:
  + card_id: optional id of an existing credit card id
  + category_id: optional id of an existing category
  + amount: optional transaction amount in cents
  + currency_id: optional id of an existing currency
  + time: optional transaction time with format "%m/%d/%y %H:%M:%S.%f"
  + description: optional short description for the transaction
  + receipt_no: optional receipt info
- Returns: a JSON object with status code true when success.

Sample curl request:
```
curl -d '{"card_id":3, "category_id": "2", "amount": 9989, "currency_id": 1, "time": "1/1/22 12:00:00.0", "description": "book", "receipt_no": "54321"}' -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN" -X PATCH http://127.0.0.1:5000/transactions/3
```

Sample response:
```
{
  "success": True
}
```

## Heroku Link

[ExpenseTracker](https://slim-expense-tracker.herokuapp.com/)


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

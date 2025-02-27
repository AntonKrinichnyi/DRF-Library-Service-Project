# DRF Library Service API

API for online management system for book borrowings. The system will optimize the 
library administrators’ work and make the service much more user-friendly.

## Installing using GitHub

Install PostgreSQL and create db

```shell
git clone <link>
cd library_service
python -m venv venv
source venv\Scripts\activate
pip install requirements.txt
set DB_HOST=<your db hostname>
set DB_NAME=<your db name>
set DB_USER=<your db username>
set DB_PASSWORD=<your db User password>
set DJANGO_SECRET_KEY=<your secret key>
set TELEGRAM_TOKEN=<your telegram token>
set TELEGRAM_CHAT_ID=<your telegram chat id>
set STRIPE_PUBLISHABLE_KEY=<your stripe publishable key>
set STRIPE_SECRET_KEY=<you stripe secret key>
python manage.py migrate
python manage.py runserver
```

## Getting started with Docker

Build containers in docker-compose file with command,
docker should be installed

```shell
docker-compose build
```

And start it with command

```shell
docker-compose up
```

## Getting access
Open your browser and enter the domain for book app

```shell
http://127.0.0.1:8000/api/book/
```

Open your browser and enter the domain for borrowing app

```shell
http://127.0.0.1:8000/api/borrowing/
```

You can create your user own User here

```shell
http://127.0.0.1:8000/api/user/create/
```

Or you can use already created users:
Regular user:
    username: sampleuser@test.com
    password: samplepassword3223
Admin or Superuser:
    username: sampleadmin@test.com
    password: heater2332

You can get access token here

```shell
http://127.0.0.1:8000/api/user/token/
```

## Features

* JWT authenticated
* Admin panel
* Managing borrowing and payment
* Creating books and authors
* Filtering books by title
* Telegram notificated
* Stripe payment

To get acquainted with all endpoints you can read
swagger documentation by link

```shell
http://127.0.0.1:8000/api/doc/swagger/
```
# knock_api

Simple RESTful API for Knock coding challenge. Written using the Flask framework.

## Installation

```
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt 
python route.py
```

For local development, copy `sample.config.py` to `config.py`, edit the file to supply the required fields and uncomment the Config from route.py and message.py

Heroku deployments operate using environment variables and `config.py` is not necessary.

## Highlights

* Simple easy-to-follow RESTful API. 
* Implements basic CRUD on each API resource (abstract methods on base class force compliance).
* User registration/authentication with salted + hashed passwords.
* Relay all inbound messages to all participants via email and in-app.
* Perform basic input validation on required fields.

## To Do

* Read and write session ID and token in a cookie.
* Validate session info before allowing reads/writes on conversations.
* More error handling in various places.
* Pagination support for conversations with a lot of messages.
* Sanitize HTML to prevent abuse.

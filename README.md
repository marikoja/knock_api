# knock_api

Simple RESTful API for Knock coding challenge. Written using the Flask framework.

## Installation

```
. venv/bin/activate
pip install -r requirements.txt 
python route.py
```

For local development, copy `sample.config.py` to `config.py`, edit the file to supply the required fields and uncomment the Config from route.py and message.py

Heroku deployments operate using environment variables and `config.py` is not necessary.

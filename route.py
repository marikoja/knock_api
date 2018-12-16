from flask import Flask
from models import *
from config import Config
from pg_adapter import *
import json

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://'+Config.USER+':\
#'+Config.PW+'@'+Config.HOST+':'+Config.PORT+'/'+Config.DB
db.init_app(app)
adapter = PgAdapter(db)

@app.route("/")
def main():
    rows = adapter.query('SELECT * FROM users WHERE email = :email', {'email' : 'maggie@mutt.com'} )

    return json.dumps(rows)

if __name__ == '__main__':
    app.run()

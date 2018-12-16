from flask import Flask
from flask import request
from models import *
from config import Config

from resources.user import *

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://'+Config.USER+':\
#'+Config.PW+'@'+Config.HOST+':'+Config.PORT+'/'+Config.DB
db.init_app(app)

# adapter = PgAdapter(db)

@app.route("/", methods=['GET', 'POST'])
def main():

    user = User(db, request, None)
    
    if request.method == 'GET':
        result = user.read()
    
    return result

if __name__ == '__main__':
    app.run()

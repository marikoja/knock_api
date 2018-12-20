from flask import Flask
from flask import request
from flask_cors import CORS
#from config import Config
import os
from models import *
from resources.user import *
from resources.auth import *
from resources.conversation import *
from resources.message import *


app = Flask(__name__)

# Allow requests from other domains, enable cross-origin
CORS(app)

app.config['DEBUG'] = True

# Config file with connection info only used for local dev
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://'+Config.USER+':\
#'+Config.PW+'@'+Config.HOST+':'+Config.PORT+'/'+Config.DB

# Pull in the DATABASE_URL environment variable set by Heroku
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db.init_app(app)

@app.route("/auth", methods=['POST'])
def auth():

    auth = Auth(db, request)
    return auth.create()

@app.route("/user", methods=['GET', 'POST'])
def user():

    user = User(db, request, None)
    
    if request.method == 'GET':
        result = user.read()
    elif request.method == 'POST':
        result = user.create()

    return result
    
@app.route("/conversation", methods=['POST'])
def conversation():

    conversation = Conversation(db, request, None)
    return conversation.create()
    
@app.route("/conversation/<int:conversation_id>", methods=['GET'])
def conversation_id(conversation_id):
    
    conversation = Conversation(db, request, conversation_id)
    return conversation.read()
    
@app.route("/conversation/<int:conversation_id>/message", methods=['POST'])
def message(conversation_id):

    message = Message(db, request, conversation_id)
    return message.create()

@app.route("/mailgun_catch_all", methods=['POST'])
def mailgun():
    mailgun = Message(db, request, None)
    
    return mailgun.handle_mailgun()
    
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

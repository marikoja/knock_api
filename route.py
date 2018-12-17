from flask import Flask
from flask import request
from config import Config
from models import *
from resources.user import *
from resources.auth import *
from resources.conversation import *
from resources.message import *

app = Flask(__name__)

app.config['DEBUG'] = Config.DEBUG
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://'+Config.USER+':\
#'+Config.PW+'@'+Config.HOST+':'+Config.PORT+'/'+Config.DB
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
    app.run()

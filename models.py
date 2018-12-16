from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }


class Users(BaseModel, db.Model):
    """Model for the users table"""
    __tablename__ = 'users'

    user_id = db.Column(db.BigInteger, primary_key = True)
    user_name = db.Column(db.Text, index = True)
    salt = db.Column(db.Text)
    email= db.Column(db.Text, index = True)
    pw_hash = db.Column(db.Text)

class Session(BaseModel, db.Model):
    """Model for the session table"""
    __tablename__ = 'session'

    session_id = db.Column(db.BigInteger, primary_key = True)
    user_id = db.Column(db.BigInteger, index = True)
    token = db.Column(db.Text)
    expiration = db.Column(db.TIMESTAMP(True), index = True)

class Conversation(BaseModel, db.Model):
    """Model for the conversation table"""
    __tablename__ = 'conversation'

    conversation_id = db.Column(db.BigInteger, primary_key = True)

class Message(BaseModel, db.Model):
    """Model for the message table"""
    __tablename__ = 'message'

    message_id = db.Column(db.BigInteger, primary_key = True)
    conversation_id = db.Column(db.BigInteger, index = True)
    text = db.Column(db.Text)
    user_id = db.Column(db.Text, index = True)
    expiration = db.Column(db.TIMESTAMP(True), index = True)

class Participant(BaseModel, db.Model):
    """Model for the participant table"""
    __tablename__ = 'participant'

    conversation_id = db.Column(db.BigInteger, primary_key = True)
    user_id = db.Column(db.Text, primary_key = True)

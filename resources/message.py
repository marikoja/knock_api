from config import Config
from base import Base
import json
import requests
import os

class Message(Base):

    def __init__(self, db, request, conversation_id):
        super(Message, self).__init__(db, request)
        
        self.conversation_id = conversation_id

    def create(self):
        """
        Add a new message to an existing conversation and then return the details
        of that message.
        """
    
        # Verify that the request includes both a user_id and message text
        if self.request.json.has_key('text') == False \
            or self.request.json.has_key('user_id') == False:
            raise Exception("Cannot create new message, missing one or more required fields.")
            
        result = self.query('INSERT INTO message (conversation_id, text, user_id) ' +
                            'VALUES (:conversation_id, :text, :user_id) ' +
                            'RETURNING message_id', 
                            {'conversation_id':self.conversation_id, 
                            'text':self.request.json['text'],
                            'user_id':self.request.json['user_id']})

        self.__email_other_recipients(self.conversation_id, self.request.json['user_id'], self.request.json['text'])
        
        self.db.session.commit()
    
        return self.to_json(result)
        
    def handle_mailgun(self):
        
        if self.request.form.has_key('recipient') == False \
            or self.request.form.has_key('sender') == False \
            or self.request.form.has_key('stripped-text') == False:
            raise Exception("Could not process Mailgun message, required fields missing.")
           
        # Extract the conversation_id (12) from 12@sandbox242e1dbbbb1f4c9c94acdb96a5f2f461.mailgun.org
        conversation_id = int(self.request.form['recipient'].split('@')[0])
        sender = self.request.form['sender']
        text = self.request.form['stripped-html'] # stripped-text
        
        # TODO need to sanitize inbound html so nothing dangerous gets passed in
        
        # Verify that the sender email address belongs to a registered user
        result = self.query('SELECT user_id FROM users WHERE email = LOWER(:email)', {"email":sender})
        
        if len(result) == 0:
            raise Exception("Could not add email to conversation, unregistered sender.")
            
        user_id = result[0]['user_id']
        
        # Verify that the sender is a participant in the specified conversation
        result = self.query('SELECT 1 FROM participant WHERE user_id = :user_id AND conversation_id = :conversation_id', 
                                {"conversation_id":conversation_id, "user_id":user_id})
        
        if len(result) == 0:
            raise Exception('Could not add email to conversation, user is not a participant on the conversation.')
        
        # Add the reply to the conversation
        result = self.query('INSERT INTO message (conversation_id, text, user_id) ' +
                            'VALUES (:conversation_id, :text, :user_id) ' +
                            'RETURNING message_id', 
                            {'conversation_id':conversation_id, 
                            'text':text,
                            'user_id':user_id})
    
        
        self.__email_other_recipients(conversation_id, user_id, text)
    
        self.db.session.commit()
    
        return self.to_json(result)

    def __email_other_recipients(self, conversation_id, sender_id, message):
        """Notiy all other participants via email of the new message"""
        
        recipients = self.query('SELECT u.email FROM participant p ' + 
                            'LEFT JOIN users u ' +
                            'ON u.user_id = p.user_id ' +
                            'WHERE p.conversation_id = :conversation_id ' +
                            'AND p.user_id != :sender_id ', {"conversation_id":conversation_id,
                            "sender_id":sender_id});
                            
        for recipient in recipients:
            self.__send_email(conversation_id, recipient['email'], message)
        
        return
        
    def __send_email(self, conversation_id, recipient_email, message):

        # Attempt to retrieve Mailgun API details through OS environment variables first (so it works with Heroku)
        # and defalt back to the config file if the environment variable is not present (so it works locally)
        mailgun_domain = os.environ.get('MAILGUN_DOMAIN', Config.MAILGUN_DOMAIN)
        mailgun_api_key = os.environ.get('MAILGUN_API_KEY', Config.MAILGUN_API_KEY)

        response = requests.post(
            "https://api.mailgun.net/v3/"+mailgun_domain+"/messages",
            auth=("api", mailgun_api_key),
            data={"from": "Knock <"+str(conversation_id)+"@"+mailgun_domain+">",
                  "to": [recipient_email, recipient_email+"@"+mailgun_domain],
                  "subject": "Conversation " + str(conversation_id),
                  "html": '<html>' + message + '</html>'})
        return
        
    def read(self):
        raise Exception("Message::read is not yet implemented.")

    def update(self):
        raise Exception("Message::update is not yet implemented.")

    def delete(self):
        raise Exception("Message::delete is not yet implemented.")
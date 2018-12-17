from base import Base
import json

class Message(Base):

    def __init__(self, db, request, conversation_id):
        super(Message, self).__init__(db, request)
        
        self.conversation_id = conversation_id

    def create(self):
    
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
        text = self.request.form['stripped-text'] # stripped-html
        
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
    
        self.db.session.commit()
    
        return self.to_json(result)

    def read(self):
        raise Exception("Message::read is not yet implemented.")

    def update(self):
        raise Exception("Message::update is not yet implemented.")

    def delete(self):
        raise Exception("Message::delete is not yet implemented.")
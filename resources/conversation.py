from base import Base


class Conversation(Base):

    def __init__(self, db, request, conversation_id):
        super(Conversation, self).__init__(db, request)
        
        self.conversation_id = conversation_id

    def create(self):
        """Create a new conversation between one or more participants."""
        
        if self.request.json.has_key('users') == False:
            raise Exception("Cannot create new conversation, list of users required.")

        # Create a new conversation (right now the conversation table just consists of a conversation_id field)
        result_conversation = self.query('INSERT INTO conversation (conversation_id) ' +
                                        'VALUES (DEFAULT) ' +
                                        'RETURNING conversation_id', {})[0]
                                        
        conversation_id = result_conversation['conversation_id']
        
        # Add each user as a participant to the conversation
        for user in self.request.json['users']:
            result = self.query('INSERT INTO participant (conversation_id, user_id) VALUES (:conversation_id, :user_id)',
                                    {'conversation_id':conversation_id, 'user_id':user['user_id']})
            # TODO raise exception if any of these inserts fail
        
        self.db.session.commit()
        
        return self.to_json(result_conversation)

    def read(self):
        """Returns the full list of messages and participants for a given conversation."""
        
        after_message_id = self.request.args.get('after')
        
        conversation = {"conversation_id":self.conversation_id}
        
        # If the user supplied ?after=:message_id in the request URL query string params
        # then we will only return messages after occurred after the specified message_id
        if after_message_id is not None:
            after_message_id = int(after_message_id)

            conversation['messages'] = self.query('SELECT u.user_name, m.message_id, m.text, m.user_id, to_char(m.sent_dt_tm, \'DD-MON-YYYY HH24:MI TZ\') AS sent_dt_tm ' +
                                    'FROM message m ' +
                                    'JOIN users u ' +
                                    'ON u.user_id = m.user_id ' +
                                    'WHERE m.conversation_id = :conversation_id ' +
                                    'AND m.message_id > :after_message_id', 
                                    {"conversation_id":self.conversation_id, "after_message_id":after_message_id})
            
        # Else retrieve the full conversation, all messages
        # TODO add pagination for conversations with a large number of messages
        else:
            conversation['messages'] = self.query('SELECT u.user_name, m.message_id, m.text, m.user_id, to_char(m.sent_dt_tm, \'DD-MON-YYYY HH24:MI TZ\') AS sent_dt_tm ' +
                                    'FROM message m ' +
                                    'JOIN users u ' +
                                    'ON u.user_id = m.user_id ' +
                                    'WHERE m.conversation_id = :conversation_id', {"conversation_id":self.conversation_id})
            
        
        conversation['participants'] = self.query('SELECT u.user_name, u.user_id ' + 
                                                    'FROM participant p ' + 
                                                    'JOIN users u ' + 
                                                    'ON u.user_id = p.user_id ' + 
                                                    'WHERE p.conversation_id = :conversation_id', 
                                                    {"conversation_id":self.conversation_id});
        
        
        return self.to_json(conversation)

    def update(self):
        raise Exception("Conversation::update is not yet implemented.")

    def delete(self):
        raise Exception("Conversation::delete is not yet implemented.")
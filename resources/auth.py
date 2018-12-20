import uuid, hashlib, datetime
from base import Base


class Auth(Base):

    def __init__(self, db, request):
        super(Auth, self).__init__(db, request)

    def create(self):
        """
        Create a new session for the user by salting their password, hashing it and comparing
        the hashed value with what's stored on the user table.
        """
    
        if self.request.json.has_key('user_name') == False or \
            self.request.json.has_key('password') == False:
            raise Exception("Cannot verify login, username or password missing.")
        
        # Retrieve the salt for the user
        result = self.query('SELECT salt, pw_hash, user_id FROM users WHERE user_name = :user_name'
                            ,{'user_name':self.request.json['user_name']})
        
        # If we didn't find a user with the provided username, then we can't login
        if len(result) == 0:
            raise Exception('Did not find a matching user.')
        
        salt = result[0]['salt']
        user_id = result[0]['user_id']
        
        pw_hash = hashlib.sha512(self.request.json['password'] + salt).hexdigest()
        
        # If our generated hash matches the saved hash, 
        # then we know the user has provided the correct password
        # and we can go create a new session
        if pw_hash == result[0]['pw_hash']:
            session_token = uuid.uuid4().hex
            
            expire = datetime.datetime.now() + datetime.timedelta(minutes=60)
           
            result = self.query('INSERT INTO session (user_id, token, expiration) ' +
                            'VALUES (:user_id, :token, :expiration) ' +
                            'RETURNING session_id, token, user_id', {'user_id':user_id, 
                            'token':session_token,'expiration':expire})
            
            self.db.session.commit()
            
            return self.to_json(result)

    def read(self):
        raise Exception("Auth::read is not yet implemented.")

    def update(self):
        raise Exception("Auth::update is not yet implemented.")

    def delete(self):
        raise Exception("Auth::delete is not yet implemented.")
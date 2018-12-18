import uuid, hashlib
from base import Base


class User(Base):

    def __init__(self, db, request, user_id):
        super(User, self).__init__(db, request)
        
        self.user_id = user_id

    def create(self):
        """Create a new user and return the new user_id."""
    
        if self.request.json.has_key('user_name') == False or \
            self.request.json.has_key('email') == False or \
            self.request.json.has_key('password') == False:
            raise Exception("Cannot create new user, required fields missing.")
        
        # Verify that the username or email address have not already been registered
        result = self.query('SELECT 1 FROM users WHERE email = :email OR user_name = :user_name'
                            ,{'user_name':self.request.json['user_name'], 'email':self.request.json['email']})
                            
        if len(result) > 0:
            raise Exception("Cannot create new user, username or email address already taken.")
        
        # Create a random UUID string that we'll salt the user password with
        salt = uuid.uuid4().hex
        pw_hash = hashlib.sha512(self.request.json['password'] + salt).hexdigest()

        result = self.query('INSERT INTO users (user_name, email, salt, pw_hash) ' +
                            'VALUES (:user_name, :email, :salt, :pw_hash) ' +
                            'RETURNING user_id', {'email':self.request.json['email'].lower(), 
                            'user_name':self.request.json['user_name'].lower(),'salt':salt,'pw_hash':pw_hash})
        
        self.db.session.commit()
        
        return self.to_json(result)

    def read(self):
        """Return a list of all users excluding hashed password data."""
        
        result = self.query('SELECT user_name, user_id, email FROM users', {})
        return self.to_json(result)

    def update(self):
        raise Exception("User::update is not yet implemented.")

    def delete(self):
        raise Exception("User::delete is not yet implemented.")
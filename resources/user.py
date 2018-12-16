from base import Base

class User(Base):

    def __init__(self, db, request, user_id):
        super(User, self).__init__(db, request)

    def create(self):
        return

    def read(self):
        result = self.query('SELECT * FROM users WHERE email = :email', {'email' : 'maggie@mutt.com'} )
        return self.to_json(result)

    def update(self):
        raise Exception("User::update is not yet implemented.")

    def delete(self):
        raise Exception("User::delete is not yet implemented.")
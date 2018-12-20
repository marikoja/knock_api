from abc import abstractmethod
import json

class Base(object):
    def __init__(self, db, request):
        
        self.db = db
        self.request = request
        
    def query(self, sql, pdo):
        """
        Centralized method used for querying against our Postgres database.
        Returns an array of dicts.
        """
        
        result = self.db.session.execute(sql, pdo)
        
        # TODO add error handling for failed queries
        
        # If the query doesn't return any rows (e.g., a typical INSERT, UPDATE or DELETE)
        # then we just return a standard rows affected
        if result.returns_rows == False:
            return [{"rows_affected":result.rowcount}]
        else:
            return [dict(row.items()) for row in result]

    def to_json(self, result):
        # TODO add error handling for bad data or null values
        return json.dumps(result)
    
    # We use abstract methods to force all of our API end-point
    # classes to implement standard CRUD (create, read, update, delete)
    @abstractmethod
    def create(self):
        return 
        
    @abstractmethod
    def read(self):
        return
        
    @abstractmethod
    def update(self):
        return
        
    @abstractmethod
    def delete(self):
        return
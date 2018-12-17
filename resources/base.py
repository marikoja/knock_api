from abc import abstractmethod
import json

class Base(object):
    def __init__(self, db, request):
        
        self.db = db
        self.request = request
        
    def query(self, sql, pdo):
        
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
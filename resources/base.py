from abc import abstractmethod
import json

class Base(object):
    def __init__(self, db, request):
        
        self.db = db
        self.request = request
        
    def query(self, sql, pdo):
        
        rows = self.db.session.execute(sql, pdo)
        
        # TODO add error handling for failed queries
        
        return [dict(row.items()) for row in rows]

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
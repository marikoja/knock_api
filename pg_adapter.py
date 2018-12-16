class PgAdapter:
    def __init__(self, db):
        self.db = db

    def query(self, sql, pdo):
        rows = self.db.session.execute(sql, pdo)
        # TODO add error handling for failed queries
        return [dict(row.items()) for row in rows]

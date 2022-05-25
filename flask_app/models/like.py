from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Like:
    db_name = "bright_ideas"

    def __init__(self,data):
        self.id = data['id']
        self.liked = data['liked']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def like_idea(cls, data):
        query = "INSERT INTO like (user_id, idea_id) VALUES (%(id)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
        
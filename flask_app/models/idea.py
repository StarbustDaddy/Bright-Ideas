from subprocess import CREATE_NEW_CONSOLE
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Idea:
    db_name = "bright_ideas"

    def __init__(self,db_data):
        self.id = db_data['id']
        self.post = db_data['post']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user = user.User.get_by_id({"id": db_data['user_id']})
        self.users = []
        self.likes = []





    @classmethod
    def save(cls,data):
        query = "INSERT INTO idea (post, user_id) VALUES (%(post)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM idea WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)





    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM idea WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def get_all(cls, data):
        query = "SELECT * FROM idea;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        all_ideas = []
        for row in results:
            all_ideas.append( cls(row) )
        return all_ideas



    @classmethod
    def join(cls, data):
        # query = "SELECT users.alias AS user, ideas.post AS brightidea FROM users LEFT JOIN ideas ON users.id = ideas.user_id;"
        query = "SELECT * FROM idea JOIN user ON idea.user_id = user.id;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return []
        else:
            join_ideas = []
            for join_stuff in results:
                join_instance = cls(join_stuff)
                new_user_dictionary = {
                            "id": join_stuff['users.id'],
                            "name": join_stuff['name'],
                            "alias": join_stuff['alias'],
                            "email": join_stuff['email'],
                            "password": join_stuff['password'],
                            "created_at": join_stuff['users.created_at'],
                            "updated_at": join_stuff['users.updated_at'],
                }
                user_instance = user.User(new_user_dictionary)
                join_instance.users = user_instance
                join_ideas.append(join_instance)
            print(join_ideas)
            return join_ideas


    @staticmethod
    def validate_idea(bright_ideas):
        is_valid = True
        if len(bright_ideas['post']) < 2:
            is_valid = False
            flash("Please type out a post","bright_ideas")
        return is_valid
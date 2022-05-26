from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.models import idea
from flask_app.models import like


class User:
    db_name = "bright_ideas"

    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.alias = data['alias']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.ideas = []
        self.likes = []


    @classmethod
    def save(cls,data):
        query = "INSERT INTO user (name,alias,email,password) VALUES(%(name)s,%(alias)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.db_name).query_db(query,data)


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])


    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM user WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def get_all_ideas_with_user( cls , data):
        query = "SELECT * FROM user LEFT JOIN idea ON idea.user_id = user.id WHERE user.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db( query , data )
        this_user = cls(results[0])
        for row in results: 
            i_info = {
                "id" : row["idea.id"],
                "post" : row["post"],
                "user_id" : row["user_id"],
                "created_at" : row["idea.created_at"],
                "updated_at" : row["idea.updated_at"]
            }
            this_user.ideas.append(idea.Idea(i_info))
        return this_user

    @classmethod
    def get_all_likes_with_user( cls , data):
        query = "SELECT * FROM user LEFT JOIN bright_ideas.like ON like.user_id = user.id WHERE user.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db( query , data )
        this_user = cls(results[0])
        for row in results: 
            l_info = {
                "id" : row["like.id"],
                "user_id" : row["user_id"],
                "idea_id" : row['idea_id']
            }
            this_user.likes.append(like.Likes(l_info))
        return this_user


    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL(User.db_name).query_db(query, user)
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email","register")
            is_valid=False
        if len(user['name']) < 2:
            flash("First name must be at least 2 characters","register")
            is_valid= False
        if len(user['alias']) < 2:
            flash("Last name must be at least 2 characters","register")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid= False
        if user['password'] != user['c_password']:
            flash("Passwords don't match","register")
        return is_valid
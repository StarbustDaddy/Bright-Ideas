from flask_app.models.user import User
from flask_app.models.idea import Idea
from flask_app.models.like import Likes
from flask import request, render_template, redirect, session, flash
from flask_app import app

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session["user_id"]
    }

    user = User.get_by_id(data)
    ideas = Idea.get_all(data)
    joins = Idea.join(data)
    likes = User.get_all_likes_with_user(data) 
    return render_template("user_main.html", user=user, idea = ideas, like = likes, join=joins)

# Create
@app.route('/idea/create',methods=['POST'])
def create_idea():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Idea.validate_idea(request.form):
        return redirect('/dashboard')
    data = {
        "post": request.form["post"],
        "user_id": session["user_id"]
    }
    Idea.save(data)
    return redirect('/dashboard')


# Read
@app.route('/idea/<int:id>')
def show_idea(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    joins = Idea.join(data)
    return render_template("idea_list.html", idea=Idea.get_one(data), user=User.get_by_id(data), join=joins)


@app.route('/user/<int:id>')
def user_posts(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("profile.html", idea=User.get_all_ideas_with_user(data), like=User.get_all_likes_with_user(data), user=User.get_by_id(data))

@app.route("/idea/update/<int:id>")
def idea_update(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    joins = Idea.join(data)
    return render_template("edit_idea.html", idea=Idea.get_one(data), user=User.get_by_id(data), join=joins)

#Edit
@app.route("/idea/edit/<int:id>", methods = ["POST"])
def edit_idea(id):
    Idea.get_one({"id": id})
    change = {request.form['post']
            }
    Idea.edit(change)
    return redirect("/idea/<int:id>")


# Delete
@app.route("/idea/<int:id>/delete")
def delete_idea(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Idea.delete(data)
    return redirect("/dashboard")

#Like Idea
@app.route("/idea/like", methods=['POST'])
def like_idea():
    data = {
        "id": request.form["idea_id"],
        "user_id": session["user_id"]
    }
    Likes.like_idea(data)
    return redirect("/dashboard")
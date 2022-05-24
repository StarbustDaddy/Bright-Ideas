from flask_app.models.user import User # not sure what's goin on here
from flask_app.models.idea import Idea
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
    ideas = Idea.get_all()
    return render_template("dashboard.html", user=user, idea=ideas)


#route to show add
@app.route("/idea/new")
def add_idea():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("add_an_idea.html")

# Create
@app.route('/idea/create',methods=['POST'])
def create_idea():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Idea.validate_idea(request.form):
        return redirect('/idea/new')
    data = {
        "post": request.form["post"],
        "user_id": session["user_id"]
    }
    Idea.create(data)
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
    return render_template("display.html",idea=Idea.get_one(data),user=User.get_by_id(user_data))


@app.route('/users/<int:id>')
def user_posts(data):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("user_main", idea=Idea.get_all(data), user=User.get_by_id(id))
        # I am having a hard time with this one guys, I'm truly very sorry. Just a lot going on right now. I think we'll need to implement a new model for this function.




# per our wireframe, there is no editing of posts that I can see. But it's here if you want to imple ment it. Or remove this code; up to you.

# Update
#@app.route("/idea/<int:id>/edit")
#def edit_idea(id):
    #if 'user_id' not in session:
    #    return redirect('/logout')
    #data = {
    #    "id":id
    #}
    #user_data = {
    #    "id":session['user_id']
    #}
    #return render_template("edit_a_idea.html", edit=Idea.get_one(data), user=User.get_by_id(user_data))


#@app.route("/idea/update", methods=["POST"])
#def update_idea():
    #if 'user_id' not in session:
    #    return redirect('/logout')
    #if not Idea.validate_idea(request.form):
    #    return redirect('/ideas/new')
    #data = {
    #    "post": request.form["post"],
    #    "id": request.form['id'],
    #}
    #Idea.update(data)
    #return redirect('/dashboard')




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

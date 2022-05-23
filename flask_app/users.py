from flask_app import app
from flask import render_template, session, redirect, flash, request
from flask_bcrypt import Bcrypt
from flask_app.models.user import User     #Again, not sure what's going on with this error
from flask_app.models.idea import Idea
bcrypt= Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "name": request.form['name'],
        "alias": request.form['alias'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/dashboard')


@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
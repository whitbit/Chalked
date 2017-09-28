from flask import Flask, render_template, redirect, request, flash, session
from model import connect_to_db, db, User, Route, Review, UserLog, UserFavorites

app = Flask(__name__)

app.secret_key = 'ABC'

@app.route('/')
def index():
    """Homepage."""

    return render_template('/homepage.html')

@app.route('/map')
def routes_map():
    """shows all routes on Google map."""

    routes = Route.query.all()
    return render_template('US_map.html', routes=routes)

@app.route('/register', methods=['POST'])
def register_user():
    """Adds user to database."""

    username = request.form.get('username')
    password = request.form.get('password')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    gender = request.form.get('gender')

    user = User.query.filter_by(username=username).first()

    if user:
        flash('You\'ve already registered.  Please login!')
        return redirect('/')
    else:
        user = User(username=username,
                    pw=password,
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender)

        db.session.add(user)

        db.session.commit()
        flash('Successfully registered!')
        return redirect('/')


@app.route('/login', methods=['POST'])
def process_login():
    """checks if user is registered and verifies password."""

    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if user:
        if user.pw == password:
            session['user_id'] = user.user_id

            flash('Logged in!')
            return redirect('/map')
        flash('Invalid password.  Please try again!')

    else: 
        flash('Please register first!')
        return redirect('/')





if __name__ == '__main__':

    app.debug = True

    connect_to_db(app)

    app.run(port=5000, host='0.0.0.0')
from flask import Flask, render_template, redirect, request, flash, session
from model import connect_to_db, db, User, Route, Review, UserLog, UserFavorites
from datetime import datetime

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
            session['username'] = user.username
            session['user_id'] = user.user_id

            flash('Logged in!')
            return redirect('/dashboard')
        flash('Invalid password.  Please try again!')

    else: 
        flash('Please register first!')
        return redirect('/')


@app.route('/dashboard')
def user_dashboard():
    """Displays user dashboard."""

    routes = Route.query.all()
    state = request.args.get('state')
    area = request.args.get('area')

    states = []
    areas = []
    climbs = []

    for route in routes:
        if route.state not in states:
            states.append(route.state)
    
    states.sort()

    state_routes = Route.query.filter_by(state=state).all()


    for route in state_routes:
        if route.area not in areas:
            areas.append(route.area)
            print route.area 

    areas.sort()

    area_routes = Route.query.filter_by(area=area).order_by('v_grade').all()

    for route in area_routes:
        if route not in climbs:
          climbs.append((route.name, route.v_grade))

    return render_template('dashboard.html', states=states, areas=areas, climbs=climbs)


@app.route('/log-climb')
def logs_climb():

    climb_name = request.args.get('route')
    complete = request.args.get('complete')
    notes = request.args.get('notes')
    new_climb = Route.query.filter_by(name=climb_name).one()

    new_log = UserLog(user_id=session['user_id'],
                      route_id=new_climb.route_id,
                      date=datetime.now(),
                      notes=notes,
                      completed=complete)

    db.session.add(new_log)

    db.session.commit()

    flash('successfully logged!')
    
    return redirect('/')


@app.route('/logout', methods=['POST'])
def logs_off_session():
    """Logs user off."""

    del session['username']
    flash('logged out successfully')
    return redirect('/')






if __name__ == '__main__':

    app.debug = True

    connect_to_db(app)

    app.run(port=5000, host='0.0.0.0')
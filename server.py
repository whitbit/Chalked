from flask import Flask, render_template, redirect, request, flash, session, jsonify
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

    return render_template('dashboard.html')


@app.route('/log-climb.json', methods=['POST'])
def logs_climb():
    
    route_id = request.form.get('route_id')

    complete = request.form.get('complete')

    notes = request.form.get('notes')


    new_log = UserLog(user_id=session['user_id'],
                      route_id=route_id,
                      date=datetime.now(),
                      notes=notes,
                      completed=complete)
    print 'ADDED NEW LOG', new_log

    db.session.add(new_log)

    db.session.commit()

    return jsonify({})


@app.route('/logout', methods=['POST'])
def logs_off_session():
    """Logs user off."""

    del session['username']
    flash('logged out successfully')
    return redirect('/')


@app.route('/search.json')
def search_routes_to_log():

    routes = Route.query.all()

    states = sorted(set([route.state for route in routes]))
   
    routes_dict = {}
    
    routes_dict['states'] = states



    state = request.args.get('state')

    state_routes = Route.query.filter_by(state=state).all()

    state_routes = sorted(set([route.area for route in state_routes]))

    routes_dict['areas'] = state_routes



    area = request.args.get('area')

    area_routes = Route.query.filter_by(area=area).all()
    
    route_info = []
    
    for route in area_routes:
        route_info.append([route.v_grade, route.name, route.route_id])


    routes_dict['routes'] = sorted(route_info)

    return jsonify(routes_dict)


@app.route('/user-map.json')
def shoes_user_map_locations():

    user_id = session['user_id']
    print 'USER ID', user_id
    
    user = User.query.get(user_id)
    # get user object
    print 'USER OBJ', user

    user_logged_climbs = user.logs
    # get all log objects of user
    print 'USER LOGS', user_logged_climbs

    coordinates = {}

    for climb in user_logged_climbs:
        route = Route.query.get(climb.route_id)
        # gets route in log
        coordinates[climb.review_id] = (route.latitude, route.longitude)

    print 'COORDINATES', coordinates

    return jsonify(coordinates)



if __name__ == '__main__':

    app.debug = True

    connect_to_db(app)

    app.run(port=5000, host='0.0.0.0')
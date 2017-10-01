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
    climb_name = request.form.get('route')
    print 'climb_name', climb_name

    complete = request.form.get('complete')
    print 'complete', complete
    notes = request.form.get('notes')
    print 'notes', notes
    # new_climb = Route.query.filter_by(name=climb_name).one()



    # new_log = UserLog(user_id=session['user_id'],
    #                   route_id=new_climb.route_id,
    #                   date=datetime.now(),
    #                   notes=notes,
    #                   completed=complete)

    # db.session.add(new_log)

    # db.session.commit()

    print 'sucess!'

    # flash('successfully logged!')
    
    # return redirect('/')

    return jsonify({})

@app.route('/logout', methods=['POST'])
def logs_off_session():
    """Logs user off."""

    del session['username']
    flash('logged out successfully')
    return redirect('/')


@app.route('/search.json')
def search_specific_routes():

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
    route_names = sorted(set([route.name for route in area_routes]))
    area_routes = sorted(set([route.v_grade + ' ' + route.name for route in area_routes]))


    routes_dict['routes'] = area_routes
    routes_dict['route_names'] = route_names

    return jsonify(routes_dict)


if __name__ == '__main__':

    app.debug = True

    connect_to_db(app)

    app.run(port=5000, host='0.0.0.0')
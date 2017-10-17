import os
from flask import Flask, render_template, redirect, request, flash, session, jsonify, url_for, send_from_directory
from model import connect_to_db, db, User, Route, UserLog
from functools import wraps
from sqlalchemy import extract
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import calendar

UPLOAD_FOLDER = './static/photos'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'ABC'




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def requires_login(f):
    @wraps(f)
    def login_check(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in or register first')
            return redirect('/')
        return f(*args, **kwargs)
    return login_check


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



@app.route('/')
def index():
    """Homepage with user registration/login form."""

    return render_template('/homepage.html')


@app.route('/map')
def routes_map():
    """Shows all routes in database on Google map."""

    routes = Route.query.all()

    return render_template('US_map.html', routes=routes)


@app.route('/register', methods=['POST'])
def register_user():
    """Adds user to database."""

    username = request.form.get('username').lower()
    password = request.form.get('password')
    level = request.form.get('level')
    email = request.form.get('email')

    user = User.query.filter_by(username=username).first()

    if user:
        flash('You\'ve already registered.  Please login!')
        return redirect('/')
    else:
        user = User(username=username,
                    pw=password,
                    climb_level=level,
                    email=email)

        db.session.add(user)

        db.session.commit()
        flash('Successfully registered!')
        return redirect('/')


@app.route('/login', methods=['POST'])
def process_login():
    """Checks if user is registered and verifies password."""

    username = request.form.get('username').lower()
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if user:
        if user.pw == password:
            session['username'] = user.username
            session['user_id'] = user.user_id

            flash('Logged in!')
            return redirect('/dashboard')
        flash('Invalid password. Please try again!')
        return redirect('/')


    else: 
        flash('Please register first!')
        return redirect('/')

@app.route('/logout', methods=['POST'])
def logs_off_session():
    """Logs user off."""

    del session['username']
    del session['user_id']
    flash('logged out successfully')
    return redirect('/')

# use password decorator 
@app.route('/dashboard')
@requires_login
def renders_user_dashboard():
    """Displays user dashboard."""

    return render_template('dashboard.html')


@app.route('/upload.json', methods=['POST'])
def upload_file():


    file = request.files['file']
    print file


    if file.filename == '':
        flash('No selected file')
        return jsonify({ 'error': 'no file selected'})
        
    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print 'UPLOADED'

        return jsonify({})
    flash('Please upload a valid file type')
    return jsonify({})




@app.route('/log-climb.json', methods=['POST'])
def logs_climb():
    """Adds new UserLog entry."""

    
    route_id = request.form.get('route_id')

    complete = request.form.get('complete')

    notes = request.form.get('notes')

    rating = request.form.get('rating')

    date = request.form.get('date')

    photo = request.form.get('photo')

    if photo:
        photo = photo.split('\\')[2]


    new_log = UserLog(user_id=session['user_id'],
                      route_id=route_id,
                      date=date,
                      notes=notes,
                      rating=rating,
                      completed=complete,
                      photo=photo
                      )
    # print 'ADDED NEW LOG', new_log

    db.session.add(new_log)

    db.session.commit()

    return jsonify({})


@app.route('/search.json')
def filters_routes_to_log():
    """Filters routes for user to log."""

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


@app.route('/user-info.json')
def renders_user_journal_info():
    """Gets user's log info to render information on dashboard."""


    user_id = session['user_id']

    user = User.query.get(user_id)

    user_logged_climbs = user.logs


    log_info = {}

    log_info['coordinates'] = {}

    log_info['review_info'] = {}

    log_info['map'] = {}

    log_info['completed'] = {}

    log_info['projects'] = {}

    log_info['user_points'] = user.getUserPoints()


    for climb in user_logged_climbs:

        
        route = Route.query.get(climb.route_id)

        date = str(climb.date.date())

        photo = climb.photo

        log_info['coordinates'][climb.review_id] = {'lat': route.latitude, 'lng': route.longitude}

        log_info['map'][climb.review_id] = { 'coordinates': {'lat': route.latitude,
                                                             'lng': route.longitude},
                                             'info_window': (date, 
                                                             route.name,
                                                             route.v_grade,
                                                             route.state,
                                                             route.area,
                                                             photo,
                                                             route.url,
                                                             route.latitude,
                                                             route.longitude) 
                                            }
        if climb.completed == True:
            log_info['completed'][climb.review_id] = (date,
                                                     route.v_grade,
                                                     route.name, 
                                                     route.state,
                                                     route.area,
                                                     climb.rating,
                                                     climb.notes)
        if climb.completed == False:
            log_info['projects'][climb.review_id] = (date,
                                                    route.v_grade,
                                                    route.name,
                                                    route.state,
                                                    route.area,
                                                    climb.rating,
                                                    climb.notes,
                                                    climb.review_id)


    return jsonify(log_info)

@app.route('/user-map')
@requires_login
def renders_user_map():

    return render_template('user_map.html')


@app.route('/user-chart.json')
def user_charts_data():
    """Queries user log data for bubble chart generation"""

    user_id = session['user_id']

    # current_year = datetime.now().year

    last_twelve_months = datetime.now() - timedelta(365)

    # year_logs = db.session.query(UserLog).filter(extract('year', UserLog.date) == current_year, 
    #                                              UserLog.user_id == user_id).all()

    year_logs = db.session.query(UserLog).filter(UserLog.date > last_twelve_months, 
                                                 UserLog.user_id == user_id,
                                                 UserLog.completed == True).all()


    """Creates dictionary of climbs attempted per month and vgrade.  Keeps track of counts"""

    climbs = {}

    data = {}

    for log in year_logs:

        name = Route.query.get(log.route_id).name

        v_grade = Route.query.get(log.route_id).v_grade
        
        month = log.date.month

        year = log.date.year

        climbs[(year, month, v_grade)] = climbs.setdefault((year, month, v_grade), 0) + 1

    data['datasets'] = []

    for climb in climbs:

        # send a date format accepted by Moments into chart.js
        date = str(climb[0]) + '-' + '%02d' % climb[1] + '-01' 


        v_grade = climb[2]

        data['datasets'].append({
                'label': 'V' + str(v_grade),
                'data': [{
                    'x': date,
                    'y': v_grade,
                    'r': 23 * climbs[climb]
                }],
                'backgroundColor': 'rgba(193,46,12,0.6)',
                'hoverBackgroundColor': 'rgba(193,46,12,0.8)'
        })


    return jsonify(data)

@app.route('/update-log.json')
def updates_review_log():

    print 'HELLO'

    return jsonify({})



if __name__ == '__main__':

    app.debug = True

    connect_to_db(app)

    app.run(port=5000, host='0.0.0.0')
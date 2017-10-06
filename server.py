import os
from flask import Flask, render_template, redirect, request, flash, session, jsonify, url_for, send_from_directory
from model import connect_to_db, db, User, Route, UserLog, UserFavorites
from functools import wraps
from werkzeug.utils import secure_filename

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
        if 'user_id' not in session:
            flash('Please log in or register first')
            return redirect('/')


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

    username = request.form.get('username')
    password = request.form.get('password')
    level = request.form.get('level')

    user = User.query.filter_by(username=username).first()

    if user:
        flash('You\'ve already registered.  Please login!')
        return redirect('/')
    else:
        user = User(username=username,
                    pw=password,
                    climb_level=level,
                    last_name=last_name)

        db.session.add(user)

        db.session.commit()
        flash('Successfully registered!')
        return redirect('/')


@app.route('/login', methods=['POST'])
def process_login():
    """Checks if user is registered and verifies password."""

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

@app.route('/logout', methods=['POST'])
def logs_off_session():
    """Logs user off."""

    del session['username']
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
    print 'ADDED NEW LOG', new_log

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

    log_info['user_points'] = user.getUserPoints()


    for climb in user_logged_climbs:

        
        route = Route.query.get(climb.route_id)

        date = str(climb.date.date())

        photo = climb.photo

        log_info['coordinates'][climb.review_id] = {'lat': route.latitude, 'lng': route.longitude}

        log_info['review_info'][climb.review_id] = (date,
                                                    route.name, 
                                                    route.state,
                                                    route.area,
                                                    route.v_grade,
                                                    climb.rating,
                                                    climb.notes,
                                                    climb.completed)
        log_info['map'][climb.review_id] = { 'coordinates': {'lat': route.latitude, 'lng': route.longitude},
                                             'info_window': (date, route.name, route.v_grade, route.state, route.area, photo, route.url, route.latitude, route.longitude) }


    return jsonify(log_info)

@app.route('/user-map')
@requires_login
def renders_user_map():

    return render_template('user_map.html')


if __name__ == '__main__':

    app.debug = True

    connect_to_db(app)

    app.run(port=5000, host='0.0.0.0')
from flask import Flask, render_template, redirect, request
from model import connect_to_db, db, User, Route, Review, UserLog, UserFavorites

app = Flask(__name__)

app.secret_key = 'ABC'

@app.route('/')
def index():
    """Homepage."""

    pass

@app.route('/map')
def routes_map():
    """shows all routes on Google map."""

    routes = Route.query.all()
    return render_template('US_map.html', routes=routes)





if __name__ == '__main__':

    app.debug = True

    connect_to_db(app)

    app.run(port=5000, host='0.0.0.0')
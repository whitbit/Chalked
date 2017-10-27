# Chalked

Chalked is a fullstack web application for tracking outdoor rockclimbing experiences. Keep track of completed climbs and projects you'd like to return to. Visualize your progress over time, and earn badges along the way! Additionally, integration with the Google Maps API allows users to build a roadmap of places they've visited. ![Chalked Homepage](/static/homepage.png)


## Table of Contents
* [Technologies Used] (#technologiesused)
* [How to locally run Chalked] (#run)


## <a name="technologiesused"></a>Technologies Used

* Python
* Javascript/jQuery
* Flask
* PostgresSQL
* SQLAlchemy
* AJAX/JSON
* HTML/CSS
* Jinja2
* Chart.js
* Bcrypt
* Scrapy
* Bootstrap
* Google Maps API
* Mountain Project API

## <a name="run"></a>How to locally run Chalked
Chalked is not deployed yet, but stay tuned!

For now:

* Set up and activate a python virtualinv
    * `pip install -r requirements.text`
* Run PostgreSQL and create a new database named vroutes:
    * `psql`
    * `createdb vroutes`
* Seed Mountain Project routes data into database
    * `python seed.py`
* Start up the flask server
    * `python server.py`
* Go to localhost:5000 to see the home page




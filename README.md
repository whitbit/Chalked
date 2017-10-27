# Chalked

Chalked is a fullstack web application for tracking outdoor rockclimbing experiences. Securely keep track of completed climbs and projects you'd like to return to. Visualize your progress over the past twelve months, and earn badges via vpoints along the way! Users with over 100 points in climbs completed earn the title of Mountain Goat! Integration with the Google Maps API allows users to build a roadmap of places they've visited. User logs are rendered dynamically via AJAX. ![Chalked Homepage](/static/homepage.png)
![Chalked User Log](/static/log.png)
![Chalked Map](/static/map.png)


## Table of Contents
* [Technologies Used](#technologiesused)
* [How to locally run Chalked](#run)


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
* Selenium
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




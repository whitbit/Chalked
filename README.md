# Chalked

Chalked is a fullstack web application for tracking outdoor rockclimbing experiences. Search for top routes within the US, securely keep track of completed climbs and projects you'd like to return to. Upload photos and visualize your progress over the past twelve months, and earn badges via v-points. Users with over 100 points in climbs completed earn the title of Mountain Goat! Integration with the Google Maps API allows users to build a roadmap of places they've visited. ![Chalked Homepage](/static/homepage.png)

[a link](https://chalked.herokuapp.com)

![Chalked User Log](/static/log.png)
![Chalked New Log](/static/new_log.png)
![Chalked Map](/static/map.png)
![Chalked User](/static/user-photo.png)


## Table of Contents
* [Technologies Used](#technologiesused)
* [How to locally run Chalked](#run)
* [Credits](#credits)


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
Chalked is now deployed on: [a link](https://chalked.herokuapp.com)


Alternatively:

* Set up and activate a python virtualenv
    * `pip install -r requirements.text`
* Run PostgreSQL and create a new database named vroutes:
    * `psql`
    * `createdb vroutes`
* Seed Mountain Project routes data into database
    * `python seed.py`
* Start up the flask server
    * `python server.py`
* Go to localhost:5000 to see the home page

## <a name="credits"></a>Credits

* My friends, mentors, TAs, and instructors at Hackbright http://www.hackbrightacademy.com
* Snazzy Maps design: http://simey.me 
* Mountain Project for routes data: https://www.mountainproject.com/data
* Homepage photo cred goes to my friend Yi Sun! www.yisunphotography.com/






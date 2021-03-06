from sqlalchemy import func
from model import User, Route, UserLog, connect_to_db, db
from server import app
from datetime import datetime
from faker import Faker
from random import randint
import requests, os, json

TOKEN = os.environ.get('MOUNTAIN_PROJECT_TOKEN')


def getRouteIds(file):
    """Gets all route IDs out of json file."""

    routes_file = open(file)
    routes = routes_file.read()
    routes_file.close()

    routes_dict = json.loads(routes)

    route_ids = []

    for page in routes_dict:
        for route in page:
            route_ids.append(page[route])

    return route_ids


def load_routes():
    """Loads database with routes from Mountain Project API."""

    route_ids = getRouteIds('routes.json')

    Route.query.delete()

    for i in range(len(route_ids))[::100]: 

        payload = {
            'routeIds': ','.join(route_ids[i:i+100]),
            'key': TOKEN
        }

        r = requests.get('https://www.mountainproject.com/data/get-routes', params=payload).json()

        for route in r['routes']:
            if validates_vgrade(route['rating']):  
              route = Route(name=route['name'],
                            latitude=route['latitude'],
                            longitude=route['longitude'],
                            state=route['location'][0],
                            area=route['location'][1],
                            v_grade=route['rating'][1:2],
                            url=route['url'],
                            img=route['imgSmallMed'])

              db.session.add(route)

        db.session.commit()


def validates_vgrade(grade):
  
  return grade[0] == 'V' and grade[1].isdigit()


if __name__ == "__main__":
    connect_to_db(app, os.environ.get("DATABASE_URL"))

    db.create_all()
    load_routes()
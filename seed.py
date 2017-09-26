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

route_ids = getRouteIds('routes.json')


def get_data():

    for i in range(len(route_ids))[::200]: 

        payload = {
            'routeIds': ','.join(route_ids[i:i+200]),
            'key': TOKEN
        }

        response = requests.get('https://www.mountainproject.com/data/get-routes', params=payload)

        print response

    return response

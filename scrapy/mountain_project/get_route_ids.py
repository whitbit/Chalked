import json

def getRouteIds():
    """Gets all route IDs out of json file."""

    routes_file = open('routes.json')
    routes = routes_file.read()
    routes_file.close()

    routes_dict = json.loads(routes)

    route_ids = []

    for page in routes_dict:
        for route in page:
            route_ids.append(page[route])

    return route_ids


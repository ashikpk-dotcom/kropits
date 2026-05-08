from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from django.utils.translation import gettext_lazy as _
import math

def optimize_delivery_routes(deliveries):
    if not deliveries:
        return []

    num_vehicles = len(deliveries)
    depot = 0

    distance_matrix = create_distance_matrix(deliveries)

    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), num_vehicles, depot)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        return format_solution(manager, routing, solution, deliveries)
    return []


def create_distance_matrix(deliveries):
    n = len(deliveries)
    matrix = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j:
                loc1 = deliveries[i]['location']
                loc2 = deliveries[j]['location']
                matrix[i][j] = int(calculate_distance(loc1, loc2) * 1000)
    return matrix


def calculate_distance(loc1, loc2):
    from math import radians, cos, sin, asin, sqrt

    lon1, lat1 = loc1
    lon2, lat2 = loc2

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r


def format_solution(manager, routing, solution, deliveries):
    routes = []
    for vehicle_id in range(routing.vehicles()):
        index = routing.Start(vehicle_id)
        route = []
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route.append({
                'order_id': deliveries[node_index].get('order_id'),
                'location': deliveries[node_index]['location'],
            })
            index = solution.Value(routing.NextVar(index))
        if route:
            routes.append({
                'vehicle_id': vehicle_id,
                'route': route,
                'distance': calculate_route_distance(route),
            })
    return routes


def calculate_route_distance(route):
    total = 0
    for i in range(len(route) - 1):
        total += calculate_distance(route[i]['location'], route[i+1]['location'])
    return total

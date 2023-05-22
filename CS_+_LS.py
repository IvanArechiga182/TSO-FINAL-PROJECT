import math
import random

def read_file(file_name):
    with open(file_name) as f:
        data = f.readlines()
        time_limit, start_point = map(int, data[0].strip().split())
        points = []
        for line in data[1:]:
            x, y, score = map(float, line.strip().split())
            points.append((x, y, score))
    return time_limit, start_point, points

def euclidean_distance(point1, point2):
    x1, y1, _ = point1
    x2, y2, _ = point2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def calculate_score(route):
    return sum(point[2] for point in route)

def calculate_remaining_time(current_time, start_time, time_limit):
    return time_limit - (current_time - start_time)

def generate_initial_solution(points, start_point, time_limit):
    route = [points[start_point]]
    unvisited_points = set(points)
    unvisited_points.remove(points[start_point])
    remaining_time = time_limit

    while unvisited_points:
        next_point = find_nearest_point(route[-1], unvisited_points, remaining_time)
        if next_point is None:
            break

        distance = euclidean_distance(route[-1], next_point)
        if distance > remaining_time:
            break

        route.append(next_point)
        unvisited_points.remove(next_point)
        remaining_time -= distance

    return route

def swap_points(route, i, j):
    # Intercambia dos puntos en la ruta
    route[i], route[j] = route[j], route[i]

def find_nearest_point(current_point, points, remaining_time):
    min_distance = float("inf")
    nearest_point = None
    for point in points:
        distance = euclidean_distance(current_point, point)
        if distance < min_distance and distance <= remaining_time:
            min_distance = distance
            nearest_point = point
    return nearest_point

def local_search_optimization(file_name):
    time_limit, start_point, points = read_file(file_name)
    best_route = generate_initial_solution(points, start_point, time_limit)
    best_score = calculate_score(best_route)
    improved = True
    
    while improved:
        improved = False
        
        for i in range(len(best_route)):
            for j in range(i + 1, len(best_route)):
                new_route = list(best_route)
                swap_points(new_route, i, j)
                new_score = calculate_score(new_route)
                
                if new_score > best_score:
                    best_route = new_route
                    best_score = new_score
                    improved = True
                    break
                    
            if improved:
                break
    
    return best_score, best_route

score, route = local_search_optimization('test_instance.txt')
print("Total score: ", score)
print("Route: ", route)


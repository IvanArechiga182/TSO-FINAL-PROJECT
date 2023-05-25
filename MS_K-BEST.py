import math
import random

def read_file(file_name):
    with open(file_name) as f:
        data = f.readlines()
        time_limit, num_paths = map(int, data[0].strip().split())
        points = []
        for line in data[1:]:
            x, y, score = map(float, line.strip().split())
            points.append((x, y, score))
    return time_limit, num_paths, points

def euclidean_distance(point1, point2):
    x1, y1, _ = point1
    x2, y2, _ = point2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def calculate_score(route):
    return sum(point[2] for point in route)

def generate_initial_solution(points, time_limit):
    start_point = points[0]
    end_point = points[-1]
    unvisited_points = set(points[1:-1])
    remaining_time = time_limit - euclidean_distance(start_point, end_point)
    route = [start_point]

    while unvisited_points and remaining_time > 0:
        next_point = find_nearest_point(route[-1], unvisited_points, remaining_time)
        if next_point is None:
            break

        distance = euclidean_distance(route[-1], next_point)
        if distance > remaining_time:
            break

        route.append(next_point)
        unvisited_points.remove(next_point)
        remaining_time -= distance

    route.append(end_point)
    return route

def swap_points(route, i, j):
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

def local_search_optimization(route, time_limit):
    best_route = route[:]
    best_score = calculate_score(best_route)
    improved = True
    
    while improved:
        improved = False
        
        for i in range(len(best_route)):
            for j in range(i + 1, len(best_route)):
                new_route = best_route[:]
                swap_points(new_route, i, j)
                new_score = calculate_score(new_route)
                
                if new_score > best_score:
                    best_route = new_route
                    best_score = new_score
                    improved = True
                    break
                    
            if improved:
                break
    
    return best_route, best_score

def multi_start_strategy(file_name, num_starts):
    time_limit, num_paths, points = read_file(file_name)
    best_route = None
    best_score = 0
    
    for _ in range(num_starts):
        route = generate_initial_solution(points, time_limit)
        route, score = local_search_optimization(route, time_limit)
        
        if score > best_score:
            best_route = route
            best_score = score
    
    return best_route, best_score

best_route, best_score = multi_start_strategy('test_instance.txt', 3)
print("Total score:", best_score)
print("Route:", best_route)

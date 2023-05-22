import math

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

def find_nearest_unvisited_point(current_point, points, visited_points):
    min_distance = float("inf")
    nearest_point = None
    for point in points:
        if point not in visited_points:
            distance = euclidean_distance(current_point, point)
            if distance < min_distance:
                min_distance = distance
                nearest_point = point
    return nearest_point

def orienteering_heuristic(file_name):
    time_limit, start_point, points = read_file(file_name)
    visited_points = set()
    current_point = points[start_point]
    score = 0
    time_remaining = time_limit
    
    while len(visited_points) < len(points):
        nearest_point = find_nearest_unvisited_point(current_point, points, visited_points)
        if nearest_point is None:
            break
        
        distance = euclidean_distance(current_point, nearest_point)
        if time_remaining - distance < 0:
            break
        
        score += nearest_point[2]
        visited_points.add(nearest_point)
        time_remaining -= distance
    
    return score, visited_points

score, route = orienteering_heuristic('test_instance.txt')
print("Total score: ", score)
print("Route: ", route)







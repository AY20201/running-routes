from collections import deque
from data import get_osm_nodes
from data import get_closest_node_to_point
from data import get_elevation_change
import data
from geographic_math import get_distance
import time
import random

class Loop:
    path = []
    distance = 0.0
    center_point = []
    elevation_gain = 0.0

    def __init__(self, path, distance, center_point, elevation_gain):
        self.path = path
        self.distance = distance
        self.center_point = center_point
        self.elevation_gain = elevation_gain

def create_loop(path, distance):
    
    avg_point = [0.0, 0.0]
    for n in path:
        avg_point[0] += data.current_nodes[n].location[0]
        avg_point[1] += data.current_nodes[n].location[1]
    avg_point[0] /= len(path)
    avg_point[1] /= len(path)

    elevation_gain = 0.0 #get_elevation_change(path)

    return Loop(path, distance, avg_point, elevation_gain)

def dfs(node, distance, target_distance_min, target_distance_max, origin_index, path, loops, max_loops, dist_dict):
    #max is set because we could find all loops (if distance is small) but with big distance it will take too long
    current_node = data.current_nodes[node]
    #if more than desired path distance has been searched, or shortest possible distance exceeds target, terminate branch
    #or 
    if distance > target_distance_max or len(loops) >= max_loops:
        return
    
    if distance > target_distance_min / 2:
        if distance + get_distance(current_node.location, data.current_nodes[origin_index].location) > target_distance_max:
            return

    neighbors = current_node.neighbor_indices
    if origin_index in neighbors and len(path) > 1 and distance >= target_distance_min and distance <= target_distance_max:
        #loops.append(path[:])
        new_path = path[:]
        new_path.append(node)
        new_path.append(origin_index)
        loops.append(create_loop(new_path, distance))
        return
    
    path.append(node)

    randomized_neighbors = neighbors
    random.shuffle(randomized_neighbors)
    for neighbor in randomized_neighbors:
        neighbor_node = data.current_nodes[neighbor]
        if neighbor not in path:
            if (node, neighbor) not in dist_dict:
                dist_dict[(node, neighbor)] = get_distance(current_node.location, neighbor_node.location)
            dfs(neighbor, distance + dist_dict[(node, neighbor)], target_distance_min, target_distance_max, origin_index, path, loops, max_loops, dist_dict)

    path.pop()

def dfs_optimized(node, target_distance_min, target_distance_max, origin_index, path, loops, max_loops):
    #max is set because we could find all loops (if distance is small) but with big distance it will take too long
    current_node = data.current_nodes[node]

    #will adjust 800 later
    if len(path) * 0.015 > target_distance_max or len(loops) >= max_loops:
        return

    neighbors = current_node.neighbor_indices
    if origin_index in neighbors and len(path) > 1 and len(path) * 0.013 > target_distance_min:
        #loops.append(path[:])
        loop_distance = 0.0
        for i in range(1, len(path)):
            if i % 2 == 0:
                loop_distance += get_distance(data.current_nodes[path[i - 2]].location, data.current_nodes[path[i]].location)

        if loop_distance >= target_distance_min and loop_distance <= target_distance_max:
            loops.append(create_loop(path[:], origin_index, loop_distance))
            return
    
    path.append(node)

    for neighbor in neighbors:
        if neighbor not in path: 
            dfs_optimized(neighbor, target_distance_min, target_distance_max, origin_index, path, loops, max_loops)

    path.pop()

def convert_loops_to_dict(loops):
    loops_dict = { "loops":[] }
    for loop in loops:
        new_dict = { "path":[], "distance":loop.distance, "center":loop.center_point }
        for node in loop.path:
            new_dict["path"].append(data.current_nodes[node].location)
        loops_dict["loops"].append(new_dict)
    return loops_dict

def get_loops(starting_location, target_distance_min, target_distance_max, kilometers, loop_count):
    if kilometers: #target distances coming in as km, convert them to miles
        target_distance_min = target_distance_min * 0.6213
        target_distance_max = target_distance_max * 0.6213

    get_osm_nodes(starting_location, target_distance_max / 4.0)
    starting_node_index = get_closest_node_to_point(starting_location)
    
    max_loops = loop_count
    if loop_count == 0:
        max_loops = max(int(((8.0 - target_distance_max) / 8 + (10000 - len(data.current_nodes)) / 10000) / 2.0 * 35), 1)

    loops = []
    dfs(starting_node_index, 0, target_distance_min, target_distance_max, starting_node_index, [], loops, max_loops, {})
    #dfs_optimized(starting_node_index, target_distance_min, target_distance_max, starting_node_index, [], loops, max_loops)
    return loops
"""
start_time = time.time()
#loops = get_loops([42.3752760, -71.3355820], 5.90, 6.00) #in wayland
loops = get_loops([42.37566157427506, -71.33491550075408], 3.05, 3.10)
print("completed in " + str(time.time() - start_time))

print(len(loops))
if len(loops) > 0:
    print("loop 10")
    print(str(loops[0].distance) + " miles")
    for node in loops[0].path:
        print("node(" + str(data.current_nodes[node].id) + ");") #so I can put this in overpass turbo
"""
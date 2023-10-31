import requests
from geographic_math import get_distance

current_nodes = []

class Node:
    id = 0
    belonging_way_id = 0
    location = []
    neighbor_indices = []
    elevation = 0.0

    def __init__(self, id, belonging_way_id, latitude, longitude, elevation):
        self.id = id;
        self.belonging_way_id = belonging_way_id
        self.location = [latitude, longitude]
        self.neighbor_indices = []
        self.elevation = elevation

def get_node_of_id(id):
    for i in range(len(current_nodes)):
        if current_nodes[i].id == id:
            return i #only gets first occurance. Doesn't matter though
    return -1

def get_closest_node_to_point(location):
    current_closest_dist = 100000.0
    current_closest_index = 0
    for i in range(len(current_nodes)):
        node_distance = get_distance(current_nodes[i].location, location)
        if(node_distance < current_closest_dist):
            current_closest_dist = node_distance
            current_closest_index = i
    return current_closest_index #not exactly that effecient but should be fine

#def trim_node_neighbors(nodes):
def delete_duplicates(nodes, node_ids):
    for i in range(len(nodes)):
        for j in range(len(nodes[i].neighbor_indices)):
            if node_ids.count(nodes[nodes[i].neighbor_indices[j]].id) > 1:
                nodes[i].neighbor_indices[j] = node_ids.index(nodes[nodes[i].neighbor_indices[j]].id)


def get_node_neighbors(nodes):
    node_ids = []
    for i in range(len(nodes)):
        node_ids.append(nodes[i].id)

    for i in range(len(nodes)): #first pass, get neighbors that belong to the same way
        neighbors = [i + 1, i - 1]
        for j in range(2):
            if neighbors[j] < len(nodes) and neighbors[j] >= 0:
                if nodes[i].belonging_way_id == nodes[neighbors[j]].belonging_way_id:
                    nodes[i].neighbor_indices.append(neighbors[j])
    
    for i in range(len(nodes)): #second pass: get neighbors that belong to different ways
        if node_ids.count(nodes[i].id) > 1:
            for j in range(len(nodes)):
                if i != j:
                    if nodes[i].id == nodes[j].id and nodes[i].belonging_way_id != nodes[j].belonging_way_id:
                        nodes[i].neighbor_indices += nodes[j].neighbor_indices
    delete_duplicates(nodes, node_ids)


def congfigure_node_data(json_data):
    nodes = []

    for way in json_data["elements"]:
        for i in range(len(way["nodes"])):
            location = way["geometry"][i]
            new_node = Node(way["nodes"][i], way["id"], location["lat"], location["lon"], 0.0)
            nodes.append(new_node)

    #get_elevation_data(nodes)
    get_node_neighbors(nodes)
    return nodes

def get_osm_nodes(center, radius_in_miles):

    overpass_url = "https://overpass-api.de/api/interpreter"
    rad_in_meters = radius_in_miles * 1609.34
    search_circle = str(rad_in_meters) + "," + str(center[0]) + "," + str(center[1])

    query = """
    [out:json][timeout:25];
    (
    way(around:{boundary})[highway~"^(secondary|tertiary|unclassified|residential|path|track|cycleway)$"];
    );
    out geom;
    """
    query = query.format(boundary = search_circle)

    response = requests.get(overpass_url, params={"data": query})
    data = response.json()

    global current_nodes
    current_nodes = congfigure_node_data(data)
    #print(len(current_nodes))
    #osmpy.get(query, search_circle)

def get_elevation_data(nodes):
    url = "https://api.open-elevation.com/api/v1/lookup"

    locations = {"locations":[]}
    for node in nodes:
        locations["locations"].append({"latitude": node.location[0], "longitude": node.location[1]})
    
    response = requests.post(url, json=locations, verify=False)
    elevation_data = response.json()

    for i in range(len(nodes)):
        nodes[i].elevation = elevation_data["results"][i]["elevation"]
    """
    elevation_gain = 0 #higher number means more hills
    previous_elevation = 100000

    if elevation_data.get('results'):
        for result in elevation_data['results']:
            elevation = result['elevation']
            if elevation > previous_elevation:
                elevation_gain += elevation - previous_elevation
            previous_elevation = elevation
    return elevation_gain
    """

def get_elevation_change(path):
    elevation_gain = 0 #higher number means more hills
    previous_elevation = current_nodes[path[0]].elevation

    for node in path:
        elevation = current_nodes[node].elevation
        if elevation > previous_elevation:
            elevation_gain += elevation - previous_elevation
        previous_elevation = elevation

    return elevation_gain
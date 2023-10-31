import math

earth_radius = 3960.0
degrees_to_radians = math.pi/180.0
radians_to_degrees = 180.0/math.pi

def get_distance(p1, p2): #   p2 = next point, p1 = current point
    #return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
    if p1 == p2:
        return 0.0

    earth_radius = 3956
    lon1 = math.radians(p1[1])
    lon2 = math.radians(p2[1])
    lat1 = math.radians(p1[0])
    lat2 = math.radians(p2[0])
    
    ratio = math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2)* math.cos(lon2-lon1)
    ratio = max(min(ratio, 1.0), -1.0) #make sure it doesn't go out of acos range

    distance = math.acos(ratio) * earth_radius

    return distance
    

def change_in_latitude(miles):
    return (miles/earth_radius)*radians_to_degrees

def change_in_longitude(latitude, miles):
    r = earth_radius*math.cos(latitude*degrees_to_radians)
    return (miles/r)*radians_to_degrees
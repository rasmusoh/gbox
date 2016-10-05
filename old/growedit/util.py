import math

def endpoint(startpoint, direction, length):
    return (startpoint[0]+length*math.cos(direction),startpoint[1]+length*math.sin(direction))

def distance(startpoint, endpoint):
    return math.sqrt(distance2(startpoint, endpoint))

def distance2(startpoint, endpoint):
    return (endpoint[0] - startpoint[0])**2 + (endpoint[1] - startpoint[1])**2

def angle(startpoint, endpoint):
    return atan2(endpoint[1] - startpoint[1], endpoint[0] - startpoint[0])

def vector(startpoint, endpoint):
    return (endpoint[0] - startpoint[0], endpoint[1] - startpoint[1])

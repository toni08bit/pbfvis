def _orientation(p,q,r):
    value = ((q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1]))
    if (value == 0):
        return 0 # Collinear
    elif (value > 0):
        return 1 # Clockwise
    else:
        return 2 # Counterclockwise
    
def _on_segment(p,q,r):
    return (min(p[0],q[0]) <= r[0] <= max(p[0],q[0]) and min(p[1],q[1]) <= r[1] <= max(p[1],q[1]))

def segment_intersect(p1,q1,p2,q2):
    o1 = _orientation(p1,q1,p2)
    o2 = _orientation(p1,q1,q2)
    o3 = _orientation(p2,q2,p1)
    o4 = _orientation(p2,q2,q1)

    if (o1 != o2) and (o3 != o4):
        return True

    if ((o1 == 0) and _on_segment(p1,q1,p2)):
        return True
    if ((o2 == 0) and _on_segment(p1,q1,q2)):
        return True
    if ((o3 == 0) and _on_segment(p2,q2,p1)):
        return True
    if ((o4 == 0) and _on_segment(p2,q2,q1)):
        return True

    return False

def polygon_area(vertices):
    vertices_length = len(vertices)
    total_area = 0
    for i in range(vertices_length):
        x0,y0 = vertices[i]
        x1,y1 = vertices[(i + 1) % vertices_length]
        total_area = (total_area + (x0 * y1 - y0 * x1))
    return abs(total_area / 2)

# p1 = (0,0)
# q1 = (0,0)
# p2 = (-3,7)
# q2 = (-7,7)

# print(segment_intersect(p1, q1, p2, q2))

# print(polygon_area([
#     (1,1),
#     (1,4),
#     (4,4),
#     (4,1),
#     (7,4),
#     (7,0),
#     (1,0)
# ]))
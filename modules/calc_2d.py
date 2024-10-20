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

# p1 = (0,0)
# q1 = (0,0)
# p2 = (-3,7)
# q2 = (-7,7)

# print(segment_intersect(p1, q1, p2, q2))
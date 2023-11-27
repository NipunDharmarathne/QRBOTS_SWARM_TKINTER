import math

def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

def calculate_bearing(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    angle = math.atan2(x2 - x1, y2 - y1)
    # Convert angle from radians to degrees
    angle_degrees = math.degrees(angle)
    return angle_degrees

# Example usage:
point1 = (0, 0)
point2 = (-3, 4)

distance = calculate_distance(point1, point2)
angle = calculate_bearing(point1, point2)

print(f"Distance between points: {distance}")
print(f"Angle between points: {angle} degrees")

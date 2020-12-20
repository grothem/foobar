"""
Bringing a Gun to a Guard Fight
===============================

Uh-oh - you've been cornered by one of Commander Lambdas elite guards! Fortunately, you grabbed a beam weapon from an abandoned guard post while you were running
through the station, so you have a chance to fight your way out. But the beam weapon is potentially dangerous to you as well as to the elite guard: its beams reflect
off walls, meaning you'll have to be very careful where you shoot to avoid bouncing a shot toward yourself!

Luckily, the beams can only travel a certain maximum distance before becoming too weak to cause damage. You also know that if a beam hits a corner, it will bounce
back in exactly the same direction. And of course, if the beam hits either you or the guard, it will stop immediately (albeit painfully).

Write a function solution(dimensions, your_position, guard_position, distance) that gives an array of 2 integers of the width and height of the room, an array of 2
integers of your x and y coordinates in the room, an array of 2 integers of the guard's x and y coordinates in the room, and returns an integer of the number of
distinct directions that you can fire to hit the elite guard, given the maximum distance that the beam can travel.

The room has integer dimensions [1 < x_dim <= 1250, 1 < y_dim <= 1250]. You and the elite guard are both positioned on the integer lattice at different
distinct positions (x, y) inside the room such that [0 < x < x_dim, 0 < y < y_dim]. Finally, the maximum distance that the beam can travel before
becoming harmless will be given as an integer 1 < distance <= 10000.

For example, if you and the elite guard were positioned in a room with dimensions [3, 2], your_position [1, 1], guard_position [2, 1], and a maximum shot distance of
4, you could shoot in seven different directions to hit the elite guard (given as vector bearings from your location): [1, 0], [1, 2], [1, -2], [3, 2], [3, -2], [-3,
2], and [-3, -2]. As specific examples, the shot at bearing [1, 0] is the straight line horizontal shot of distance 1, the shot at bearing [-3, -2] bounces off the
left wall and then the bottom wall before hitting the elite guard with a total shot distance of sqrt(13), and the shot at bearing [1, 2] bounces off just the top
wall before hitting the elite guard with a total shot distance of sqrt(5).
"""
import math

def solution(dimensions, your_position, guard_position, distance):
    # calculate all of the possible positions of you and the guard in the first quardrant
    your_side_points = mirror_on_side_wall(dimensions[0], your_position[0], distance)
    your_top_points = mirror_on_top_wall(dimensions[1], your_position[1], distance)

    your_points = []
    for i in your_top_points:
        for j in your_side_points:
            your_points.append([j, i])

    guard_side_points = mirror_on_side_wall(dimensions[0], guard_position[0], distance)
    guard_top_points = mirror_on_top_wall(dimensions[1], guard_position[1], distance)

    the_guard_points = []
    for i in guard_top_points:
        for j in guard_side_points:
            the_guard_points.append([j, i])

    # now reflect those positions across the x and y axis to give us all possible locations of you and the guard
    your_points += reflect_on_x_axis(your_points)
    your_points += reflect_on_y_axis(your_points)

    the_guard_points += reflect_on_x_axis(the_guard_points)
    the_guard_points += reflect_on_y_axis(the_guard_points)

    # determine what angles result in a shot that hits you
    solution = set()
    angles = {}
    for p in your_points:
        if (p == your_position): continue
        angle = shot_angle(your_position, p)
        d = distance_between(your_position, p)
        if ((angle in angles and angles[angle] > d) or angle not in angles):
            angles[angle] = d

    # if there's an existing angle, it's only a valid solution if the guards distance is closer than you
    for p in the_guard_points:
        angle = shot_angle(your_position, p)
        d = distance_between(your_position, p)
        if (d > distance): continue
        if ((angle in angles and d < angles[angle]) or angle not in angles):
            angles[angle] = d
            solution.add(angle)

    return(len(solution))

# takes an x value and mirrors it horizontally
def mirror_on_side_wall(room_width, x, distance):
    steps = [2 * (room_width - x), 2 * x]
    number_of_mirrors = -(distance // -room_width)
    points = [x]
    for i in range(0, number_of_mirrors):
        points.append(points[-1] + steps[i % 2])

    return points

# takes a y value and mirrors it vertically
def mirror_on_top_wall(room_height, y, distance):
    steps = [2 * (room_height - y), 2 * y]
    number_of_mirrors = -(distance // -room_height)
    points = [y]
    for i in range(0, number_of_mirrors):
        points.append(points[-1] + steps[i % 2])

    return points

def reflect_on_x_axis(points):
    return [[x, -y] for (x, y) in points]

def reflect_on_y_axis(points):
    return [[-x, y] for (x, y) in points]

def distance_between(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def shot_angle(p1, p2):
    return math.atan2((p1[1] - p2[1]), (p1[0] - p2[0]))


print(solution([3,2], [1,1], [2,1], 4))
print(solution([300,275], [150,150], [185,100], 500))


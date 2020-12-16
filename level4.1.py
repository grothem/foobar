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
    your_x = your_position[0]
    your_y = your_position[1]

    guard_x = guard_position[0]
    guard_y = guard_position[1]

    room_max_x = dimensions[0]
    room_max_y = dimensions[1]

    solution_count = 1

    if (not your_x == guard_x):
        solution_count += reflect_on_horizontal_walls(your_x, your_y, guard_x, guard_y, room_max_y, distance)
    if (not your_y == guard_y):
        solution_count += reflect_on_vertical_walls(your_x, your_y, guard_x, guard_y, room_max_x, distance)

    # now get the "third" location projection
    a = reflect_on_room_wall(guard_x, room_max_x) - your_x
    b = reflect_on_room_wall(guard_y, room_max_y) - your_y
    c = hypotenous(a, b)
    if (c <= distance):
        solution_count += 1

    b = reflect_on_x_axis(guard_y)
    c = hypotenous(a, b)
    if (c <= distance):
        solution_count += 1

    # next side
    px = reflect_on_y_axis(guard_x)
    if (guard_x < your_x):
        a = px + your_x
    else:
        a = px + guard_x
    b = reflect_on_room_wall(guard_y, room_max_y) - your_y
    c = hypotenous(a, b)
    if (c <= distance):
        solution_count += 1

    b = reflect_on_x_axis(guard_y)
    c = hypotenous(a, b)
    if (c <= distance):
        solution_count += 1

    return solution_count

def reflect_on_horizontal_walls(your_x, your_y, guard_x, guard_y, room_height, d):
    b = abs(your_x - guard_x) # always gonna be the same for this chunk
    solution_count = 0
    # reflect point on horizontal walls until the hypotenus is greater than the max distance laser can travel
    pi = guard_y
    pj = guard_y

    while(True):
        p1y = reflect_on_x_axis(pi)
        a1 = bottom_leg(your_x, guard_x, p1y)
        # gives us the total distance the beam would travel
        c1 = hypotenous(a1, b)
        if (c1 < d):
            solution_count += 1

        p2y = reflect_on_room_wall(pj, room_height)
        a2 = bottom_leg(your_x, guard_x, p2y)
        c2 = hypotenous(a1, b)
        if (c2 < d):
            solution_count += 1
        else:
            break

        pi = p2y
        pj = p1y

    return solution_count

def reflect_on_vertical_walls(your_x, your_y, guard_x, guard_y, room_width, d):
    b = abs(your_y - guard_y) # always gonna be the same for this chunk
    solution_count = 0
    # reflect point on vertical walls until the hypotenus is greater than the max distance laser can travel
    pi = guard_x
    pj = guard_x

    while(True):
        p1x = reflect_on_y_axis(pi)
        a1 = bottom_leg(your_x, guard_x, p1x)
        # gives us the total distance the beam would travel
        c1 = hypotenous(a1, b)
        if (c1 < d):
            solution_count += 1

        p2x = reflect_on_room_wall(pj, room_width)
        a2 = bottom_leg(your_x, guard_x, p2x)
        c2 = hypotenous(a1, b)
        if (c2 < d):
            solution_count += 1
        else:
            break

        pi = p2x
        pj = p1x

    return solution_count

def bottom_leg(your_x, guard_x, point_x):
    leg = 0
    if (point_x > 0):
        if (guard_x > your_x):
            leg = point_x - guard_x + (guard_x - your_x)
        else:
            leg = point_x - your_x
    else:
        if (guard_x < your_x):
            leg = abs(point_x) + guard_x + (your_x - guard_x)
        else:
            leg = abs(point_x) + your_x

    return leg

def reflect_on_y_axis(x):
    return -x

def reflect_on_x_axis(y):
    return -y

def reflect_on_room_wall(value, l):
    if (value < 0):
        distance_from_wall = abs(value) + l
    else:
        distance_from_wall = l - value

    return distance_from_wall + l


def hypotenous(a, b):
    return math.sqrt(a**2 + b**2)

print(solution([3,2], [1,1], [2,1], 4))
print(solution([300,275], [150,150], [185,100], 500))

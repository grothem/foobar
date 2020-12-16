"""
oops - forgot the copy the problem, but something like this:

Jail cells are ordered in a triangle, you have to find the ID of a prisoner
for the given x, y coordinates. For example:
    |7
    |4 8
    |2 5 9
    |1 3 6 10

Given the (2, 3), the ID would 8
"""

def solution(x, y):
    # Get the number at the corresponding x value
    # i.e. the number of values in the triangle
    xn = x * (x + 1) // 2

    # Now the ID we're looking for will be at the y value:
    # (xn + x + (x + 1) + (x + 2) + (x + 3) + ... + (x + y - 1))
    for i in range(0, y - 1):
        xn += x + i

    return str(xn)

print(solution(5,10))
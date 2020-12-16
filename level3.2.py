def solution(x, y):
    x = int(x)
    y = int(y)

    # Treat the cycles as a tree
    # Assume that the provided x and y are valid nodes in the tree
    # Work our way up until we can verify if they are valid or not
    cycles = 0
    while (not atRoot(x, y)):
        if (x == 1):
            cycles += y - 1
            break

        if (y == 1):
            cycles += x - 1
            break

        if (x < y):
            if (x == 0):
                return "impossible"
            cycles += y // x
            y %= x
        else:
            if (y == 0):
                return "impossible"
            cycles += x // y
            x %= y

    return str(cycles)

def atRoot(x, y):
    return x == 1 and y == 1

print(solution("4","7"))

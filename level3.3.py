"""
Doomsday Fuel
=============

Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw ore, then during processing, begins randomly changing between
forms, eventually reaching a stable form. There may be multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel.

Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample. You have carefully studied the different structures
that the ore can take and which transitions it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it
has the same probabilities of entering the next state (which might be the same state).  You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more
exotic forms that the ore can become, but you haven't seen all of them.

Write a function solution(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next state and return an array of ints for each terminal
state giving the exact probabilities of each terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is
at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a
stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly.

For example, consider the matrix m:
[
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of
[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
[0, 3, 2, 9, 14].
"""

import fractions
from fractions import Fraction

def solution(m):
    """
    Solve using Absorbing Markov Chain
    We need to find the fundamental matrix, F = (In - B)^-1
    using the canonical form of the input, which is given by:

                                Terminal    Transient
        Termanal States   |       In          O     |
        Transient States  |       A           B     |

    We can then solve for the terminal state probabilites with F*A
    """

    if (len(m) == 1):
        return [1, 1]

    m = normalizeMatrix(m)
    B = getBMatrix(m)
    A = getAMatrix(m)

    transientStates = getTransientStates(m)
    I = identityMatrix(len(transientStates))
    F = invertMatrix(matrixSubtract(I, B))

    # We always start in state 0, so grab the first one
    probabilites = matrixMultiply(F, A)[0]

    denominators = [fr.denominator for fr in probabilites if fr.numerator > 0]
    lcm = lcmFor(denominators)

    answer = []
    for p in probabilites:
        if (p == 0 or p.denominator == lcm):
            answer.append(p.numerator)
        else:
            answer.append(p.numerator * (lcm / p.denominator))

    answer.append(lcm)
    return answer

def identityMatrix(n):
    return [[1 if i==j else 0 for j in range(n)] for i in range(n)]

def getTerminalStates(m):
    terminalStates = []
    for i, state in enumerate(m):
        if (all(s == 0 for s in state)):
            terminalStates.append(i)

    return terminalStates

def getTransientStates(m):
    transientStates = []
    for i, state in enumerate(m):
        if (not all(s == 0 for s in state)):
            transientStates.append(i)

    return transientStates

def getBMatrix(m):
    transientStates = getTransientStates(m)
    B = [[0 for i in range(len(transientStates))] for j in range(len(transientStates))]
    for i, ith in enumerate(transientStates):
        for j, jth in enumerate(transientStates):
            B[i][j] = m[ith][jth]

    return B

def getAMatrix(m):
    transientStates = getTransientStates(m)
    terminalStates = getTerminalStates(m)
    A = [[0 for i in range(len(terminalStates))] for j in range(len(transientStates))]
    for i, ith in enumerate(transientStates):
        for j, jth in enumerate(terminalStates):
            A[i][j] = m[ith][jth]

    return A

def normalizeMatrix(m):
    transientStates = []
    for i, state in enumerate(m):
        if (not all(s == 0 for s in state)):
            denominator = sum(state)
            for j, value in enumerate(state):
                if (value > 0):
                    state[j] = Fraction(value, denominator)

    return m

def matrixSubtract(a, b):
    # assuming A and B have the same dimensions
    c = [[ 0 for j in range(len(a))] for i in range(len(b))]
    for i in range(len(a)):
        for j in range(len(b)):
            c[i][j] = a[i][j] - b[i][j]

    return c

def matrixMultiply(a, b):
    # assuming A and B can be multiplied
    rows_a = len(a)
    cols_a = len(a[0])
    rows_b = len(b)
    cols_b = len(b[0])

    c = [[0 for row in range(cols_b)] for col in range(rows_a)]

    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                c[i][j] += a[i][k] * b[k][j]
    return c

def lcm(a, b):
    return abs(a * b) // fractions.gcd(a, b)

def lcmFor(n):
    return reduce(lambda x, y: lcm(x, y), n)

def invertMatrix(A):
    """
    Taken from: https://integratedmlai.com/matrixinverse/
    Returns the inverse of the passed in matrix.
        :param A: The matrix to be inversed

        :return: The inverse of the matrix A
    """
    # Section 1: Make sure A can be inverted.
    # check_squareness(A)
    # check_non_singular(A)

    # Section 2: Make copies of A & I, AM & IM, to use for row ops
    n = len(A)
    AM = copy_matrix(A)
    I = identityMatrix(n)
    IM = copy_matrix(I)

    # Section 3: Perform row operations
    indices = list(range(n)) # to allow flexible row referencing ***
    for fd in range(n): # fd stands for focus diagonal
        fdScaler = Fraction(1, AM[fd][fd])
        # FIRST: scale fd row with fd inverse.
        for j in range(n): # Use j to indicate column looping.
            AM[fd][j] *= fdScaler
            IM[fd][j] *= fdScaler
        # SECOND: operate on all rows except fd row as follows:
        for i in indices[0:fd] + indices[fd+1:]:
            # *** skip row with fd in it.
            crScaler = AM[i][fd] # cr stands for "current row".
            for j in range(n):
                # cr - crScaler * fdRow, but one element at a time.
                AM[i][j] = AM[i][j] - crScaler * AM[fd][j]
                IM[i][j] = IM[i][j] - crScaler * IM[fd][j]

    return IM

def zeros_matrix(rows, cols):
    A = []
    for i in range(rows):
        A.append([])
        for j in range(cols):
            A[-1].append(0.0)

    return A

def copy_matrix(M):
    rows = len(M)
    cols = len(M[0])

    MC = zeros_matrix(rows, cols)

    for i in range(rows):
        for j in range(rows):
            MC[i][j] = M[i][j]

    return MC

foo = [[0,1],[1,1],[1,2]]
print(len(foo))
print(len(foo[0]))
# print(solution([[1,0,0,3,0],[0,2,0,0,5],[0,0,0,1,0],[0,0,0,0,0],[0,0,0,0,0]]))
print(solution([[1,3,0,2,0],[0,0,0,0,0],[0,2,1,3,0],[0,0,0,0,0],[1,0,0,1,2]]))
print(solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]))
print(solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]]))
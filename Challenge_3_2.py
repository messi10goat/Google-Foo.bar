'''

Doomsday Fuel
=============

Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw ore, then during processing, begins randomly changing between forms, eventually reaching a stable form. There may be multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel. 

Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample. You have carefully studied the different structures that the ore can take and which transitions it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state).  You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that the ore can become, but you haven't seen all of them.

Write a function solution(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly. 

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

Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Java cases --
Input:
Solution.solution({{0, 2, 1, 0, 0}, {0, 0, 0, 3, 4}, {0, 0, 0, 0, 0}, {0, 0, 0, 0,0}, {0, 0, 0, 0, 0}})
Output:
    [7, 6, 8, 21]

Input:
Solution.solution({{0, 1, 0, 0, 0, 1}, {4, 0, 0, 3, 2, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}})
Output:
    [0, 3, 2, 9, 14]

-- Python cases --
Input:
solution.solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])
Output:
    [7, 6, 8, 21]

Input:
solution.solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
Output:
    [0, 3, 2, 9, 14]
    
'''

# Solution:

from fractions import gcd
import unittest
from fractions import Fraction


def multiply_matrices(a, b):
    # confirm dimensions
    a_rows = len(a)
    a_cols = len(a[0])
    b_cols = len(b[0])
    rows = a_rows
    cols = b_cols
    # create the result matrix c = a*b
    c = make_2d_list(rows, cols)
    # now find each value in turn in the result matrix
    for row in xrange(rows):
        for col in xrange(cols):
            dot_product = Fraction(0, 1)
            for i in xrange(a_cols):
                dot_product += a[row][i]*b[i][col]
            c[row][col] = dot_product
    return c


def multiply_row_of_square_matrix(m, row, k):
    n = len(m)
    row_operator = make_identity(n)
    row_operator[row][row] = k
    return multiply_matrices(row_operator, m)


def make_2d_list(rows, cols):
    a = []
    for row in xrange(rows):
        a += [[0] * cols]
    return a


def make_identity(n):
    result = make_2d_list(n, n)
    for i in xrange(n):
        result[i][i] = Fraction(1, 1)
    return result


def add_multiple_of_row_of_square_matrix(m, source_row, k, target_row):
    # add k * source_row to target_row of matrix m
    n = len(m)
    row_operator = make_identity(n)
    row_operator[target_row][source_row] = k
    return multiply_matrices(row_operator, m)


def invert_matrix(m):
    n = len(m)
    assert(len(m) == len(m[0]))
    inverse = make_identity(n)
    for col in xrange(n):
        diagonal_row = col
        assert(m[diagonal_row][col] != 0)
        k = Fraction(1, m[diagonal_row][col])
        m = multiply_row_of_square_matrix(m, diagonal_row, k)
        inverse = multiply_row_of_square_matrix(inverse, diagonal_row, k)
        source_row = diagonal_row
        for target_row in xrange(n):
            if source_row != target_row:
                k = -m[target_row][col]
                m = add_multiple_of_row_of_square_matrix(m, source_row, k, target_row)
                inverse = add_multiple_of_row_of_square_matrix(inverse, source_row, k, target_row)
    # that's it!
    return inverse


def subtract_identity(q, denominator):
    size = range(len(q))
    for i in size:
        for j in size:
            if i == j:
                q[i][j] = denominator - q[i][j]
            else:
                q[i][j] = - q[i][j]


def transform_matrix(m):
    for row_index, row in enumerate(m):
        row_sum = sum(m[row_index])
        if row_sum == 0:
            m[row_index][row_index] = 1
        else:
            for col_index, col in enumerate(row):
                m[row_index][col_index] = Fraction(col, row_sum)


def get_submatrix(m, rows, cols):
    new_matrix = []

    for row in rows:
        current_row = []
        for col in cols:
            current_row.append(m[row][col])
        new_matrix.append(current_row)
    return new_matrix


def get_q(m, non_terminal_states):
    return get_submatrix(m, non_terminal_states, non_terminal_states)


def get_r(m, non_terminal_states, terminal_states):
    return get_submatrix(m, non_terminal_states, terminal_states)


def subtract_matrices(a, b):
    new_matrix = []
    for row_index, row in enumerate(a):
        column = []
        for col_index, col in enumerate(row):
            column.append(a[row_index][col_index] - b[row_index][col_index])
        new_matrix.append(column)

    return new_matrix


def lcm(a, b):
    result = a * b / gcd(a, b)

    return result


def lcm_for_arrays(args):
    array_length = len(args)
    if array_length <= 2:
        return lcm(*args)

    initial = lcm(args[0], args[1])
    i = 2
    while i < array_length:
        initial = lcm(initial, args[i])
        i += 1
    return initial


def solution(m):
    terminal_states = []
    non_terminal_states = []
    for index, row in enumerate(m):
        if sum(row) == 0:
            terminal_states.append(index)
        else:
            non_terminal_states.append(index)
    if len(terminal_states) == -1:
        return [-1,1]
    if len(terminal_states) == 1:
        return [1, 1]

    transform_matrix(m)

    q = get_q(m, non_terminal_states)
    r = get_r(m, non_terminal_states, terminal_states)

    result = multiply_matrices(invert_matrix(subtract_matrices(make_identity(len(q)), q)), r)

    denominator = lcm_for_arrays([item.denominator for item in result[0]])

    result = [item.numerator * denominator / item.denominator for item in result[0]]

    result.append(denominator)

    return result

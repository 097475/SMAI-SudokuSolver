#
# Informed Search Methods
#
# Implementation of various backtracking-based solvers
#

from enum import Enum
import random


class SolverType(Enum):
    GTBT = 1  # Generate-and-test Backtracking
    BT = 2  # Cronological Backtracking
    BJ = 3  # Backjumping
    CBJ = 4  # Conflict-Directed Backjumping


def make_arc_consistent(cn):
    """
    Makes the cn constraint network arc-consistent (use the AC-3 algorithm).
    (there are no unary-constraints so you can omit making it first node-consistent).
    """

    # ********** YOU IMPLEMENT THIS **********

    q = cn.get_constraints()[:]
    for el in cn.get_constraints():
        q.append((el[1], el[0]))

    while len(q) > 0:
        arc = q[0]
        i = arc[0]
        j = arc[1]
        q.remove(arc)
        if revise(cn, i, j):
            for h in range(cn.num_variables()):
                if h != i and h != j:
                    q.append((h, i))

    return


def revise(cn, i, j):
    delete = False
    domain = set(cn.get_domain(i))

    for d_i in cn.get_domain(i):
        satisfied = False
        for d_j in cn.get_domain(j):
            if cn.consistent_values(i, j, d_i, d_j):
                satisfied = True
                break

        if not satisfied:
            domain.remove(d_i)
            delete = True

    cn.set_domain(i, domain)

    return delete


def solve(st, cn):
    """
    Use the specified backtracking algorithm (st) to solve the CSP problem (cn).
    Returns a tuple (assignment, nodes), where the former is the solution (an empty list if not found)
    and the latter the number of nodes generated.
    """

    def consistent_upto_level(cn, i, A):
        for j in range(0, i):
            if not cn.consistent(i, j, A):
                return j
        return i

    def GTB(cn, i, A):
        # print(A)
        nonlocal num_nodes
        num_nodes += 1
        if i >= cn.num_variables():
            return cn.consistent_all(A)
        for v in cn.get_sorted_domain(i):
            A.append(v)
            solved = GTB(cn, i + 1, A)
            if solved:
                return True
            A.pop()
        return False

    def BT(cn, i, A):
        # ********** YOU IMPLEMENT THIS **********
        nonlocal num_nodes
        num_nodes += 1
        for value in cn.get_sorted_domain(i):
            A.append(value)
            consistent = cn.consistent_other(i, A)
            if consistent:
                if i == cn.num_variables() - 1:
                    return True
                else:
                    consistent = BT(cn, i + 1, A)
            if not consistent:
                A.pop()
            else:
                return consistent
        return False

    def BJ(cn, i, A):
        # ********** YOU IMPLEMENT THIS **********
        nonlocal num_nodes
        num_nodes += 1

        max_check_lvl = 0
        return_depth = 0

        for value in cn.get_sorted_domain(i):
            if len(A) <= i:
                A.append(value)
            else:
                A[i] = value

            consistent = True
            for j in range(len(A)):
                if j < i and not cn.consistent(i, j, A):
                    max_check_lvl = j
                    consistent = False
                    break

            if consistent:
                if i == cn.num_variables() - 1:
                    return True, return_depth
                else:
                    consistent, max_check_lvl = BJ(cn, i + 1, A)
                    if max_check_lvl < i:
                        return consistent, max_check_lvl
                    if consistent:
                        return_depth = i - 1
                        break

            return_depth = max(return_depth, max_check_lvl)

        return consistent, return_depth

    def CBJ(cn, i, A, CS):

        # ********** YOU IMPLEMENT THIS **********
        nonlocal num_nodes
        num_nodes += 1
        CS[i].clear()
        for value in sorted(cn.get_sorted_domain(i)):
            if len(A) <= i:
                A.append(value)
            else:
                A[i] = value

            consistent = True
            for j in range(len(A)):
                if j < i and not cn.consistent(i, j, A):
                    CS[i].add(j)
                    consistent = False
                    break

            if consistent:
                if i == cn.num_variables() - 1:
                    CS[i].add(i - 1)
                    break
                else:
                    consistent, return_depth = CBJ(cn, i + 1, A, CS)
                    if return_depth < i:
                        return consistent, return_depth
                    if consistent:
                        CS[i].add(i - 1)
                        break

        return_depth = max(CS[i])
        CS[i].remove(return_depth)
        CS[return_depth].update(CS[i])
        return consistent, return_depth

    num_nodes = 0
    assignment = []
    ConflictSet = [set() for _ in range(0, cn.num_variables())]  # NOTE: remove.

    print('Solving ...', st)
    if st == SolverType.GTBT:
        solved = GTB(cn, 0, assignment)
    elif st == SolverType.BT:
        solved = BT(cn, 0, assignment)
    elif st == SolverType.BJ:
        (solved, _) = BJ(cn, 0, assignment)
    elif st == SolverType.CBJ:
        (solved, _) = CBJ(cn, 0, assignment, ConflictSet)

    return (assignment, num_nodes)

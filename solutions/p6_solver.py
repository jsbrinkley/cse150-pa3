# -*- coding: utf-8 -*-
from p1_is_complete import is_complete
from p2_is_consistent import is_consistent
from p5_ordering import select_unassigned_variable
from p5_ordering import order_domain_values


from collections import deque


def inference(csp, variable):
    """Performs an inference procedure for the variable assignment.

    For P6, *you do not need to modify this method.*
    """
    return ac3(csp, csp.constraints[variable].arcs())


def backtracking_search(csp):
    """Entry method for the CSP solver.  This method calls the backtrack method to solve the given CSP.

    If there is a solution, this method returns the successful assignment (a dictionary of variable to value);
    otherwise, it returns None.

    For P6, *you do not need to modify this method.*
    """
    if backtrack(csp):
        return csp.assignment
    else:
        return None


def backtrack(csp):
    """Performs the backtracking search for the given csp.

    If there is a solution, this method returns True; otherwise, it returns False.
    """

    # Do whatever
    if is_complete(csp):
        return True

    # get the next unassigned variable
    var = select_unassigned_variable(csp)

    result = False
    orderedDomain = order_domain_values(csp, var)
    # for each value in var
    for value in orderedDomain:
        if is_consistent(csp, var, value):

            csp.variables.begin_transaction()

            var.assign(value)

            if inference(csp, var):

                result = backtrack(csp)
                if result:
                    return result

            csp.variables.rollback()

    return None


def ac3(csp, arcs=None):
    """Executes the AC3 or the MAC (p.218 of the textbook) algorithms.

    If the parameter 'arcs' is None, then this method executes AC3 - that is, it will check the arc consistency
    for all arcs in the CSP.  Otherwise, this method starts with only the arcs present in the 'arcs' parameter
    in the queue.

    Note that the current domain of each variable can be retrieved by 'variable.domains'.

    This method returns True if the arc consistency check succeeds, and False otherwise."""

    queue_arcs = deque(arcs if arcs is not None else csp.constraints.arcs())

    size = len(queue_arcs)

    while size > 0:
        xi, xj = queue_arcs.popleft()

        if revise(csp, xi, xj):
            
            if len(xi.domain) == 0:
                return False

            for constraint in csp.constraints[xi]:
                x_neighbor = constraint.var2

                queue_arcs.append((x_neighbor, xi))

        size = len(queue_arcs)

    return True


def revise(csp, xi, xj):
    # You may additionally want to implement the 'revise' method.
    revised = False

    constraints = csp.constraints[xi, xj]

    for constraint in constraints:
        for x in xi.domain:

            satisfied = False

            for y in xj.domain:
                if constraint.is_satisfied(x, y):
                    satisfied = True

            if not satisfied:
                xi.domain.remove(x)
                revised = True

    return revised

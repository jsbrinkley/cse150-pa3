# -*- coding: utf-8 -*-

from collections import deque

def ac3(csp, arcs=None):
    """Executes the AC3 or the MAC (p.218 of the textbook) algorithms.

    If the parameter 'arcs' is None, then this method executes AC3 - that is, it will check the arc consistency
    for all arcs in the CSP.  Otherwise, this method starts with only the arcs present in the 'arcs' parameter
    in the queue.

    Note that the current domain of each variable can be retrieved by 'variable.domains'.

    This method returns True if the arc consistency check succeeds, and False otherwise."""

    queue_arcs = deque(arcs if arcs is not None else csp.constraints.arcs())

    while queue_arcs:
        xi, xj = queue_arcs.popleft()

        if revise(csp, xi, xj):
            if len(xi.domain) == 0:
                return False

            for constraint in csp.constraints[xi]:
                x_neighbor = constraint.var2

                queue_arcs.append((x_neighbor, xi))

    return True

def revise(csp, xi, xj):
    # You may additionally want to implement the 'revise' method.
    revised = False

    constraints = csp.constraints[xi]

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

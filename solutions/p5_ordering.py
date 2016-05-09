# -*- coding: utf-8 -*-
import sys
import operator

def select_unassigned_variable(csp):
    """Selects the next unassigned variable, or None if there is no more unassigned variables
    (i.e. the assignment is complete).

    This method implements the minimum-remaining-values (MRV) and degree heuristic. That is,
    the variable with the smallest number of values left in its available domain.  If MRV ties,
    then it picks the variable that is involved in the largest number of constraints on other
    unassigned variables.
    """

    unassigned_vars = []

    for var in csp.variables:
        if not var.is_assigned():
            unassigned_vars.append(var)

    min_domain = sys.maxint
    mrv_list = []

    for var in unassigned_vars:
        if len(var.domain) < min_domain:
            min_domain = len(var.domain)
            mrv_list = [var]
        elif len(var.domain) == min_domain:
            mrv_list.append(var)

    min_const = sys.maxint
    min_var = None
    for var in mrv_list:
        if len(csp.constraints[var]) < min_const:
            min_var = var

    return min_var

def order_domain_values(csp, variable):
    """Returns a list of (ordered) domain values for the given variable.

    This method implements the least-constraining-value (LCV) heuristic; that is, the value
    that rules out the fewest choices for the neighboring variables in the constraint graph
    are placed before others.
    """
    constraints = csp.constraints[variable]

    var_twos = []

    for constraint in constraints:
        var_twos.append(constraint.var2)

    domain_count = [0] * len(variable.domain)

    domain_map = {}

    for value in variable.domain:
        count = 0

        for var2 in var_twos:
            if value in var2.domain:
                count += 1

        domain_map[value] = count

    sorted_map = sorted(domain_map.items(), key=operator.itemgetter(1))

    sorted_domain = []

    for k, v in sorted_map:
        sorted_domain.append(k)

    return sorted_domain
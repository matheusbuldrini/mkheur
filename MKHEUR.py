from MKPsolver import MKPSolver
import numpy as np


class MKHEUR(MKPSolver):
    def __init__(self, instance):
        super().__init__(instance)
        self.solver_name = "MKHEUR"

    def solve(self):
        self.found_solution = 42
        self.print()
        return self.found_solution

    def _solve_single_constraint_continous_kp(Ai, c, bi):
        Z = 10
        x = [i for i in range(len(Ai))]
        raise NotImplementedError
        return (Z, x)

    def _surrogate_calc():
        # calc Max c't ....
        return NotImplementedError

    def _find_maximum():
        # use bisection
        return NotImplementedError

    def _procedure_1(self):

        vec_mi = [None for i in range(self.m)]

        """1 - Let m denote number of constraints. Then, for i = 1,2, . . . ,m, use constraint vector
        ai, objective function vector c, and right-hand side element bi, to define and solve m
        single-constraint continuous knapsack problems. Determine constraint i*, which corresponds
        to the single constraint knapsack problem with the lowest objective function
        value Zbar and the solution vector xbar. Let constraint i* be the current surrogate constraint."""

        solutions = []
        for i in range(self.m):
            solutions.append(
                self._solve_single_constraint_continous_kp(self.A[i], self.c, self.b[i])
            )

        Zbar = solutions[0]
        i_star = 0
        for i, solution in enumerate(solutions):
            if solution[0] < Zbar:
                Zbar = solution[0]
                i_star = i
        xbar = solutions[i_star][1]

        current_surrogate_constraint = i_star

        """2 - Determine the amount by which xbar violates each constraint of Problem IP. If none are
        violated, stop with the current surrogate constraint and corresponding upper-bound
        value Zbar (optimal surrogate multipliers are found for linear programming relaxation
        of Problem IP). If one or more constraints are violated, identify constraint i' that is
        the most violated one."""

        # pra cada restricao de IP (são m no total), ver quanto xbar viola

        violation_amounts = []  # violation if this number > 0
        for i in range(self.m):
            violation_amounts.append(self.A[i] * xbar - self.b[i])

        if violation_amounts <= 0:
            # stop with the current surrogate constraint and corresponding upper-bound value Zbar
            # TO DO
            raise NotImplementedError
            pass
        else:
            # If one or more constraints are violated, identify constraint i' (iprime) that is the most violated one.
            iprime = 0
            for i in range(self.m):
                if violation_amounts[i] > violation_amounts[iprime]:
                    iprime = i

        """3 - Let the current surrogate constraint be constraint 1 and constraint i' be constraint 2.
        Determine a multiplier pair (1,mibar) using bisection over S(1,mi). If the objective function
        value does not decline or a maximum number of iterations is reached, stop with current surrogate 
        constraint and corresponding upper bound Zbar, otherwise update Zbar to be the best upper bound 
        and xbar as the corresponding solution vector"""

        constraint_1 = current_surrogate_constraint
        constraint_2 = iprime

        def S(mi):
            self._surrogate_calc(constraint_1, mi * constraint_2)

        mibar, Zbar, xbar = self._find_maximum(S)

        self.A[current_surrogate_constraint] = np.dot(vec_mi, self.A) + np.dot(
            mibar, self.A[iprime]
        )

        return vec_mi

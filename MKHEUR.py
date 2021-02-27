from MKPsolver import MKPSolver
import scipy.optimize as op
import numpy as np


class MKHEUR(MKPSolver):
    def __init__(self, instance):
        super().__init__(instance)
        self.solver_name = "MKHEUR"

    def solve(self):
        self._procedure_1()
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

        m = self.instance.m
        n = self.instance.n
        A = self.instance.A
        b = self.instance.b
        c = self.instance.c

        vec_mi = [1 for i in range(m)]

        """1 - Let m denote number of constraints. Then, for i = 1,2, . . . ,m, use constraint vector
        ai, objective function vector c, and right-hand side element bi, to define and solve m
        single-constraint continuous knapsack problems. Determine constraint i*, which corresponds
        to the single constraint knapsack problem with the lowest objective function
        value Zbar and the solution vector xbar. Let constraint i* be the current surrogate constraint."""

        solutions = []

        for i in range(m):
            # solutions.append(self._solve_single_constraint_continous_kp(A[i], c, b[i]))
            res = op.linprog(
                np.negative(c), [A[i]], b[i], bounds=[(0, 1) for _ in range(len(c))]
            )
            solutions.append((-res.fun, res.x))  # (Zbar, x)

        Zbar = solutions[0][0]
        i_star = 0
        for i, solution in enumerate(solutions):
            if solution[0] < Zbar:
                Zbar = solution[0]
                i_star = i
        xbar = solutions[i_star][1]

        current_surrogate_constraint = i_star

        for nao_sei in range(10):
            """2 - Determine the amount by which xbar violates each constraint of Problem IP. If none are
            violated, stop with the current surrogate constraint and corresponding upper-bound
            value Zbar (optimal surrogate multipliers are found for linear programming relaxation
            of Problem IP). If one or more constraints are violated, identify constraint i' that is
            the most violated one."""

            # pra cada restricao de IP (são m no total), ver quanto xbar viola

            violation_amounts = []  # violation if this number > 0
            for i in range(m):
                violation_amounts.append(np.dot(A[i], xbar) - b[i])

            if violation_amounts <= [0 for _ in range(len(violation_amounts))]:
                # stop with the current surrogate constraint and corresponding upper-bound value Zbar
                # TO DO
                print("cabou")
                break
                raise NotImplementedError
                pass
            else:
                # If one or more constraints are violated, identify constraint i' (iprime) that is the most violated one.
                iprime = 0
                for i in range(m):
                    if violation_amounts[i] > violation_amounts[iprime]:
                        iprime = i
            # print("--------------------------------------------------------------")
            # print(iprime)
            """3 - Let the current surrogate constraint be constraint 1 and constraint i' be constraint 2.
            Determine a multiplier pair (1,mibar) using bisection over S(1,mi). If the objective function
            value does not decline or a maximum number of iterations is reached, stop with current surrogate 
            constraint and corresponding upper bound Zbar, otherwise update Zbar to be the best upper bound 
            and xbar as the corresponding solution vector"""

            constraint_1_idx = current_surrogate_constraint
            constraint_2_idx = iprime

            def Z_S(mi):

                constraint_1 = np.array(A[constraint_1_idx])
                constraint_2 = np.array(A[constraint_2_idx]) * mi

                # https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
                res = op.linprog(
                    np.negative(c),
                    A_ub=[constraint_1, constraint_2],
                    b_ub=[b[constraint_1_idx], b[constraint_2_idx] * mi],
                    bounds=[(0, 1) for _ in range(len(c))],
                )

                return (-res.fun, res.x)

                # self._surrogate_calc(constraint_1, mi * constraint_2)

            """X = []
            Y = []
            for o in range(1, 100):
                X.append(o)
                Y.append(Z_S(o)[0])
            import matplotlib.pyplot as plt

            fig, axs = plt.subplots()
            axs.plot(X, Y, label="S")
            axs.legend()
            plt.show()"""

            def _find_minimum(f):
                min = float("inf")
                for o in range(1, 100):
                    res = Z_S(o)
                    if res[0] < min:
                        min_mi = o
                        min = res[0]
                        min_x = res[1]
                return min_mi, min, min_x

            mibar, Zbar, xbar = _find_minimum(Z_S)

            # print(A[current_surrogate_constraint])
            A[current_surrogate_constraint] = np.dot(vec_mi, A) + np.dot(
                mibar, A[iprime]
            )

            vec_mi[current_surrogate_constraint] = mibar
            # print(A[current_surrogate_constraint])
            # print(vec_mi)
            # print(mibar, Zbar, xbar)
        print(vec_mi)

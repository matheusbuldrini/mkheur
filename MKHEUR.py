from MKPsolver import MKPSolver
import scipy.optimize as op
import numpy as np
import time


class MKHEUR(MKPSolver):
    def __init__(self, instance):
        super().__init__(instance)
        self.solver_name = "MKHEUR"

    def solve(self):
        start_time = time.time()
        self.found_solution = self.procedure_MKHEUR()
        self.time = time.time() - start_time
        return self.found_solution, self.time

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

    def _procedure_1(self, K=100):

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

        for nao_sei in range(1):  # TO DO
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
                # If none are violated, stop with the current surrogate
                # constraint and corresponding upper-bound value Zbar
                # TO DO
                print("cabou")
                break
                raise NotImplementedError
                pass
            else:
                # If one or more constraints are violated, identify
                # constraint i' (iprime) that is the most violated one.
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

            def _find_minimum(f):  # TO DO: use bisection
                min = float("inf")
                for o in range(1, K):
                    res = Z_S(o)
                    if res[0] < min:
                        min_mi = o
                        min = res[0]
                        min_x = res[1]
                return min_mi, min, min_x

            mibar, Zbar, xbar = _find_minimum(Z_S)

            # print(A[current_surrogate_constraint])
            # A[current_surrogate_constraint] = np.dot(vec_mi, A) + np.dot(
            #    mibar, A[iprime]
            # )

            vec_mi[current_surrogate_constraint] = mibar
            # print(A[current_surrogate_constraint])
            # print(vec_mi)
            # print(mibar, Zbar, xbar)
        # print(vec_mi)
        return vec_mi

    def procedure_MKHEUR(self):
        m = self.instance.m
        n = self.instance.n
        A = self.instance.A
        b = self.instance.b
        c = self.instance.c

        # (1) Determine a set of surrogate multipliers using Procedure 1
        mi = [1 for _ in range(len(b))]  # self._procedure_1()
        # mi2 = self._procedure_1()

        # (2) Calculate c_j/(mi A)_j, ratios.
        # Sort and renumber variables according to decreasing order of these ratios.
        ratios = []
        for j in range(len(c)):
            ratios.append((c[j] / (np.dot(mi, A)[j]), j))

        ratios.sort(reverse=True)

        # print(ratios)

        # (3) Fix variables equal to one according to the
        # order determined in Step 2. If fixing a variable
        # equal to one causes violation of one of the
        # constraints, fix that variable equal to zero and
        # continue. Denote the feasible solution determined
        # in this step as X

        def construct_solution(fixed_to_zero_var_idx=None):
            def check_solution(sol):
                # print(np.dot(A, sol))
                # print(b)
                return np.all(np.dot(A, sol) <= b)

            solution_xbar = [0 for i in range(len(c))]
            for ratio in ratios:
                if ratio[1] == fixed_to_zero_var_idx:
                    solution_xbar[ratio[1]] = 0
                else:
                    solution_xbar[ratio[1]] = 1

                if not check_solution(solution_xbar):
                    solution_xbar[ratio[1]] = 0

            # print(np.dot(c, solution_xbar))  # custo
            return solution_xbar

        solution_xbar = construct_solution()

        # (4) For each variable fixed equal to one in solution_xbar,
        # fix the variable equal to zero and repeat
        # Step 3 to define a new feasible solution.
        # print("------")
        best_xbar = solution_xbar
        best_obj_val = np.dot(c, solution_xbar)

        for j, x_j in enumerate(solution_xbar):
            if x_j == 1:
                new_sol = construct_solution(j)
                new_sol_obj_val = np.dot(c, new_sol)
                if new_sol_obj_val > best_obj_val:
                    best_xbar = new_sol
                    best_obj_val = new_sol_obj_val

        # print(best_xbar)
        return best_obj_val

from MKHEUR import MKHEUR
import numpy as np


class CustomMKH(MKHEUR):
    def __init__(self, instance):
        super().__init__(instance)
        self.solver_name = "CustomMKH"

    # def _procedure_1(self):
    #    super()._procedure_1(2)

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

        best_xbar = solution_xbar
        best_obj_val = np.dot(c, solution_xbar)

        initial_best_obj_val = best_obj_val

        P = 1

        for j, x_j in enumerate(solution_xbar):
            if x_j == 1:
                new_sol = construct_solution(j)
                new_sol_obj_val = np.dot(c, new_sol)
                if new_sol_obj_val > best_obj_val:
                    best_xbar = new_sol
                    best_obj_val = new_sol_obj_val
                # if a P% better solution is found, break
                if best_obj_val / initial_best_obj_val > 1 + P / 100:
                    break

        # print(best_xbar)
        return best_obj_val
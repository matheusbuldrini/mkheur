from MKPsolver import MKPSolver


class MKHEUR(MKPSolver):
    def __init__(self, instance):
        super().__init__(instance)
        self.solver_name = "MKHEUR"

    def solve(self):
        self.found_solution = 42
        self.print()
        return self.found_solution
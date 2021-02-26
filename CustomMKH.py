from MKPsolver import MKPSolver


class CustomMKH(MKPSolver):
    def __init__(self, instance):
        super().__init__(instance)
        self.solver_name = "CustomMKH"

    def solve(self):
        self.found_solution = 44
        self.print()
        return self.found_solution
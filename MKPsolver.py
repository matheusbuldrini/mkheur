from MKPInstance import MKPInstance


class MKPSolver:
    def __init__(self, instance: MKPInstance):
        self.instance: MKPInstance = instance
        self.found_solution = None
        self.solver_name = ""

    def solve(self):
        self.found_solution = None
        raise NotImplementedError

    def print(self):
        print("Solved by " + self.solver_name + ":")
        print(self.instance.n)
        print(self.instance.m)
        print(self.instance.optmal_value)
        print(self.instance.c)
        print(self.instance.A)
        print(self.instance.b)

        print(self.found_solution)
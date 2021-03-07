import numpy as np


class MKPInstance:
    def __init__(self, file_path):
        self._read_instance_from_file(file_path)

    def _read_instance_from_file(self, file_path):
        # The format of these data files is:
        # Variables (n), #Constraints (m), Optimal value (0 if unavailable)
        # Profit P(j) for each n
        # n x m matrix of constraints
        # Capacity b(i) for each m
        instance = []
        f = open(file_path, "r")
        for line in f:
            for i in line.split():
                instance.append(int(i))

        self.n = instance[0]
        self.m = instance[1]
        self.optmal_value = instance[2]
        self.c = np.array(instance[3 : 3 + self.n])
        self.A = np.array(instance[3 + self.n : 3 + self.n + self.n * self.m]).reshape(
            self.m, self.n
        )
        self.b = np.array(
            instance[
                3 + self.n + self.n * self.m : 3 + self.n + self.n * self.m + self.m
            ]
        )

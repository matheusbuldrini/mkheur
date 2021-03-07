from CustomMKH import CustomMKH
from MKPInstance import MKPInstance
from MKHEUR import MKHEUR
from CustomMKH import CustomMKH

instances = []


instance = MKPInstance("instances-chubeas/OR30x500/OR30x500-0.25_1.dat")

mkheur = MKHEUR(instance)
custom = CustomMKH(instance)

result = mkheur.solve()
print(result)
result2 = custom.solve()
print(result2)
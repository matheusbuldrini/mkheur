from CustomMKH import CustomMKH
from MKPInstance import MKPInstance
from MKHEUR import MKHEUR
from CustomMKH import CustomMKH

instance = MKPInstance("instances-chubeas/OR10x100/OR10x100-0.25_1.dat")

mkheur = MKHEUR(instance)
custom = CustomMKH(instance)

result = mkheur.solve()
result2 = custom.solve()
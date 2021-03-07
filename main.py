from CustomMKH import CustomMKH
from MKPInstance import MKPInstance
from MKHEUR import MKHEUR
from CustomMKH import CustomMKH
import os

instances = []

for root, dirs, files in os.walk("instances-chubeas", topdown=False):
    for name in files:
        instances.append(MKPInstance(os.path.join(root, name)))

for instance in instances:
    print("m=" + str(instance.m))
    print("n=" + str(instance.n))
    mkheur = MKHEUR(instance)
    custom = CustomMKH(instance)

    result = mkheur.solve()
    print("obj_fun=" + str(result[0]))
    print("time=" + str(result[1]))
    result2 = custom.solve()
    print("mod_obj_fun=" + str(result2[0]))
    print("mod_time=" + str(result2[1]))

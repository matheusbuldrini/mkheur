from CustomMKH import CustomMKH
from MKPInstance import MKPInstance
from MKHEUR import MKHEUR
from CustomMKH import CustomMKH
import os

instances = []

for root, dirs, files in os.walk("instances-chubeas", topdown=False):
    for name in files:
        instances.append(MKPInstance(os.path.join(root, name)))

print("FILE \t VALUE \t TIME \t MOD_VALUE \t MOD_TIME")
for instance in instances:
    mkheur = MKHEUR(instance)
    custom = CustomMKH(instance)
    result = mkheur.solve()
    result2 = custom.solve()

    print(
        os.path.split(instance.file_path)[-1][2:-4]
        + "\t"
        + str(result[0])
        + "\t "
        + str(result[1])
        + "\t "
        + str(result2[0])
        + "\t "
        + str(result2[1])
    )

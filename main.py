from MKPInstance import MKPInstance

i = MKPInstance("instances-chubeas/OR10x100/OR10x100-0.25_1.dat")

print(i.n)
print(i.m)
print(i.optmal_value)
print(i.p)
print(i.constraints_matrix)
print(i.b)
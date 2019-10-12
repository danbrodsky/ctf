from z3 import *

variables = [Real("int_%d" % i) for i in range (3)]
w = Real('w')

S = Solver()

S.add(w != 0)
S.add( ((1/2)*w) / (variables[0] + variables[1] + variables[2]) == 19400354808065.542)
S.add(variables[0] == 62791383142154)
S.add(w*w == ( 4*(variables[0]**2) * variables[1]**2 - ( (variables[1]**2 + variables[0]**2 - variables[2]**2 )**2  ) ))


S.add( (variables[0]*variables[1]*variables[2]) / w == 47770539528273.906)
print(S.check())
print (S.model())


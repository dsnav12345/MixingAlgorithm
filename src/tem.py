from docplex.mp.model import Model

sol = Model()

x = sol.integer_var()
y = sol.integer_var()

a=1
b=2
c=3

sol.add_constraint(x*a+y*b<=c)

sol.export_as_lp()
print(sol.lp_string)

a=5
b=4

sol.export_as_lp()
print(sol.lp_string)

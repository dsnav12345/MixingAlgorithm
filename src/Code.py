from docplex.mp.model import Model

m = int(input('Mixer size: '))
C = list(map(int, input('Input Reagents: ').split()))
T = int(input('Final concentration: '))
d = int(input('Depth: '))

n = len(C)
k = 2
w = []
for i in range(d+1):
    w.append([])
    if i == 0:
        continue
    for j in range(k):
        w[i].append([])
        for l in range(k):
            w[i][j].append(0)

teml = [0, ]*(k*k*d)


def next_perm():
    for i in range(len(teml)):
        teml[i] += 1
        if teml[i] == m:
            teml[i] = 0
        else:
            break

        if i == len(teml)-1 and teml[i] == 0:
            return False
    idx = 0
    for i in range(d):
        for j in range(k):
            for l in range(k):
                w[i+1][j][l] = teml[idx]
                idx += 1
    return True


while next_perm():
    try:
        Tree = Model()
        a = []
        X = []

        for i in range(d+1):
            a.append([])
            X.append([])
            if i == 0:
                X[i].append(Tree.integer_var(name='X_{}_{}'.format(i,0)))
                a[i].append([])
                for l in range(n):
                    a[i][0].append(Tree.integer_var(ub=m-1, name='a_{}_{}_{}'.format(i, 0, l)))
                continue

            for j in range(k):
                a[i].append([])
                X[i].append(Tree.integer_var(name='X_{}_{}'.format(i, j)))
                for l in range(n):
                    a[i][j].append(Tree.integer_var(ub=m-1, name='a_{}_{}_{}'.format(i, j, l)))

        for i in range(d+1):
            for j in range(len(a[i])):
                if i != d:
                    Tree.add_constraint(sum(a[i][j][l]*C[l] for l in range(n))+sum(w[i+1][l][j]*X[i+1][l] for l in range(k)) == X[i][j]*m)
                    Tree.add_constraint(sum(a[i][j][l] for l in range(n))+sum(w[i+1][l][j] for l in range(k)) <= m)
                else:
                    Tree.add_constraint(sum(a[i][j][l]*C[l] for l in range(n)) == X[i][j]*m)
                    Tree.add_constraint(sum(a[i][j][l] for l in range(n)) <= m)
                if i != 0:
                    Tree.add_constraint(sum(w[i][j][l] for l in range(k)) <= m)

        Tree.add_constraint(X[0][0] == T)

        Tree.set_objective('min', sum(X[i][j] for i in range(1, d+1) for j in range(k)))

        Tree.solve()
        Tree.print_solution()

        # cpx = Tree.get_cplex()
        # cpx.populate_solution_pool()
        # cnt = cpx.solution.pool.get_num()
        #
        # print(cnt)


    except Exception:
        pass

# while next_perm():
#     print(0)
#     sol = Tree.solve()
#     Tree.print_solution()
#     if sol is None:
#         print(1)

# for i in range(num):
#     print(cpx.solution.pool.get_values(i))

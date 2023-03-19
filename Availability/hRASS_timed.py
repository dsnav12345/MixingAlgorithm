import os
import sys
import time
from threading import *

from z3 import *

final = [float('inf'), [], -1]

Ans = math.inf
n_m = 0
n_i = 0
n_w = 0
h_n_m = 0
h_n_w = 0
h_n_i = 0
h_sat = 1
n_mix = []


def limit_time(amount):
    time.sleep(amount)
    print(final[2], final[0], h_n_i, h_n_m, h_n_w, Ans, n_i, n_m, n_w, h_sat)
    sys.stdout.close()
    os._exit(0)


def calc_obj(alpha, cst):
    N = len(cst)
    tot = 0

    for r in range(N):
        for x in alpha[r]:
            for y in x:
                tot += (y * cst[r])
    return tot


n_args = len(sys.argv)

inp = [0, ] * (n_args - 1)
for i in range(1, n_args):
    inp[i - 1] = int(sys.argv[i].strip())

sys.stdout = open('./outputs/' + str(inp[0]) + '_' + str(inp[1]) + '_' + str(inp[2]) + '.txt', 'a')

# print(inp)

p = Thread(target=limit_time, args=(inp[0] * inp[1] * inp[2] * 60,))
p.start()
p.join(1)

M_max = inp[0]
d = inp[1]
R = inp[2]

B = [0, ] * R
cst = [0, ] * R
av = [0, ] * R

for i in range(R):
    B[i] = inp[3 + i]
    cst[i] = inp[3 + i] * 10000
    cst[i] //= (M_max ** d)
    av[i] = inp[R + 3 + i]

T = inp[2 * R + 3]

for m in range(2, M_max + 1):
    W = [[B[k] * (m ** (d - j)) for j in range(d + 1)] for k in range(R)]
    val = [m ** (d - j) for j in range(d + 1)]

    X = [[Int('X_{}_{}'.format(k, j)) for j in range(d + 1)] for k in range(R)]

    S = Optimize()

    C1 = []
    C2 = []
    Obj = []
    for k in range(R):
        for j in range(d + 1):
            C1.append(W[k][j] * X[k][j])
            C2.append(X[k][j] * val[j])
            Obj.append(X[k][j] * cst[k])
            S.add(And(0 <= X[k][j], X[k][j] < m))
        # S.add(sum(X[k]) <= av[k])

    S.add(sum(C1) == T * (m ** d))
    S.add(sum(C2) <= (m ** d))
    ans = S.minimize(sum(Obj))

    if str(S.check()) == 'sat':
        tem = int(str(ans.value()))
        # print(tem, m)

        if tem > final[0]:
            continue

        ret = []
        model = S.model()
        for k in range(R):
            ret.append([])
            for j in range(d + 1):
                ret[k].append(int(str(model[X[k][j]])))

        final = [int(str(ans.value())), ret, m]

n_mix = [0, ] * (d + 1)

sys.stdout.flush()

if final[2] == -1:
    print('Unsat for hRASS')
    sys.stdout.close()
    os._exit(0)

sm = 0
m = final[2]
for i in range(d, 0, -1):
    for j in range(R):
        sm += final[1][j][i]
    n_mix[i - 1] = sm // m
    if (sm % m) != 0:
        n_mix[i - 1] += 1
    sm = n_mix[i - 1]

h_n_m = sum(n_mix)
h_n_w = (h_n_m - 1) * (m - 1)
for r in range(R):
    if sum(final[1][r]) > av[r]:
        h_sat = 0
    h_n_i += sum(final[1][r])


S = Solver()

C = [[Int('C_{}_{}'.format(i, j)) for j in range(n_mix[i])] for i in range(d + 1)]
W = [[[Int('W_{}_{}_{}'.format(i, k, l)) for l in range(n_mix[i - 1])] for k in range(n_mix[i])] for i in range(d + 1)]
Alpha = [[[Int('Alpha_{}_{}_{}'.format(r, i, k)) for k in range(n_mix[i])] for i in range(d + 1)] for r in range(R)]

for i in range(d + 1):
    for k in range(n_mix[i]):
        if i != d:
            S.add(m * C[i][k]
                  == sum([W[i + 1][l][k] * C[i + 1][l] for l in range(n_mix[i + 1])])
                  + sum([Alpha[r][i][k] * B[r] for r in range(R)]))
            S.add(m >= sum([W[i + 1][l][k] for l in range(n_mix[i + 1])]) + sum([Alpha[r][i][k] for r in range(R)]))
        else:
            S.add(m * C[i][k] == sum([Alpha[r][i][k] * B[r] for r in range(R)]))
            S.add(m >= sum([Alpha[r][i][k] for r in range(R)]))

        S.add(sum([W[i][k][l] for l in range(n_mix[i - 1])]) <= m)
        S.add(C[i][k] >= 0)

        for l in range(n_mix[i - 1]):
            S.add(And(W[i][k][l] >= 0, W[i][k][l] < m))

        if i != 0 and i != d:
            S.add(Or(sum([W[i][k][l] for l in range(n_mix[i - 1])]) > 0,
                     sum([W[i + 1][l][k] for l in range(n_mix[i + 1])]) + sum([Alpha[r][i][k] for r in range(R)]) == 0))
            S.add(Or(C[i][k] > 0, sum([W[i][k][l] for l in range(n_mix[i - 1])]) == 0))

        if i == d:
            S.add(Or(sum([W[i][k][l] for l in range(n_mix[i - 1])]) > 0,
                     sum([Alpha[r][i][k] for r in range(R)]) == 0))

        for r in range(R):
            S.add(And(Alpha[r][i][k] >= 0, Alpha[r][i][k] < m))

for r in range(R):
    S.add(sum(sum(Alpha[r][i]) for i in range(d + 1)) <= av[r])

S.add(C[0][0] == T)

idx = 1
while S.check() == sat and idx <= 100:
    mdl = S.model()
    Alpha_ = [[[int(str(mdl[Alpha[r][i][k]])) for k in range(n_mix[i])] for i in range(d + 1)] for r in range(R)]
    C_ = [[int(str(mdl[C[i][k]])) for k in range(n_mix[i])] for i in range(d + 1)]
    W_ = [[[int(str(mdl[W[i][k][l]])) for l in range(n_mix[i - 1])] for k in range(n_mix[i])] for i in range(d + 1)]

    cst_ = calc_obj(Alpha_, cst)
    nw_ = 0
    idx += 1

    for i in range(1, d + 1):
        for k in range(n_mix[i]):
            if C_[i][k] == 0:
                continue
            nw_ += (m - sum(W_[i][k]))

    if Ans > cst_:
        Ans = cst_
        n_m = sum(sum(int(bool(x)) for x in y) for y in C_)
        n_i = sum(sum(sum(x) for x in y) for y in Alpha_)
        n_w = nw_

    S.add(Or([Or([Or([Alpha[r][i][k] != Alpha_[r][i][k] for k in range(n_mix[i])]) for i in range(d + 1)]) for r in
              range(R)]))

print(final[2], final[0], h_n_i, h_n_m, h_n_w, Ans, n_i, n_m, n_w, h_sat)
sys.stdout.close()
os._exit(0)

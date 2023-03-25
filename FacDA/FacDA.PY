import os
import sys
import time
from threading import *

from z3 import *

min_mixers = float("inf")
min_total_cost = float("inf")
min_reagent_usage = float("inf")
min_wastage = float("inf")
max_buffer_usage = 0
maxM = 0


def getDivisors(n, m):
    i = 1
    div = []
    while i <= math.sqrt(n):
        if n % i == 0:
            if n / i == i:
                div.append(i)
            else:
                div.append(i)
                div.append(int(n / i))
        i = i + 1
    div.sort(reverse=True)
    for i in div:
        if i <= m and i != 1:
            return i
    return None


def get_factors(num, m):
    res = []
    num_c = num
    while num_c > m:
        re = getDivisors(num_c, m)
        if re is None:
            return []
        num_c = num_c / re
        res.append(int(re))
    if num_c != 1 and num_c <= m:
        res.append(int(num_c))
    return res


def limit_time(amount):
    time.sleep(amount)
    # print(ans_model)
    print(maxM, min_total_cost, min_reagent_usage, min_mixers, min_wastage)
    sys.stdout.close()
    os._exit(0)


n_args = len(sys.argv)

inp = [0, ] * (n_args - 1)
for i in range(1, n_args):
    inp[i - 1] = int(sys.argv[i].strip())
sys.stdout = open('./outputs/' + str(inp[0]) + '_' + str(inp[1]) + '_' + str(inp[2]) + '.txt', 'a')

# inp = [4, 4, 4, 55, 73, 82, 181, 10, 10, 10, 10, 6, 256]

p = Thread(target=limit_time, args=(3600,))
p.start()
p.join(1)

maxM = inp[0]
maxd = inp[1]
n_reg = inp[2]

conc = [0, ] * n_reg
Cost = [0, ] * n_reg
avl = [0, ] * n_reg
for i in range(n_reg):
    conc[i] = inp[3 + i]
    # Cost[i] = inp[3 + i] * 10000
    # Cost[i] //= (maxM ** maxd)
    Cost[i] = conc[i]
    avl[i] = inp[n_reg + 3 + i]
conc.append(0)
Cost.append(0)
avl.append(10000)
T = inp[-2]
req = T

min_mixers = float("inf")
min_total_cost = float("inf")
min_reagent_usage = float("inf")
min_wastage = float("inf")
max_buffer_usage = 0
target_sum = 0
opt = Optimize()
# print(maxM, maxd, n_reg, conc, avl, T)
# print("OK")
k = [Int("k_%s" % i) for i in range(len(conc))]
opt.add(sum([k[i] * conc[i] for i in range(len(conc))]) == req * (sum(([k[i] for i in range(len(conc))]))))
for i in range(len(k)):
    opt.add(k[i] >= 0)
opt.add(Or([k[i] > 0 for i in range(len(k))]))
run = 0
while opt.check() == sat and run < 15:
    # print(run)
    run = run + 1
    h = opt.minimize(sum([k[i] for i in range(len(k))]))
    opt.check()
    opt.lower(h)
    mo = opt.model()
    target_sum = sum([int(str(mo.evaluate(k[i]))) for i in range(len(k))])
    m = len(conc)
    # target_sum=maxM ** maxd
    fact = get_factors(target_sum, maxM)
    d_range = len(fact)
    if d_range != 0:
        break
    opt.add(Or([k[i] != mo.evaluate(k[i]) for i in range(len(k))]))
# for i in range(len(k)):
#     print(mo.evaluate(k[i]),"m ")
# print(target_sum)
m = len(conc)
# target_sum=maxM ** maxd
fact = get_factors(target_sum, maxM)
d_range = len(fact)
# print(fact)
if d_range == 0:
    print(maxM, min_total_cost, min_reagent_usage, min_mixers, min_wastage)
    os._exit(0)
# print(fact, flush=True)
s = Solver()
found = False
for mixers in range(1, 3):
    if found:
        continue
    for d in range(d_range, d_range + 1):
        factors = get_factors(target_sum, maxM)
        no_of_mixers = []
        for i in range(d):
            if i < d - 1:
                no_of_mixers.append(mixers)
            else:
                no_of_mixers.append(1)
        U = [Int("u_%s" % i) for i in range(m)]
        C = [[Int("c_%s_%s" % (i, j)) for j in range(no_of_mixers[i])] for i in range(d)]
        Alpha = [[[Int("Alpha_%s_%s_%s" % (i, j, l)) for l in range(no_of_mixers[j])] for j in range(d)] for i in
                 range(m)]
        M = [[Int("m_%s_%s" % (i, j)) for j in range(no_of_mixers[i])] for i in range(d)]
        W = [[[[Int("w_%s_%s_%s_%s" % (i, j, k1, l)) for l in range(no_of_mixers[j])] for k1 in range(no_of_mixers[i])]
              for j in range(d)] for i in range(d)]
        for i in range(d):
            for l in range(no_of_mixers[i]):
                s.add(M[i][l] * C[i][l] == sum(
                    [sum([W[p][i][k1][l] * C[p][k1] for k1 in range(no_of_mixers[p])]) for p in range(0, i)]) + sum(
                    [Alpha[m1][i][l] * conc[m1] for m1 in range(m)]))
                s.add(
                    M[i][l] == sum([sum([W[p][i][k1][l] for k1 in range(no_of_mixers[p])]) for p in range(0, i)]) + sum(
                        [Alpha[m1][i][l] for m1 in range(m)]))
                s.add(sum([sum([W[i][p][l][k1] for k1 in range(no_of_mixers[p])]) for p in range(i + 1, d)]) <= M[i][l])
                s.add(C[i][l] >= 0)
                s.add(M[i][l] >= 0)
                if i == d - 1:
                    pass
                else:
                    s.add(Or(M[i][l] == factors[d_range - i - 1], M[i][l] == 0))
                if i != d - 1:
                    s.add(
                        If(sum([sum([W[i][p][l][k1] for k1 in range(no_of_mixers[p])]) for p in range(i + 1, d)]) == 0,
                           M[i][l] == 0, M[i][l] > 0))

                for p in range(m):
                    s.add(Alpha[p][i][l] >= 0)
                    s.add(Or(Alpha[p][i][l] < M[i][l], M[i][l] == 0))
                for p in range(i + 1, d):
                    for l1 in range(no_of_mixers[p]):
                        s.add(W[i][p][l][l1] >= 0)
        for i in range(1, no_of_mixers[d - 1]):
            s.add(C[d - 1][i] == 0)
            s.add(M[d - 1][i] == 0)
        for m1 in range(m):
            s.add(sum([sum([Alpha[m1][i][j] for j in range(no_of_mixers[i])]) for i in range(d)]) <= avl[m1])
        s.add(C[d - 1][0] == req)
        s.add(M[d - 1][0] > 0)
        s.add(M[d - 1][0] == factors[0])
        # h = s.minimize(sum([sum([sum([Alpha[m1][i][j]*Cost[m1] for j in range(k)]) for i in range(d)]) for m1 in range(m)]))
        # print("test")

        # print("checking ",d)
        count = 0
        # print(s.check())
        # print(s.assertions())
        # print()
        # print()
        # print()

        if s.check() == sat:
            found = True
            while s.check() == sat and count < 100:
                # print("sat")
                count = count + 1
                # print(count)
                # print("checking")
                m2 = s.model()
                r = [[m2.evaluate(C[i][j]
                                  ) for j in range(no_of_mixers[i])]
                     for i in range(d)]
                # print_matrix(r)
                r1 = [[[m2.evaluate(Alpha[m1][i][j]) for m1 in range(m)] for j in range(no_of_mixers[i])]
                      for i in range(d)]
                # print_matrix(r1)
                r2 = [[[[m2.evaluate(W[i][j][k1][l]) for l in range(no_of_mixers[j])] for k1 in range(no_of_mixers[i])]
                       for j in range(d)]
                      for i in range(d)]
                # print_matrix(r2)
                present_total_cost = sum([sum([sum([int(str(m2.evaluate(Alpha[m1][i][j]))) * Cost[m1] for j in
                                                    range(no_of_mixers[i])]) for i in range(d)]) for m1 in range(m)])
                if d != 1:
                    s.add(Or([Or([Or([Alpha[m1][i][j] != m2.evaluate(Alpha[m1][i][j]) for m1 in range(m)]) for j in
                                  range(no_of_mixers[i])]) for i in range(d)]))
                    # s.add(Or([Or([C[i][j]!= m2.evaluate(C[i][j]) for j in range(no_of_mixers[i])]) for i  in range(d-1)]))
                # s.add(Or([Or([M[i][j]!= m2.evaluate(M[i][j]) for j in range(k)]) for i  in range(d)]))
                # print(present_total_cost)
                if present_total_cost < min_total_cost:
                    found = True
                    ans_model = m2
                    min_total_cost = present_total_cost
                    pres_reagent_usage = sum([sum([sum([int(str(m2.evaluate(Alpha[m1][i][j]))) for j in
                                                        range(no_of_mixers[i])]) for i in range(d)]) for m1 in
                                              range(m - 1)])
                    min_reagent_usage = min(min_reagent_usage, pres_reagent_usage)
                    pres_wastage = sum([sum([sum([int(str(m2.evaluate(Alpha[m1][i][j]))) for j in
                                                  range(no_of_mixers[i])]) for i in range(d)]) for m1 in
                                        range(m)]) - int(str(m2.evaluate(M[d - 1][0])))
                    min_wastage = min(min_wastage, pres_wastage)
                    cnt = 0
                    for i in range(d):
                        for j in range(no_of_mixers[i]):
                            if int(str(m2.evaluate(M[i][j]))) != 0:
                                cnt = cnt + 1
                    min_mixers = min(min_mixers, cnt)

# print(ans_model)
print(maxM, min_total_cost, min_reagent_usage, min_mixers, min_wastage)
sys.stdout.close()
os._exit(0)

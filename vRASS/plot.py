import sys

from matplotlib import pyplot as plt
import numpy as np

unsat_cnt = 0
avh = 0
avv = 0
t_out = 0
cntm = [0, ] * 5
cntd = [0, ] * 3

data = []

for i in range(2):
    data.append([])
    for j in range(4):
        data[i].append([])
        for k in range(2):
            if i == 0:
                data[i][j].append([0, ] * 5)
            else:
                data[i][j].append([0, ] * 3)

for m in range(2, 7):
    for d in range(3, 6):
        for r in range(2, 6):
            sys.stdin = open('outputs/{}_{}_{}.txt'.format(m, d, r), 'r')
            input()
            for line in range(20):
                ls = list(input().split())
                if ls[0] == 'Unsat':
                    unsat_cnt += 1
                    continue

                if ls[9] == '0':
                    avh += 1
                    if ls[5] == 'inf':
                        avv += 1
                if ls[5] == 'inf':
                    t_out += 1
                    continue

                ls = list(map(int, ls))

                if 2 * (ls[1] - ls[5]) >= ls[1]:
                    print(m, d, r, line, ((ls[1] - ls[5]) / ls[1]))

                data[0][0][0][m - 2] += ls[1]
                data[0][0][1][m - 2] += ls[5]
                data[1][0][0][d - 3] += ls[1]
                data[1][0][1][d - 3] += ls[5]

                data[0][2][0][m - 2] += ls[3]
                data[0][2][1][m - 2] += ls[7]
                data[1][2][0][d - 3] += ls[3]
                data[1][2][1][d - 3] += ls[7]

                data[0][1][0][m - 2] += ls[2]
                data[0][1][1][m - 2] += ls[6]
                data[1][1][0][d - 3] += ls[2]
                data[1][1][1][d - 3] += ls[6]

                data[0][3][0][m - 2] += ls[4]
                data[0][3][1][m - 2] += ls[8]
                data[1][3][0][d - 3] += ls[4]
                data[1][3][1][d - 3] += ls[8]

                cntm[m - 2] += 1
                cntd[d - 3] += 1

for d in range(3, 6):
    data[1][0][0][d - 3] /= cntd[d - 3]
    data[1][0][1][d - 3] /= cntd[d - 3]
    data[1][1][0][d - 3] /= cntd[d - 3]
    data[1][1][1][d - 3] /= cntd[d - 3]
    data[1][2][0][d - 3] /= cntd[d - 3]
    data[1][2][1][d - 3] /= cntd[d - 3]
    data[1][3][0][d - 3] /= cntd[d - 3]
    data[1][3][1][d - 3] /= cntd[d - 3]

for m in range(2, 7):
    data[0][0][0][m - 2] /= cntm[m - 2]
    data[0][0][1][m - 2] /= cntm[m - 2]
    data[0][1][0][m - 2] /= cntm[m - 2]
    data[0][1][1][m - 2] /= cntm[m - 2]
    data[0][2][0][m - 2] /= cntm[m - 2]
    data[0][2][1][m - 2] /= cntm[m - 2]
    data[0][3][0][m - 2] /= cntm[m - 2]
    data[0][3][1][m - 2] /= cntm[m - 2]

plt.rcParams['font.size'] = 15
x = [np.arange(5), np.arange(3)]
width = [0.3, 0.18]
labels = [['2', '3', '4', '5', '6'], ['3', '4', '5']]

y_l = ['Avg Cost', 'Avg # reagents used', 'Avg # mixing steps', 'Avg # Waste produced']
x_l = ['Mixer size', 'Depth']

################### Combined Graph production ###########################################

plt.rcParams['figure.figsize'] = [20, 10]
fig, ax = plt.subplots(2, 4)
plt.subplots_adjust(left=0.06, right=0.98, top=0.9, bottom=0.1)

for i in range(2):
    for j in range(4):
        rect = ax[i, j].bar(x[i] - (width[i] / 2), data[i][j][0], width[i], label='hRASS', color='r', edgecolor='black')
        # ax[i, j].bar_label(rect, padding=3)
        rect = ax[i, j].bar(x[i] + (width[i] / 2), data[i][j][1], width[i], label='vRASS', color='b', edgecolor='black')
        # ax[i, j].bar_label(rect, padding=3)

        ax[i, j].set_ylabel(y_l[j])
        ax[i, j].set_xlabel(x_l[i])

        ax[i, j].set_xticks(x[i])
        ax[i, j].set_xticklabels(labels[i])
        ax[i, j].legend()
fig.savefig('Plots/All_Graphs.png')

################### Individual Graph production ###########################################

fig = [[], []]
ax = [[], []]
name_x = ['Cst', 'Ni', 'Nm', 'Nw']
name_y = ['Mix', 'Depth']
for i in range(2):
    for j in range(4):
        fig[i].append(plt.figure())
        ax[i].append(fig[i][j].add_subplot())
        rect = ax[i][j].bar(x[i] - width / 2, data[i][j][0], width, label='hRASS', color='r', edgecolor='black')
        # ax[i, j].bar_label(rect, padding=3)
        rect = ax[i][j].bar(x[i] + width / 2, data[i][j][1], width, label='vRASS', color='b', edgecolor='black')
        # ax[i, j].bar_label(rect, padding=3)

        ax[i][j].set_ylabel(y_l[j])
        ax[i][j].set_xlabel(x_l[i])

        ax[i][j].set_xticks(x[i])
        ax[i][j].set_xticklabels(labels[i])
        ax[i][j].legend()

        fig[i][j].savefig('Plots/{}_vs_{}.png'.format(name_x[j], name_y[i]))


print(unsat_cnt, t_out, avh, avv)
print(cntm)
print(cntd)
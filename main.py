"""
The purpose of this script is to find the optimum segment lengths of a straandbest leg linkage

author: mikekraso@gmail.com
December 17th, 2024
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

from modules.genetic_algorithm import geneticAlgorithm
from modules.evaluation import evaluation
from modules.linkage_function import produce_linkage_path

names = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm'
]

# use the known ideal values as a starting point for the mins and max gene ranges
ideal = [38.0, 41.5, 39.3, 40.1, 55.8, 39.4, 36.7, 65.7, 49.0, 50.0, 61.9, 7.8, 15.0]
gene_info = {names[iii]: [val - (val / 2), val + (val / 2)] for iii, val in enumerate(ideal)}

ga = geneticAlgorithm(
    gene_info=gene_info,
    numpopinit=200,
    iters=100,
)

divs = 128  # 320
bests = []
all_est = []
while ga.continue_status:

    print('mpk: starting iteration:', ga.current_iter)

    est = []
    for genome in ga.population:
        pts = produce_linkage_path(ga, genome, divisions=divs)

        est.append(pts)

    ga.est = est

    print('starting fitness...')
    ga.fitness(fitfunc=evaluation)

    all_est += ga.est
    bests.append(ga.est[np.where(ga.score == np.min(ga.score))[0][0]])

    print('starting selection...')
    ga.selection(numparents=20)

    print('starting crossover...')
    ga.crossover(numchild=2, numcrosspts=4)

    print('starting mutation...')
    ga.mutation(mrates=0.8, nummutations=2)  # [0.1, 0.05, 0.01, 0.005, 0.001])

    print('mpk: best score:', min(ga.score))

# plot all
fig, ax = plt.subplots(1, 1)

for iii, pts in enumerate(all_est):

    if pts == ga.fail_value:
        continue

    xxx, yyy = zip(*pts)

    ax.plot(xxx, yyy)

ax.set_aspect('equal')
plt.savefig('./figures/all_est.png', dpi=600)

# plot bests
cmap = plt.get_cmap('jet')
colors = cmap(np.arange(int(ga.iters / 10)))

fig, ax = plt.subplots(1, 1)

for iii, bbb in enumerate(bests[-int(ga.iters / 10):]):
    xxx, yyy = zip(*bbb)

    ax.plot(xxx, yyy, color=colors[iii])
    ax.scatter(xxx, yyy, color=colors[iii])

ax.set_aspect('equal')
plt.savefig('./figures/bests.png', dpi=600)

# create a video!

import matplotlib.animation as animation

i_genome = [38.0, 41.5, 39.3, 40.1, 55.8, 39.4, 36.7, 65.7, 49.0, 50.0, 61.9, 7.8, 15.0]
i_points, i_links = produce_linkage_path(ga, i_genome, return_links=True, divisions=divs)

e_genome = ga.parents[0]
e_points, e_links = produce_linkage_path(ga, e_genome, return_links=True, divisions=divs)

fig, ax = plt.subplots(1, 1)
ax.set_aspect('equal')

ax.set_xlim([-200, 100])
ax.set_ylim([-200, 100])

xxx_i, yyy_i = zip(*i_points)
line1 = ax.plot(xxx_i, yyy_i, color='blue')[0]

xxx_e, yyy_e = zip(*e_points)
line2 = ax.plot(xxx_e, yyy_e, color='orange')[0]

line_i = ax.plot(i_links[0][0], i_links[0][1], color='gray')[0]
line_e = ax.plot(e_links[0][0], e_links[0][1], color='black')[0]

def update(frame):

    line1.set_xdata(xxx_i)
    line1.set_ydata(yyy_i)

    line2.set_xdata(xxx_e)
    line2.set_ydata(yyy_e)

    line_i.set_xdata(i_links[frame][0])
    line_i.set_ydata(i_links[frame][1])

    line_e.set_xdata(e_links[frame][0])
    line_e.set_ydata(e_links[frame][1])

    return (line1, line2, line_i, line_e)

print('anifunc')
ani = animation.FuncAnimation(fig=fig, func=update, frames=len(i_points), interval=30)

print('writing gif')
writergif = animation.PillowWriter(fps=30)
ani.save('./figures/animation.gif',writer=writergif)

print('done')



"""
The purpose of this script is to find the optimum segment lengths of a straandbest leg linkage

author: mikekraso@gmail.com
December 17th, 2024
"""

from modules.genetic_algorithm import geneticAlgorithm
from modules.evaluation import *

ga = geneticAlgorithm(
    initscalars=[10,10,10,10,10,10,10,10,10],
    numpopinit=500,
    iters=100,
)

while ga.continue_status:

    print('mpk: starting iteration:', ga.current_iter)

    print('function that determines traced path goes here')

    print('starting fitness...')
    ga.fitness(fitfunc=evaluation)

    print('starting selection...')
    ga.selection(numparents=20)

    print('starting crossover...')
    ga.crossover(numchild=2, numcrosspts=2)

    print('starting mutation...')
    ga.mutation(mrates=0.8, nummutations=2)  # [0.1, 0.05, 0.01, 0.005, 0.001])

    print('mpk: best score:', min(ga.score))

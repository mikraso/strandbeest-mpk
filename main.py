"""
The purpose of this script is to find the optimum segment lengths of a straandbest leg linkage

author: mikekraso@gmail.com
December 17th, 2024
"""

from modules.genetic_algorithm import geneticAlgorithm
from modules.evaluation import evaluation
from modules.linkage_function import produce_linkage_path

names = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm'
]

ideal = [2 * val for val in [38.0, 41.5, 39.3, 40.1, 55.8, 39.4, 36.7, 65.7, 49.0, 50.0, 61.9, 7.8, 15.0]]

ga = geneticAlgorithm(
    initscalars=ideal,
    gene_names=names,
    numpopinit=1000,
    iters=10,
)

while ga.continue_status:

    print('mpk: starting iteration:', ga.current_iter)

    est = []
    for genome in ga.population:

        pts = produce_linkage_path(ga, genome)

        est.append(pts)

    ga.est = est

    print('starting fitness...')
    ga.fitness(fitfunc=evaluation)

    print('starting selection...')
    ga.selection(numparents=20)

    print('starting crossover...')
    ga.crossover(numchild=2, numcrosspts=2)

    print('starting mutation...')
    ga.mutation(mrates=0.8, nummutations=2)  # [0.1, 0.05, 0.01, 0.005, 0.001])

    print('mpk: best score:', min(ga.score))

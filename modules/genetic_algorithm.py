"""
The purpose of this script is to set up a simple genetic algorithm

author: mikekraso@gmail.com
December 17th, 2024
"""

import random

class geneticAlgorithm:

    def __init__(
            self,
            initscalars,
            gene_names,
            numpopinit,
            iters,
    ):
        
        self.initscalars = initscalars
        self.gene_names = gene_names
        self.numpopinit = numpopinit
        self.iters = iters

        self.current_iter = 0
        self.continue_status = True

        self.parents = None
        self.fitfunc = None
        self.score = None
        self.mutrates = None

        self.score_log=[]

        # build the initial population
        self.population = self.produce_genomes()

    def produce_genomes(self, number_to_produce=None, scalars=None):

        if number_to_produce is None:
            number_to_produce = self.numpopinit

        if scalars is None:
            scalars = self.initscalars

        genomes = []
        for iii in range(number_to_produce):
            genome = []
            for genescale in scalars:
                genome.append(random.random() * genescale)

            genomes.append(genome)

        return genomes

    def fitness(self, fitfunc):

        self.fitfunc = fitfunc
        self.score = []
        # how flat is the bottom section?
        for iii, genome in enumerate(self.population):
            self.score.append(self.fitfunc(genome))

        self.score_log.append(self.score)

    def selection(self, numparents):

        self.numparents = numparents
        # pick the best and keep them as parents

        genome_score_pairs = []
        for iii, genome in enumerate(self.population):
            genome_score_pairs.append((self.score[iii], genome))

        genome_score_pairs.sort()
        self.parents = []
        for gsp in genome_score_pairs[:self.numparents]:
            self.parents.append(gsp[1])

        self.population = self.parents.copy()

    def crossover(self, numchild, numcrosspts):

        for iii, genome in enumerate(self.parents):

            for nc in range(numchild):

                # select another parent
                pidx = iii * 1
                while pidx == iii:
                    pidx = random.choice(range(self.numparents))

                # identify indices to perform crossover at
                cidx = [0]
                while len(cidx) < numcrosspts + 1:

                    maybe_idx = random.choice(range(len(genome) - 1))

                    if maybe_idx not in cidx:
                        cidx.append(maybe_idx)

                cidx.append(len(genome))
                cidx.sort()

                # now create a list for each randomly chosen parent segment to be added to
                child = []
                for jjj in range(len(cidx) - 1):

                    child = child + random.choice(
                        (
                            genome[cidx[jjj]:cidx[jjj+1]],
                            self.population[pidx][cidx[jjj]:cidx[jjj+1]]
                        )
                    )

                self.population.append(child)

    def mutation(self, mrates, nummutations):

        if isinstance(mrates, float):
            mrates = mrates * random.random()

        elif isinstance(mrates, list):

            # annealing
            iters_per_step = int(self.iters / len(mrates))
            for iii in range(self.iters):
                print('here is where you interpolate')

        mut_pop = []
        for genome in self.population:
            for mmm in range(nummutations):
                midx = random.choice(range(len(genome)))
                msign = random.choice([-1, 1])

                genome[midx] = genome[midx] + (msign * mrates * genome[midx])

            mut_pop.append(genome)

        self.population = self.parents + mut_pop

        if self.current_iter >= self.iters -1 :
            self.continue_status = False

        self.current_iter += 1





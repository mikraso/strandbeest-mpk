"""
The purpose of this script is to house the function which computes the "forward kinematics" of the strandbeest
leg given a set of linkage lengths for segments and pivot geometry following the naming given at:

https://en.wikipedia.org/wiki/Jansen%27s_linkage#/media/File:Strandbeest_Leg_Proportions.svg

author: mikekraso@gmail.com
December 22nd, 2024
"""

# imports
import math

from modules.evaluation import find_high_low_portion

def dist(v1, v2):

    return (((v1[0] - v2[0])**2) + ((v1[1] - v2[1])**2))**0.5

def produce_linkage_path(ga, genome, divisions=64, return_links=False):
    """
    The purpose of this function is to take the linkage lengths in and compute the location of the foot at a set number
    of angles. These locations define the path of the foot and are returned by the function

    :param genome: list
        the definitional linkage lengths
    :param divisions:
        the number of divisions of the unit circle to solve at
    :return:
    """

    # rework genome to be a dictionary
    gnm = {ga.gene_names[iii]: gene for iii, gene in enumerate(genome)}
    # checks
    hyp = ((gnm['a']**2) + (gnm['l']**2))**0.5

    # triangle bde
    if (gnm['b'] + gnm['d'] < gnm['e']) or \
        (gnm['d'] + gnm['e'] < gnm['b']) or \
        (gnm['b'] + gnm['e'] < gnm['d']):
        return ga.fail_value

    # triangle ghi
    if (gnm['g'] + gnm['h'] < gnm['i']) or \
        (gnm['h'] + gnm['i'] < gnm['g']) or \
        (gnm['g'] + gnm['i'] < gnm['h']):
        return ga.fail_value

    # b + j must be larger than hyp + m
    if (gnm['b'] + gnm['j']) < (hyp + gnm['m']):
        return ga.fail_value

    # c + k must be larger than hyp + m
    if (gnm['c'] + gnm['k']) < (hyp + gnm['m']):
        return ga.fail_value

    # loop through the angles at which the geometry will be solved and solve
    delta_theta = 2 * math.pi / divisions
    theta = 0
    soln_pts = []
    try:
        linkages = []
        while theta < ((2 + 1/divisions) * math.pi):
            linkages.append(([], []))
            # calculate angles and vectors (following https://www.youtube.com/watch?v=n-8I00R3i1U)
            v_OA = (gnm['m'] * math.cos(theta),
                    gnm['m'] * math.sin(theta))
            v_OB = (-gnm['a'],
                    -gnm['l'])
            alpha = math.atan2(v_OA[1] - v_OB[1], v_OA[0] - v_OB[0])
            beta = math.acos(((dist(v_OA, v_OB)**2) + (gnm['b']**2) - (gnm['j']**2)) /
                              (2 * dist(v_OA, v_OB) * gnm['b']))
            v_OC = (-gnm['a'] + (gnm['b'] * math.cos(alpha + beta)),
                    -gnm['l'] + (gnm['b'] * math.sin(alpha + beta)))
            gamma = math.acos(((gnm['b']**2) + (gnm['d']**2) - (gnm['e']**2)) / (2 * gnm['b'] * gnm['d']))
            v_OD = (-gnm['a'] + (gnm['d'] * math.cos(alpha + beta + gamma)),
                    -gnm['l'] + (gnm['d'] * math.sin(alpha + beta + gamma)))
            delta = math.acos(((dist(v_OA, v_OB)**2) + (gnm['c']**2) - (gnm['k']**2)) /
                              (2 * dist(v_OA, v_OB) * gnm['c']))
            v_OE = (-gnm['a'] + (gnm['c'] * math.cos(alpha - delta)),
                    -gnm['l'] + (gnm['c'] * math.sin(alpha - delta)))
            epsilon = math.atan2(v_OD[1] - v_OE[1], v_OD[0] - v_OE[0])
            zeta = math.acos(((dist(v_OD, v_OE)**2) + (gnm['g']**2) - (gnm['f']**2)) /
                             (2 * dist(v_OD, v_OE) * gnm['g']))
            v_OF = (-gnm['a'] + (gnm['c']*math.cos(alpha-delta) + (gnm['g']*math.cos(epsilon+zeta))),
                    -gnm['l'] + (gnm['c']*math.sin(alpha-delta) + (gnm['g']*math.sin(epsilon+zeta))))
            nu_ = math.acos(((gnm['g']**2) + (gnm['i']**2) - (gnm['h']**2)) / (2*gnm['g']*gnm['i']))
            v_OG = (-gnm['a'] + (gnm['c']*math.cos(alpha-delta) + (gnm['i']*math.cos(epsilon+zeta+nu_))),
                    -gnm['l'] + (gnm['c']*math.sin(alpha-delta) + (gnm['i']*math.sin(epsilon+zeta+nu_))))

            soln_pts.append(v_OG)
            linkages[-1][0].append(0)
            linkages[-1][1].append(0)
            linkages[-1][0].append(v_OA[0])
            linkages[-1][1].append(v_OA[1])
            linkages[-1][0].append(v_OC[0])
            linkages[-1][1].append(v_OC[1])
            linkages[-1][0].append(v_OD[0])
            linkages[-1][1].append(v_OD[1])
            linkages[-1][0].append(v_OF[0])
            linkages[-1][1].append(v_OF[1])
            linkages[-1][0].append(v_OG[0])
            linkages[-1][1].append(v_OG[1])
            linkages[-1][0].append(v_OE[0])
            linkages[-1][1].append(v_OE[1])
            linkages[-1][0].append(v_OF[0])
            linkages[-1][1].append(v_OF[1])
            linkages[-1][0].append(v_OE[0])
            linkages[-1][1].append(v_OE[1])
            linkages[-1][0].append(v_OB[0])
            linkages[-1][1].append(v_OB[1])
            linkages[-1][0].append(v_OD[0])
            linkages[-1][1].append(v_OD[1])
            linkages[-1][0].append(v_OB[0])
            linkages[-1][1].append(v_OB[1])
            linkages[-1][0].append(v_OC[0])
            linkages[-1][1].append(v_OC[1])
            linkages[-1][0].append(v_OA[0])
            linkages[-1][1].append(v_OA[1])
            linkages[-1][0].append(v_OE[0])
            linkages[-1][1].append(v_OE[1])

            theta += delta_theta

    except Exception as e:

        # if hasattr(e, 'message'):
        #     print(e.message)
        # else:
        #     print(e)

        return ga.fail_value

    # # check for lowest not being laterally sequential
    # temp_pts = soln_pts.copy()
    # lows = find_high_low_portion(temp_pts)
    #
    # lows.sort()
    #
    # sequence = []
    # for iii, lll in enumerate(lows[:-1]):
    #     if lll[1] > lows[iii+1][1]:
    #         sequence.append(0)
    #     else:
    #         sequence.append(1)
    #
    # counter = 0
    # for iii, sss in enumerate(sequence[:-1]):
    #     if sss != sequence[iii+1]:
    #         counter += 1
    #
    # if counter > 1:
    #     return ga.fail_value
    #

    # check for highest not having multiple concavity flips
    temp_pts = soln_pts.copy()

    highs = find_high_low_portion(temp_pts, highlow='high', proportion=4)

    highs.sort()

    sequence = []
    for iii, hhh in enumerate(highs[:-1]):

        if hhh[1] > 0:
            return ga.fail_value

        if hhh[1] < highs[iii + 1][1]:
            sequence.append(0)
        else:
            sequence.append(1)

    counter = 0
    for iii, sss in enumerate(sequence[:-1]):
        if iii == 0:
            if sss != 0:
                return ga.fail_value
        if sss != sequence[iii + 1]:
            counter += 1

    if counter != 1:
        return ga.fail_value

    if return_links:
        return soln_pts, linkages
    else:
        return soln_pts


if __name__ == '__main__':

    import matplotlib.pyplot as plt
    from genetic_algorithm import geneticAlgorithm

    names = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm'
    ]

    ga = geneticAlgorithm(
        initscalars=[10] * len(names),
        gene_names=names,
        numpopinit=500,
        iters=100,
    )
    genome = [38.0, 41.5, 39.3, 40.1, 55.8, 39.4, 36.7, 65.7, 49.0, 50.0, 61.9, 7.8, 15.0]
    points = produce_linkage_path(ga, genome)

    fig, ax = plt.subplots(1, 1)

    xxx, yyy = zip(*points)

    ax.plot(xxx, yyy, markersize=0.4)
    # ax.scatter(xxx, yyy, markersize=0.4)

    ax.set_aspect('equal')
    plt.savefig('../figures/ideal.png', dpi=600)




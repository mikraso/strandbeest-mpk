"""
The purpose of this script is to house the function which computes the "forward kinematics" of the strandbeest
leg given a set of linkage lengths for segments and pivot geometry following the naming given at:

https://en.wikipedia.org/wiki/Jansen%27s_linkage#/media/File:Strandbeest_Leg_Proportions.svg

author: mikekraso@gmail.com
December 22nd, 2024
"""

# imports
import math

def produce_linkage_path(ga, genome, divisions=32):
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
    tht = 0
    soln_pts = []
    while tht < (2 * math.pi):

        # calculate coordinates
        m_coords = [(0,0),                      (gnm['m']*math.cos(tht), gnm['m']*math.sin(tht))]
        l_coords = [(0,0),                      (0,0-gnm['l'])]
        a_coords = [(0-gnm['a'],0-gnm['l']),    (0,0-gnm['l'])]
        j_coords = [(xxx, yyy),                 m_coords[1]]
        k_coords = [(xxx, yyy),                 m_coords[1]]
        b_coords = [((0-gnm['a'], 0-gnm['l'])), (xxx, yyy)]
        c_coords = [((0-gnm['a'], 0-gnm['l'])), (xxx, yyy)]
        d_coords = [((0-gnm['a'], 0-gnm['l'])), (xxx, yyy)]
        e_coords = [(xxx, yyy),                 (xxx, yyy)]
        f_coords = [(xxx, yyy),                 (xxx, yyy)]
        g_coords = [(xxx, yyy),                 (xxx, yyy)]
        h_coords = [(xxx, yyy),                 (xxx, yyy)]
        i_coords = [(xxx, yyy),                 (xxx, yyy)]

        # can it be as simple as adding to the x and y coordinates of known coordinates?
        # i would need to know the orientation of the segment to know what direction to go

        soln_pts.append((xxx, yyy))
        tht += delta_theta



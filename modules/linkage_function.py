"""
The purpose of this script is to house the function which computes the "forward kinematics" of the strandbeest
leg given a set of linkage lengths for segments and pivot geometry following the naming given at:

https://en.wikipedia.org/wiki/Jansen%27s_linkage#/media/File:Strandbeest_Leg_Proportions.svg

author: mikekraso@gmail.com
December 22nd, 2024
"""

# imports
import math

def dist(v1, v2):

    return (((v1[0] - v2[0])**2) + ((v1[1] - v2[1])**2))**0.5

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
    theta = 0
    soln_pts = []
    while theta < (2 * math.pi):

        # calculate angles and vectors (following https://www.youtube.com/watch?v=n-8I00R3i1U)
        v_OA = (gnm['m'] * math.cos(theta),
                gnm['m'] * math.sin(theta))
        v_OB = (-gnm['a'],
                -gnm['l'])
        alpha = math.atan2(v_OA[1] - v_OB[1], v_OA[0] - v_OB[0])
        beta  = math.acos(((dist(v_OA, v_OB)**2) + (gnm['b']**2) - (gnm['j']**2)) /
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
        v_OG = (-gnm['a'] + (gnm['c']*math.cos(alpha-delta) + (gnm['i']*math.cos(epsilon+zeta+nu))),
                -gnm['l'] + (gnm['c']*math.sin(alpha-delta) + (gnm['i']*math.sin(epsilon+zeta+nu))))


        # can it be as simple as adding to the x and y coordinates of known coordinates?
        # i would need to know the orientation of the segment to know what direction to go

        soln_pts.append(v_OG)

        theta += delta_theta


    return soln_pts
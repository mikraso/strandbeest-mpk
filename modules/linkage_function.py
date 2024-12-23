"""
The purpose of this script is to house the function which computes the "forward kinematics" of the strandbeest
leg given a set of linkage lengths for segments and pivot geometry following the naming given at:

https://en.wikipedia.org/wiki/Jansen%27s_linkage#/media/File:Strandbeest_Leg_Proportions.svg

author: mikekraso@gmail.com
December 22nd, 2024
"""

# imports


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
    # checks
    # triangle bde
    if (genome['b'] + genome['d'] < genome['e']) or \
        (genome['d'] + genome['e'] < genome['b']) or \
        (genome['b'] + genome['e'] < genome['d']):
        return ga.fail_value

    # triangle ghi
    if (genome['g'] + genome['h'] < genome['i']) or \
        (genome['h'] + genome['i'] < genome['g']) or \
        (genome['g'] + genome['i'] < genome['h']):
        return ga.fail_value

    # j + k must be larger than b + c
    
    # additional checks observed from the mechanism?


    # starting coordinates (unit circle origin)
    m_coords = [(0,0),                         (genome['m'],0)]  # need to functionalize second coords
    l_coords = [(0,0),                         (0,0-genome['l'])]
    a_coords = [(0-genome['a'],0-genome['l']), (0,0-genome['l'])]



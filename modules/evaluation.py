"""
The purpose of this script is to house the function that evaluates the leg path

author: mikekraso@gmail.com
December 17th, 2024
"""

import random

def evaluation(points):

    # select the lowest 12 points
    lows = []
    while len(lows) < int(len(points)/2.67):

        min_idx = None
        min_y = 10000
        for idx, pnt in enumerate(points):

            if pnt[1] < min_y:
                min_y = pnt[1]
                min_idx = idx

        lows.append(points[min_idx])
        points.remove(points[min_idx])

    # with the lowest points identified, now test to see how tightly gathered to the mean they are (flatness)
    y_vals = []
    for pnt in lows:
        y_vals.append(pnt[1])

    mean_val = sum(y_vals) / len(y_vals)

    mean_removed = [y_v - mean_val for y_v in y_vals]

    abs_error = [abs(val) for val in mean_removed]

    max_error = max(abs_error)

    normalized_abs_error = [a_e / max_error for a_e in abs_error]

    mean_norm_abs_error = sum(normalized_abs_error) / len(normalized_abs_error)

    return mean_norm_abs_error



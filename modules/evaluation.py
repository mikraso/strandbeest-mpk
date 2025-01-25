"""
The purpose of this script is to house the function that evaluates the leg path

author: mikekraso@gmail.com
December 17th, 2024
"""

import random

def find_high_low_portion(points, highlow='low', proportion=2.65):

    if highlow == 'low':
        # select the lowest 12 points
        lows = []
        og_points_len = len(points)
        while len(lows) < int(og_points_len/proportion):

            min_idx = None
            min_y = 1e6
            for idx, pnt in enumerate(points):

                if pnt[1] < min_y:
                    min_y = pnt[1]
                    min_idx = idx

            lows.append(points[min_idx])
            points.remove(points[min_idx])

        return lows

    elif highlow == 'high':
        # select the lowest 12 points
        highs = []
        og_points_len = len(points)
        while len(highs) < int(og_points_len / proportion):

            max_idx = None
            max_y = -1e6
            for idx, pnt in enumerate(points):

                if pnt[1] > max_y:
                    max_y = pnt[1]
                    max_idx = idx

            highs.append(points[max_idx])
            points.remove(points[max_idx])

        return highs

def PolyArea(x,y):
    import numpy as np
    return 0.5*np.abs(np.dot(x, np.roll(y, 1))-np.dot(y, np.roll(x, 1)))

def evaluation(points):

    temp_pts = points.copy()

    # # maximize area, too
    # xxx = []
    # yyy = []
    # for pnt in points:
    #     xxx.append(pnt[0])
    #     yyy.append(pnt[1])
    #
    # area = PolyArea(xxx, yyy)

    # we know we want more points in the walking portion of the curve so give that a boost
    max_y = max([pnt[1] for pnt in temp_pts])
    min_y = min([pnt[1] for pnt in temp_pts])

    avg_y = (max_y + min_y) / 2
    counter = 0
    for pnt in temp_pts:
        if pnt[1] > avg_y:
            counter += 1

    ud_ratio = counter / (len(temp_pts) - counter)

    # we know we want a flat bottom so check how flat the lowest portion of points is
    lows = find_high_low_portion(temp_pts, proportion=2.25)

    length = max([pnt[0] for pnt in lows]) - min([pnt[0] for pnt in lows])

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

    # if ud_ratio > 1:
    #     return mean_norm_abs_error * ud_ratio  # / area
    #
    # else:
    length_counteractor = 40
    return mean_norm_abs_error * (ud_ratio**2) * (length_counteractor / length)



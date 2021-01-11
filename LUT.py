import numpy as np

distances_LUT = np.array(
    [15, 17, 20, 28, 35, 44, 47, 58, 89, 90])
speeds_LUT = np.array(
    [58, 59, 65, 70, 70, 79, 86, 95, 103, 109])


def get_thrower_speed2(distance):
    best_match = speeds_LUT[np.argmin(np.absolute(distances_LUT - (720-distance)))]
    return best_match


distances_LUT = np.array(
    [21, 22, 23, 24, 25, 30, 33, 34, 35, 37, 40, 47, 50, 69, 103, 130])
speeds_LUT = np.array(
    [130, 126, 122, 105, 116, 96, 73, 105, 92, 85, 87, 88, 67, 75, 55, 63])


def get_thrower_speed(distance):
    best_match = speeds_LUT[np.argmin(np.absolute(distances_LUT - distance))]
    print(best_match)
    return best_match

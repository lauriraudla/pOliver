import numpy as np

#distances_LUT = np.array(
    #[26, 29, 32, 33,40, 43, 51, 52, 55, 59, 68, 77, 78, 96, 98, 104, 140, 182, 223, 314])
distances_LUT = np.array(
    [8, 11, 11, 12, 16, 17, 19, 20, 21, 23, 26, 31, 34, 38, 39, 47, 55, 71, 88, 121])
speeds_LUT = np.array(
    [120, 125, 111, 115, 110, 105, 100, 96, 95, 90, 85, 83, 80, 75, 72, 70, 65, 60, 55, 51])


def get_thrower_speed(distance):
    best_match = speeds_LUT[np.argmin(np.absolute(distances_LUT - distance))]
    print("igrek: " + str(distance))
    print("spiid: " + str(best_match))
    return best_match


#distances_LUT = np.array(
    #[21, 22, 23, 24, 25, 30, 33, 34, 35, 37, 40, 47, 50, 69, 103, 130])
#speeds_LUT = np.array(
    #[130, 126, 122, 105, 116, 96, 73, 105, 92, 85, 87, 88, 67, 75, 55, 63])


def get_thrower_speed2(distance):
    best_match = speeds_LUT[np.argmin(np.absolute(distances_LUT - distance))]
    print(best_match)
    return best_match

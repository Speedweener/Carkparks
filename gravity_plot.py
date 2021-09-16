import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import matplotlib.colors as color
import json
import gmaps
import math

import gmplot
import random

import pandas as pd

color_codes = {
    0: "#ff0000",  # RED
    1: "#ffa500",  # ORANGE
    2: "#ffff00",  # YELLOW
    3: "#008000",  # GREEN
    4: "#0000ff",  # BLUE
    5: "#4b0082",  # INDIGO
    6: "#ee82ee",  # VIOLET
    7: "#0c0c0c",  # BLACK
    8: "#ffffff",  # WHITE
}


def f(x, y):
    s = np.hypot(x, y)
    phi = np.arctan2(y, x)
    tau = s + s * (1 - s) / 5 * np.sin(6 * phi)
    return 5 * (1 - tau) + tau


def interpolate(lat_sample, long_sample, values, points=100, levels=10, method='cubic'):
    # Grid does not have to be that many points
    lat_space = np.linspace(min(lat_sample), max(lat_sample), points)
    long_space = np.linspace(min(long_sample), max(long_sample), points)
    x, y = np.meshgrid(long_space, lat_space)

    Ti = griddata((long_sample, lat_sample), values, (x, y), method=method)

    contour_map = plt.contourf(x, y, Ti, levels=levels)

    '''
       [WEIGHT][AREA][POLYGON/HOLE][POINT][LAT/LONG]
    eg. [1][0][1][2][1]
    The 2nd area, first area, 1st hole (0 is polygon), 3rd point, longitude
    Each weight will have certain areas(polygons), and each area will have different
    coordinates
    '''
    return contour_map


'''
This method attempts to separate a polygon with holes into separate polygons,
the first being the outline of the polygon, and the rest being the different holes
of the polygon

It does this by checking for continuity of the polygon by comparing the current and
starting long and lat coordinates. Coordinates that match indicate the end of the 
polygon. The code then checks if there are other polygons (holes) to be plotted.

Separation is done so that polygons with holes can be properly plotted in Google Maps

First value (start) will be appended last as the matched value
'''


def polygon_hole_split(polygon):
    polygon_and_holes = []
    points_container = []
    num_points = len(polygon)

    start_long = polygon[0][0]
    start_lat = polygon[0][1]
    index = 1  # The next value

    while index < num_points:

        curr_long = polygon[index][0]
        curr_lat = polygon[index][1]

        if curr_long == start_long and curr_lat == start_lat:

            points_container.append((curr_lat, curr_long))
            polygon_and_holes.append(points_container.copy())
            points_container.clear()

            index += 1

            if index < num_points:
                start_long = polygon[index][0]
                start_lat = polygon[index][1]
                index += 1  # The next value

        else:
            points_container.append((curr_lat, curr_long))
            index += 1

    return polygon_and_holes


def gmap_plot():
    gmap1 = gmplot.GoogleMapPlotter(1.2847,
                                    103.8117, 21, map_type='satellite')

    gmap1.max_intensity = 0.1
    gmap1.point_radius = 1

    latitude_sample = [1.2847, 1.2848, 1.2849, 1.285, 1.2851, 1.2852, 1.2852999999999999, 1.2853999999999999,
                       1.2854999999999999, 1.2855999999999999, 1.2847, 1.2848, 1.2849, 1.285, 1.2851, 1.2852,
                       1.2852999999999999, 1.2853999999999999, 1.2854999999999999, 1.2855999999999999, 1.2847, 1.2848,
                       1.2849, 1.285, 1.2851, 1.2852, 1.2852999999999999, 1.2853999999999999, 1.2854999999999999,
                       1.2855999999999999, 1.2847, 1.2848, 1.2849, 1.285, 1.2851, 1.2852, 1.2852999999999999,
                       1.2853999999999999, 1.2854999999999999, 1.2855999999999999, 1.2847, 1.2848, 1.2849, 1.285,
                       1.2851, 1.2852, 1.2852999999999999, 1.2853999999999999, 1.2854999999999999, 1.2855999999999999,
                       1.2847, 1.2848, 1.2849, 1.285, 1.2851, 1.2852, 1.2852999999999999, 1.2853999999999999,
                       1.2854999999999999, 1.2855999999999999, 1.2847, 1.2848, 1.2849, 1.285, 1.2851, 1.2852,
                       1.2852999999999999, 1.2853999999999999, 1.2854999999999999, 1.2855999999999999, 1.2847, 1.2848,
                       1.2849, 1.285, 1.2851, 1.2852, 1.2852999999999999, 1.2853999999999999, 1.2854999999999999,
                       1.2855999999999999, 1.2847, 1.2848, 1.2849, 1.285, 1.2851, 1.2852, 1.2852999999999999,
                       1.2853999999999999, 1.2854999999999999, 1.2855999999999999, 1.2847, 1.2848, 1.2849, 1.285,
                       1.2851, 1.2852, 1.2852999999999999, 1.2853999999999999, 1.2854999999999999, 1.2855999999999999]
    longitude_sample = [103.8117, 103.8117, 103.8117, 103.8117, 103.8117, 103.8117, 103.8117, 103.8117, 103.8117,
                        103.8117, 103.8118, 103.8118, 103.8118, 103.8118, 103.8118, 103.8118, 103.8118, 103.8118,
                        103.8118, 103.8118, 103.81190000000001, 103.81190000000001, 103.81190000000001,
                        103.81190000000001, 103.81190000000001, 103.81190000000001, 103.81190000000001,
                        103.81190000000001, 103.81190000000001, 103.81190000000001, 103.812, 103.812, 103.812, 103.812,
                        103.812, 103.812, 103.812, 103.812, 103.812, 103.812, 103.8121, 103.8121, 103.8121, 103.8121,
                        103.8121, 103.8121, 103.8121, 103.8121, 103.8121, 103.8121, 103.8122, 103.8122, 103.8122,
                        103.8122, 103.8122, 103.8122, 103.8122, 103.8122, 103.8122, 103.8122, 103.81230000000001,
                        103.81230000000001, 103.81230000000001, 103.81230000000001, 103.81230000000001,
                        103.81230000000001, 103.81230000000001, 103.81230000000001, 103.81230000000001,
                        103.81230000000001, 103.8124, 103.8124, 103.8124, 103.8124, 103.8124, 103.8124, 103.8124,
                        103.8124, 103.8124, 103.8124, 103.8125, 103.8125, 103.8125, 103.8125, 103.8125, 103.8125,
                        103.8125, 103.8125, 103.8125, 103.8125, 103.8126, 103.8126, 103.8126, 103.8126, 103.8126,
                        103.8126, 103.8126, 103.8126, 103.8126, 103.8126]
    weight_sample = [9.80812889029008, 9.807984177661622, 9.806559495962446, 9.806956764963843, 9.805823442144325,
                     9.809914022729686, 9.80968241927086, 9.80672916158248, 9.808537116524334, 9.805069858731638,
                     9.805784042133165, 9.806311139820245, 9.807236568231412, 9.809005620435926, 9.80626061971379,
                     9.808424087353403, 9.809656699105672, 9.806506584882046, 9.808049684149685, 9.807671207774785,
                     9.805144011983813, 9.805483497359164, 9.806074906327101, 9.80829464675826, 9.807975987236965,
                     9.809705068849658, 9.80834205496633, 9.808640235335215, 9.809396918983007, 9.806503433001225,
                     9.809193703162727, 9.807470163149294, 9.809999574566886, 9.805474169740945, 9.807523611269701,
                     9.80686658485638, 9.80940471235577, 9.808830288668737, 9.807113971699327, 9.80724329179546,
                     9.807654317175295, 9.809161340412432, 9.806603892981242, 9.809241826925241, 9.80788718748318,
                     9.808910223553442, 9.808122277493553, 9.80732953213465, 9.808331005597516, 9.808948210899445,
                     9.807395952616844, 9.807170528777254, 9.806162320750824, 9.805205546720039, 9.80861429843123,
                     9.806954772391748, 9.805677130980143, 9.806705827166198, 9.808470121763396, 9.807288828602529,
                     9.805291531160268, 9.809783445139834, 9.80861418317851, 9.807751134159018, 9.80838182355061,
                     9.806775661454601, 9.809104544968637, 9.807543824714326, 9.808795371888426, 9.809558052716389,
                     9.806593501181663, 9.807280279227063, 9.805899238131529, 9.805982539772936, 9.806844625522363,
                     9.808142697138528, 9.807030529843926, 9.805988053034163, 9.809004055286433, 9.807076188597893,
                     9.80923544884448, 9.805490351012663, 9.80942019820369, 9.805159965612928, 9.809900781684062,
                     9.80554187264365, 9.809269399287288, 9.80514722920465, 9.805769289865252, 9.807989537442362,
                     9.808199588238333, 9.808074494072416, 9.809329506152901, 9.807640469959711, 9.806581612023928,
                     9.80835945925168, 9.806678679376079, 9.80773218445338, 9.807810362838671, 9.808357954197117]
    lat_space = np.linspace(min(latitude_sample), max(latitude_sample), 100)
    long_space = np.linspace(min(longitude_sample), max(longitude_sample), 100)

    X, Y = np.meshgrid(long_space, lat_space)

    Ti = griddata((longitude_sample, latitude_sample), weight_sample, (X, Y), method='cubic')

    # img_bounds = {'north': 1.2856, 'south': 1.2847, 'east': 103.8126+0.001, 'west': 103.8117+0.001}
    # gmap1.ground_overlay('https://drive.google.com/uc?export=view&id=1r0cQVzRXii8r05VEAYVnxVZVl7EcCfef', img_bounds)
    # gmap1.heatmap(lats=Y.ravel(), lngs=X.ravel(), weights=Ti.ravel())

    levels = np.linspace(min(weight_sample), max(weight_sample), 100)

    contour_map = plt.contourf(X, Y, Ti, levels=9)

    for weight in range(len(contour_map.allsegs)):
        for area in range(len(contour_map.allsegs[weight])):
            dat0 = contour_map.allsegs[weight][area]

            lat = []
            long = []

            prev_long = dat0[0][0]
            prev_lat = dat0[0][1]

            for points in range(len(dat0)):
                current_long = dat0[points][0]
                current_lat = dat0[points][1]

                if abs(current_long - prev_long) > 0.00001 or abs(current_lat - prev_lat) > 0.00001:
                    # for reverse_points in range(len(dat0) - points):
                    #     reverse_long.append(dat0[points + reverse_points][0])
                    #     reverse_lat.append(dat0[points + reverse_points][1])
                    break

                long.append(dat0[points][0])
                lat.append(dat0[points][1])
                prev_long = current_long
                prev_lat = current_lat

            gmap1.polygon(lat, long,
                          color=color_codes[weight % 9])
            break
        break

    # polygons = []
    # color_bar = []
    # same_weight_polygons = []
    # for weight in range(len(contour_map.allsegs)):
    #     color_bar.append((weight, contour_map.levels[weight]))
    #     print(f"Number of segs:{len(contour_map.allsegs[weight])}, weight = {contour_map.levels[weight]}")
    #
    #     for area in range(len(contour_map.allsegs[weight])):
    #         dat0 = contour_map.allsegs[weight][area]
    #         same_weight_polygons.append(polygon_hole_split(dat0, 0.00001))
    #     polygons.append(same_weight_polygons.copy())
    #     same_weight_polygons.clear()
    # print(color_bar)
    # print(contour_map.levels)
    # gmap1.draw("C:\\Users\\kwekz\\Desktop\\test2.html")

    plt.colorbar(contour_map)

    plt.show()


def func(x, y):
    y = round((y - 1.2847) * 1000, 1)
    x = round((x - 103.8117) * 1000, 1)
    return x * (1 - x) * np.cos(4 * np.pi * x) * np.sin(4 * np.pi * y ** 2) ** 2


def defunct(x, y):
    y = (y - 1.2847) * 1000
    x = (x - 103.8117) * 1000
    return x * (1 - x) * np.cos(4 * np.pi * x) * np.sin(4 * np.pi * y ** 2) ** 2


def function_2(x, y):
    y = (y - 1.315709) * 400
    x = (x - 104.001393) * 700
    return x * (1 - x) * np.cos(4 * np.pi * x) * np.sin(4 * np.pi * y ** 2) ** 2


def original_func(x, y):
    return x * (1 - x) * np.cos(4 * np.pi * x) * np.sin(4 * np.pi * y ** 2) ** 2


def point_dist(x1, y1, x2, y2):
    return math.sqrt((pow((x2 - x1), 2) + pow(y2 - y1, 2)))


def mid_point(coordinate_list):
    return (max(coordinate_list) + min(coordinate_list)) / 2


def generate_values():
    # latitude_sample = [1.2847, 1.2848, 1.2849, 1.285, 1.2851, 1.2852, 1.2853, 1.2854, 1.2855, 1.2856, 1.2847, 1.2848, 1.2849, 1.285, 1.2851, 1.2852, 1.2853, 1.2854, 1.2855, 1.2856, 1.2847, 1.2848, 1.2849, 1.285, 1.2851, 1.2852, 1.2853, 1.2854, 1.2855, 1.2856, 1.2847, 1.2848, 1.2849, 1.285, 1.2851, 1.2852, 1.2853, 1.2854, 1.2855, 1.2856, 1.2847, 1.2848, 1.2849, 1.285, 1.2851, 1.2852, 1.2853, 1.2854, 1.2855, 1.2856, 1.2847, 1.2848, 1.2849, 1.285, 1.2851, 1.2852, 1.2853, 1.2854, 1.2855, 1.2856, 1.2847, 1.2848, 1.2849, 1.285, 1.2851, 1.2852, 1.2853, 1.2854, 1.2855, 1.2856, 1.2847, 1.2848, 1.2849, 1.285, 1.2851, 1.2852, 1.2853, 1.2854, 1.2855, 1.2856, 1.2847, 1.2848, 1.2849, 1.285, 1.2851, 1.2852, 1.2853, 1.2854, 1.2855, 1.2856, 1.2847, 1.2848, 1.2849, 1.285, 1.2851, 1.2852, 1.2853, 1.2854, 1.2855, 1.2856]
    # longitude_sample = [103.8117, 103.8117, 103.8117, 103.8117, 103.8117, 103.8117, 103.8117, 103.8117, 103.8117, 103.8117, 103.8118, 103.8118, 103.8118, 103.8118, 103.8118, 103.8118, 103.8118, 103.8118, 103.8118, 103.8118, 103.8119, 103.8119, 103.8119, 103.8119, 103.8119, 103.8119, 103.8119, 103.8119, 103.8119, 103.8119, 103.812, 103.812, 103.812, 103.812, 103.812, 103.812, 103.812, 103.812, 103.812, 103.812, 103.8121, 103.8121, 103.8121, 103.8121, 103.8121, 103.8121, 103.8121, 103.8121, 103.8121, 103.8121, 103.8122, 103.8122, 103.8122, 103.8122, 103.8122, 103.8122, 103.8122, 103.8122, 103.8122, 103.8122, 103.8123, 103.8123, 103.8123, 103.8123, 103.8123, 103.8123, 103.8123, 103.8123, 103.8123, 103.8123, 103.8124, 103.8124, 103.8124, 103.8124, 103.8124, 103.8124, 103.8124, 103.8124, 103.8124, 103.8124, 103.8125, 103.8125, 103.8125, 103.8125, 103.8125, 103.8125, 103.8125, 103.8125, 103.8125, 103.8125, 103.8126, 103.8126, 103.8126, 103.8126, 103.8126, 103.8126, 103.8126, 103.8126, 103.8126, 103.8126]
    # weight_sample = [9.80812889029008, 9.807984177661622, 9.806559495962446, 9.806956764963843, 9.805823442144325, 9.809914022729686, 9.80968241927086, 9.80672916158248, 9.808537116524334, 9.805069858731638, 9.805784042133165, 9.806311139820245, 9.807236568231412, 9.809005620435926, 9.80626061971379, 9.808424087353403, 9.809656699105672, 9.806506584882046, 9.808049684149685, 9.807671207774785, 9.805144011983813, 9.805483497359164, 9.806074906327101, 9.80829464675826, 9.807975987236965, 9.809705068849658, 9.80834205496633, 9.808640235335215, 9.809396918983007, 9.806503433001225, 9.809193703162727, 9.807470163149294, 9.809999574566886, 9.805474169740945, 9.807523611269701, 9.80686658485638, 9.80940471235577, 9.808830288668737, 9.807113971699327, 9.80724329179546, 9.807654317175295, 9.809161340412432, 9.806603892981242, 9.809241826925241, 9.80788718748318, 9.808910223553442, 9.808122277493553, 9.80732953213465, 9.808331005597516, 9.808948210899445, 9.807395952616844, 9.807170528777254, 9.806162320750824, 9.805205546720039, 9.80861429843123, 9.806954772391748, 9.805677130980143, 9.806705827166198, 9.808470121763396, 9.807288828602529, 9.805291531160268, 9.809783445139834, 9.80861418317851, 9.807751134159018, 9.80838182355061, 9.806775661454601, 9.809104544968637, 9.807543824714326, 9.808795371888426, 9.809558052716389, 9.806593501181663, 9.807280279227063, 9.805899238131529, 9.805982539772936, 9.806844625522363, 9.808142697138528, 9.807030529843926, 9.805988053034163, 9.809004055286433, 9.807076188597893, 9.80923544884448, 9.805490351012663, 9.80942019820369, 9.805159965612928, 9.809900781684062, 9.80554187264365, 9.809269399287288, 9.80514722920465, 9.805769289865252, 9.807989537442362, 9.808199588238333, 9.808074494072416, 9.809329506152901, 9.807640469959711, 9.806581612023928, 9.80835945925168, 9.806678679376079, 9.80773218445338, 9.807810362838671, 9.808357954197117]

    latitude_sample = []
    longitude_sample = []
    values = []
    tidal_correction = []
    gravity_correction = []

    for i in range(200):
        latitude_sample.append(random.uniform(1.315709, 1.318058))
        longitude_sample.append(random.uniform(104.001393, 104.003131))

    for i in range(len(latitude_sample)):
        values.append(function_2(longitude_sample[i], latitude_sample[i]))

    for i in range(len(latitude_sample)):
        values.append(function_2(longitude_sample[i], latitude_sample[i]))

    for i in range(len(latitude_sample)):
        tidal_correction.append(random.uniform(-1, 1))

    for i in range(len(latitude_sample)):
        gravity_correction.append(random.uniform(-0.05, 0.05))


    # df = pd.read_csv(r'sample_data.csv')
    # data = []
    # data.append(latitude_sample)
    # data.append(longitude_sample)
    # data.append(values)
    # df['Latitude(deg)'] = latitude_sample
    # df['Longitude(deg)'] = longitude_sample
    # df['Values'] = values
    df = pd.DataFrame(list(zip(latitude_sample, longitude_sample, values, tidal_correction, gravity_correction)),
                      columns=['Latitude(deg)', 'Longitude(deg)', 'Values', 'Tidal Correction', 'Gravity Correction'])

    df.to_csv('data_with_correction.csv')


    # return latitude_sample, longitude_sample, values


def get_correction_values(values, tidal_correction):
    correction_array = [values.copy()]

    new_arr = []
    for i in range(len(values)):
        new_arr.append(values[i] + tidal_correction[i])
    correction_array.append(new_arr)

    print(correction_array)
    return correction_array


def gmap_output(lat_sample, long_sample, values):

    contour_map = interpolate(lat_sample, long_sample, values, levels=15, points=100, method='cubic')
    # contour_map.allsegs contain all the polygons sorted into different weights.
    # Each weight will have certain areas(polygons), and each area will have different
    # coordinates
    # Last weight in contour_map.levels is ignored (Outermost contour) as it is not plotted

    polygons = []
    color_bar = []
    same_weight_polygons = []
    for weight in range(len(contour_map.allsegs)):
        color_bar.append(contour_map.levels[weight])
        for area in range(len(contour_map.allsegs[weight])):
            dat0 = contour_map.allsegs[weight][area]
            same_weight_polygons.append(polygon_hole_split(dat0))

        polygons.append(same_weight_polygons.copy())
        same_weight_polygons.clear()

    return polygons, color_bar, mid_point(lat_sample), mid_point(long_sample)


def apply_corrections(df, values):

    tide_correction_list = df['Tidal Correction'].tolist()
    for i in range(len(values)):
        values[i] += tide_correction_list[i]


    gravity_correction_list = df['Gravity Correction'].tolist()
    for i in range(len(values)):
        values[i] += gravity_correction_list[i]


def read_csv():
    file = open("data_with_correction.csv")

    df = pd.read_csv(file)
    lat_list = df['Latitude(deg)'].tolist()
    long_list = df['Longitude(deg)'].tolist()
    values_list = df['Values'].tolist()

    apply_corrections(df, values_list)

    gmap_output(lat_list, long_list, values_list)


def step_draw():
    gmap1 = gmplot.GoogleMapPlotter(1.2847,
                                    103.8117, 21, map_type='satellite')

    gmap1.max_intensity = 0.1
    gmap1.point_radius = 1

    latitude_sample = [1.2847, 1.2848, 1.2849, 1.285, 1.2851, 1.2852, 1.2852999999999999, 1.2853999999999999,
                       1.2854999999999999, 1.2855999999999999, 1.2847, 1.2848, 1.2849, 1.285, 1.2851, 1.2852,
                       1.2852999999999999, 1.2853999999999999, 1.2854999999999999, 1.2855999999999999, 1.2847, 1.2848,
                       1.2849, 1.285, 1.2851, 1.2852, 1.2852999999999999, 1.2853999999999999, 1.2854999999999999,
                       1.2855999999999999, 1.2847, 1.2848, 1.2849, 1.285, 1.2851, 1.2852, 1.2852999999999999,
                       1.2853999999999999, 1.2854999999999999, 1.2855999999999999, 1.2847, 1.2848, 1.2849, 1.285,
                       1.2851, 1.2852, 1.2852999999999999, 1.2853999999999999, 1.2854999999999999, 1.2855999999999999,
                       1.2847, 1.2848, 1.2849, 1.285, 1.2851, 1.2852, 1.2852999999999999, 1.2853999999999999,
                       1.2854999999999999, 1.2855999999999999, 1.2847, 1.2848, 1.2849, 1.285, 1.2851, 1.2852,
                       1.2852999999999999, 1.2853999999999999, 1.2854999999999999, 1.2855999999999999, 1.2847, 1.2848,
                       1.2849, 1.285, 1.2851, 1.2852, 1.2852999999999999, 1.2853999999999999, 1.2854999999999999,
                       1.2855999999999999, 1.2847, 1.2848, 1.2849, 1.285, 1.2851, 1.2852, 1.2852999999999999,
                       1.2853999999999999, 1.2854999999999999, 1.2855999999999999, 1.2847, 1.2848, 1.2849, 1.285,
                       1.2851, 1.2852, 1.2852999999999999, 1.2853999999999999, 1.2854999999999999, 1.2855999999999999]
    longitude_sample = [103.8117, 103.8117, 103.8117, 103.8117, 103.8117, 103.8117, 103.8117, 103.8117, 103.8117,
                        103.8117, 103.8118, 103.8118, 103.8118, 103.8118, 103.8118, 103.8118, 103.8118, 103.8118,
                        103.8118, 103.8118, 103.81190000000001, 103.81190000000001, 103.81190000000001,
                        103.81190000000001, 103.81190000000001, 103.81190000000001, 103.81190000000001,
                        103.81190000000001, 103.81190000000001, 103.81190000000001, 103.812, 103.812, 103.812, 103.812,
                        103.812, 103.812, 103.812, 103.812, 103.812, 103.812, 103.8121, 103.8121, 103.8121, 103.8121,
                        103.8121, 103.8121, 103.8121, 103.8121, 103.8121, 103.8121, 103.8122, 103.8122, 103.8122,
                        103.8122, 103.8122, 103.8122, 103.8122, 103.8122, 103.8122, 103.8122, 103.81230000000001,
                        103.81230000000001, 103.81230000000001, 103.81230000000001, 103.81230000000001,
                        103.81230000000001, 103.81230000000001, 103.81230000000001, 103.81230000000001,
                        103.81230000000001, 103.8124, 103.8124, 103.8124, 103.8124, 103.8124, 103.8124, 103.8124,
                        103.8124, 103.8124, 103.8124, 103.8125, 103.8125, 103.8125, 103.8125, 103.8125, 103.8125,
                        103.8125, 103.8125, 103.8125, 103.8125, 103.8126, 103.8126, 103.8126, 103.8126, 103.8126,
                        103.8126, 103.8126, 103.8126, 103.8126, 103.8126]
    weight_sample = [9.80812889029008, 9.807984177661622, 9.806559495962446, 9.806956764963843, 9.805823442144325,
                     9.809914022729686, 9.80968241927086, 9.80672916158248, 9.808537116524334, 9.805069858731638,
                     9.805784042133165, 9.806311139820245, 9.807236568231412, 9.809005620435926, 9.80626061971379,
                     9.808424087353403, 9.809656699105672, 9.806506584882046, 9.808049684149685, 9.807671207774785,
                     9.805144011983813, 9.805483497359164, 9.806074906327101, 9.80829464675826, 9.807975987236965,
                     9.809705068849658, 9.80834205496633, 9.808640235335215, 9.809396918983007, 9.806503433001225,
                     9.809193703162727, 9.807470163149294, 9.809999574566886, 9.805474169740945, 9.807523611269701,
                     9.80686658485638, 9.80940471235577, 9.808830288668737, 9.807113971699327, 9.80724329179546,
                     9.807654317175295, 9.809161340412432, 9.806603892981242, 9.809241826925241, 9.80788718748318,
                     9.808910223553442, 9.808122277493553, 9.80732953213465, 9.808331005597516, 9.808948210899445,
                     9.807395952616844, 9.807170528777254, 9.806162320750824, 9.805205546720039, 9.80861429843123,
                     9.806954772391748, 9.805677130980143, 9.806705827166198, 9.808470121763396, 9.807288828602529,
                     9.805291531160268, 9.809783445139834, 9.80861418317851, 9.807751134159018, 9.80838182355061,
                     9.806775661454601, 9.809104544968637, 9.807543824714326, 9.808795371888426, 9.809558052716389,
                     9.806593501181663, 9.807280279227063, 9.805899238131529, 9.805982539772936, 9.806844625522363,
                     9.808142697138528, 9.807030529843926, 9.805988053034163, 9.809004055286433, 9.807076188597893,
                     9.80923544884448, 9.805490351012663, 9.80942019820369, 9.805159965612928, 9.809900781684062,
                     9.80554187264365, 9.809269399287288, 9.80514722920465, 9.805769289865252, 9.807989537442362,
                     9.808199588238333, 9.808074494072416, 9.809329506152901, 9.807640469959711, 9.806581612023928,
                     9.80835945925168, 9.806678679376079, 9.80773218445338, 9.807810362838671, 9.808357954197117]
    lat_space = np.linspace(min(latitude_sample), max(latitude_sample), 100)
    long_space = np.linspace(min(longitude_sample), max(longitude_sample), 100)

    X, Y = np.meshgrid(long_space, lat_space)

    Ti = griddata((longitude_sample, latitude_sample), weight_sample, (X, Y), method='cubic')

    plt.ylim([1.2850127465950092, 1.2855999999999999])
    plt.xlim([103.8117, 103.8126])

    contour_map = plt.contourf(X, Y, Ti)
    dat0 = contour_map.allsegs[2][6]
    lat = []
    long = []
    prev_long = dat0[0][0]
    prev_lat = dat0[0][1]

    print(len(dat0))

    # [2][6]  [3][6] [7][5]

    plt.clf()

    plt.ylim([1.2850127465950092, 1.2855999999999999])
    plt.xlim([103.8117, 103.8126])

    lat = []
    long = []
    prev_long = dat0[0][0]
    prev_lat = dat0[0][1]

    for numbers in range(7):
        for j in range(10):
            long.append(dat0[numbers * 10 + j][0])
            lat.append(dat0[numbers * 10 + j][1])

    gmap1.polygon(lat, long,
                  color=color_codes[1])
    gmap1.draw("C:\\Users\\kwekz\\Desktop\\test2.html")


def hole_plot():
    import gmplot
    apikey = ''  # (your API key here)
    gmap = gmplot.GoogleMapPlotter(24.886, -70.268, 5, apikey=apikey)

    golden_gate_park = [
        (25.774, -80.19),
        (18.466, -66.118),
        (32.321, -64.757),
    ]

    innerCoords = [
        (28.745, -70.579),
        (29.57, -67.514),
        (27.339, -66.668),
    ]
    results = zip(golden_gate_park, innerCoords)
    print(list(results))
    gmap.polygon([golden_gate_park, innerCoords], face_color='pink', edge_color='cornflowerblue', edge_width=5)
    gmap.draw("C:\\Users\\kwekz\\Desktop\\test2.html")


if __name__ == '__main__':
    # interpolation()
    # poly = gmap_output(generate_values())
    read_csv()
    # generate_values()

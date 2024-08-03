import math
import itertools

def create_distance_coordinates_list(measure_data, coordinates_dict):
    distance_coordinates_list = []
    for key, coordinates in coordinates_dict.items():
        for measure in measure_data:
            if measure[0] == key:
                distance_coordinates_list.append([measure[1], coordinates])
                break
    return distance_coordinates_list


# this function calculates a single
# (x,y) coordinates given 3 points and distances


def calculate_distance(distances_and_points):
    if len(distances_and_points) < 3:
        raise ValueError("At least three distances and points are required for trilateration.")

    # Extract distances and points
    distances = [distance for distance, _ in distances_and_points]
    points = [point for _, point in distances_and_points]

    # Calculate differences between the coordinates
    diff_x1 = points[1][0] - points[0][0]
    diff_y1 = points[1][1] - points[0][1]
    diff_x2 = points[2][0] - points[0][0]
    diff_y2 = points[2][1] - points[0][1]

    # Calculate squared distances between the points
    dist_sq1 = math.pow(distances[0], 2) - math.pow(distances[1], 2) + math.pow(points[1][0], 2) + math.pow(
        points[1][1], 2) - math.pow(points[0][0], 2) - math.pow(points[0][1], 2)
    dist_sq2 = math.pow(distances[0], 2) - math.pow(distances[2], 2) + math.pow(points[2][0], 2) + math.pow(
        points[2][1], 2) - math.pow(points[0][0], 2) - math.pow(points[0][1], 2)

    # Calculate the coordinates if denominator is not zero
    denominator = 2 * (diff_x1 * diff_y2 - diff_x2 * diff_y1)
    if denominator != 0 and diff_y2 != 0:
        x = (dist_sq1 * diff_y2 - dist_sq2 * diff_y1) / denominator
        y = (dist_sq2 - 2 * x * diff_x2) / (2 * diff_y2)
        return x, y
    else:
        return None  # Trilateration cannot be performed with collinear points


# this function gets a list of distance and corresponds coordinates
# and returns the location of the beacon during the test
def average_trilateration(distances_and_points_list):
    if len(distances_and_points_list) < 3:
        raise ValueError("At least three sets of distances and points are required.")

    # Initialize lists to store calculated coordinates
    coordinates = []

    # Iterate over all combinations of three points
    for points_combination in itertools.combinations(distances_and_points_list, 3):
        # Calculate coordinates using trilateration for the current combination
        result = calculate_distance(points_combination)
        if result is not None:
            coordinates.append(result)

    # Calculate the average coordinates
    if coordinates:
        average_x = sum(x for x, _ in coordinates) / len(coordinates)
        average_y = sum(y for _, y in coordinates) / len(coordinates)
        return average_x, average_y
    else:
        return None  # Return None if no valid coordinates were calculated

from flask import Flask, request, jsonify

app = Flask(__name__)

raw_measurements_demo = \
    [[[1, 43.8, -75], [2, 27.15, -67], [4, 35.25, -63]], [[1, 51.45, -71], [2, 26.85, -55], [3, 5.7, -61], [4, 30.75, -69]], [[1, 47.1, -69], [2, 25.65, -57], [3, 9.3, -59], [4, 23.1, -64]], [[1, 35.85, -72], [2, 22.95, -56], [3, 11.55, -64], [4, 21.15, -61]], [[1, 35.25, -69], [2, 24.15, -51], [3, 17.1, -73], [4, 32.4, -77]], [[1, 36.75, -63], [2, 11.1, -54], [3, 21.3, -68], [4, 24.0, -66]], [[1, 30.6, -72], [2, 10.8, -51], [3, 25.2, -68], [4, 13.5, -63]], [[1, 42.0, -64], [2, 22.95, -60], [3, 22.5, -66], [4, 12.6, -57]], [[1, 47.25, -71], [2, 16.95, -64], [3, 12.15, -66], [4, 12.75, -54]], [[1, 40.95, -73], [3, 19.5, -76], [4, 15.0, -50]], [[1, 31.95, -79], [2, 27.3, -62], [3, 24.6, -71], [4, 9.9, -49]], [[2, 26.1, -59], [3, 20.55, -73], [4, 15.0, -56]], [[2, 27.6, -73], [3, 13.65, -82], [4, 12.75, -57]], [[1, 41.55, -73], [3, 11.85, -68], [4, 15.6, -57]], [[2, 22.5, -60], [3, 9.75, -59], [4, 14.85, -58]], [[2, 22.65, -61], [3, 13.8, -65], [4, 17.85, -58]], [[1, 45.75, -75], [2, 11.4, -54], [3, 25.8, -70], [4, 12.75, -53]], [[1, 42.6, -75], [2, 15.3, -61], [3, 19.5, -72], [4, 11.25, -57]], [[1, 35.85, -76], [2, 25.8, -66], [3, 15.45, -74], [4, 16.5, -59]], [[1, 28.5, -71], [2, 20.1, -64], [3, 19.95, -69], [4, 10.2, -53]], [[1, 33.3, -73], [2, 24.3, -63], [4, 8.85, -52]], [[4, 12.3, -47]], [[1, 43.8, -86], [2, 29.7, -70], [3, 24.9, -77], [4, 8.7, -43]], [[2, 21.6, -64], [3, 24.75, -73], [4, 7.2, -46]], [[1, 29.4, -69], [2, 7.5, -46], [3, 31.5, -75], [4, 23.4, -61]], [[1, 42.45, -70], [2, 11.4, -49], [4, 23.85, -63]], [[1, 27.0, -65], [2, 12.0, -48], [3, 29.25, -73], [4, 15.6, -58]], [[1, 30.75, -68], [2, 21.3, -52], [3, 45.9, -78], [4, 19.65, -71]], [[1, 36.3, -64], [2, 25.8, -64], [3, 47.85, -80], [4, 18.45, -64]], [[1, 27.0, -64], [2, 22.5, -61], [3, 47.25, -83], [4, 16.5, -65]], [[1, 28.5, -64], [2, 35.85, -74], [3, 46.8, -82], [4, 28.2, -71]], [[1, 22.2, -55], [2, 25.8, -58], [3, 47.25, -78], [4, 26.55, -72]], [[1, 19.5, -65], [2, 35.25, -66], [3, 49.5, -76], [4, 35.55, -72]], [[1, 13.8, -71], [2, 33.45, -68], [3, 44.25, -80], [4, 34.65, -71]], [[1, 18.15, -56], [2, 25.65, -61], [3, 44.55, -84], [4, 44.25, -75]], [[1, 24.15, -61], [2, 25.5, -63], [3, 37.5, -82], [4, 26.7, -76]], [[1, 20.7, -71], [2, 32.1, -77], [3, 29.7, -87], [4, 24.15, -80]], [[1, 32.85, -77], [2, 23.1, -73], [3, 25.5, -78], [4, 20.25, -69]], [[1, 28.5, -73], [2, 11.85, -62], [3, 25.8, -76], [4, 17.7, -65]], [[1, 36.15, -80], [2, 15.15, -60], [3, 30.75, -85], [4, 19.5, -70]], [[1, 34.95, -80], [2, 4.65, -60], [3, 25.95, -81], [4, 19.65, -80]], [[1, 36.9, -77], [2, 2.55, -51], [3, 28.5, -79], [4, 16.8, -71]], [[1, 35.55, -75], [2, 7.5, -58], [3, 17.4, -87], [4, 20.85, -69]], [[2, 14.7, -64], [3, 22.95, -71], [4, 26.7, -77]], [[1, 34.2, -80], [2, 17.85, -64], [3, 11.7, -71], [4, 22.95, -80]], [[1, 43.35, -85], [2, 16.5, -62], [3, 17.25, -77], [4, 27.3, -75]], [[1, 40.2, -81], [2, 25.5, -65], [3, 12.0, -67], [4, 31.35, -82]], [[1, 46.5, -85], [2, 26.55, -71], [3, 17.1, -68], [4, 34.5, -83]], [[1, 35.25, -81], [2, 29.7, -78], [3, 22.35, -82], [4, 24.15, -82]], [[1, 33.6, -75], [2, 25.65, -67], [4, 39.15, -76]], [[1, 33.15, -79], [2, 15.3, -67], [3, 33.3, -80], [4, 29.55, -75]], [[1, 33.3, -76], [2, 19.2, -60], [3, 22.95, -78], [4, 25.5, -75]], [[1, 41.4, -77], [2, 8.85, -59], [4, 25.5, -69]], [[1, 34.5, -79], [2, 7.95, -60], [3, 35.7, -90], [4, 29.85, -76]], [[1, 31.5, -75], [2, 2.85, -55], [3, 36.45, -85], [4, 28.8, -75]], [[1, 19.35, -79], [2, 6.15, -59], [3, 37.35, -90], [4, 28.2, -85]], [[1, 19.2, -68], [2, 15.75, -65], [4, 30.6, -78]], [[1, 18.75, -74], [2, 13.2, -62], [3, 35.7, -94]], [[1, 26.55, -68], [2, 17.55, -62], [3, 33.9, -86], [4, 36.9, -69]], [[1, 18.3, -62], [2, 17.1, -68], [3, 38.85, -86], [4, 33.6, -74]], [[1, 22.8, -72], [2, 25.5, -62], [3, 35.85, -89], [4, 31.8, -73]], [[1, 15.3, -64]], [[1, 10.65, -54], [2, 26.7, -77], [3, 36.6, -88], [4, 36.9, -76]], [[1, 28.5, -73], [2, 34.5, -70], [3, 40.65, -81], [4, 40.2, -87]], [[1, 34.35, -77], [2, 30.3, -69], [3, 22.5, -70], [4, 1.5, -26]]]
# the measurements received with the mac addresses
raw_measurements = []
measurements_xy_array = []  # the location of each measurement which matches the index in the list
processed_measurement = []  # measurements with the locations of the agent ready for k-means algorithm
measurements_distance_array = []
data_for_k_means = []
beacon_colors = {}
map_size = (0, 0)
measurements = []
id_measurements = []
measurement_counter = 0
beacon_locations = {
    1: (7, 1),
    2: (11, 13),
    3: (19, 23),
    4: (11, 21)
}
beacons_mac_id_dict = {
    '80:65:99:c7:9d:e5': 1,
    '80:65:99:c8:5c:51': 2,
    '80:65:99:c8:5c:a9': 3,
    '80:65:99:c7:a9:99': 4,

}
optimal_locations = []
optimal_locations_to_send = [{'x': 11, 'y': 13}]

@app.route("/")
def hello_world():
    return "<p>Hello World!</p>"

@app.route("/health")
def health():
    return "<p>everythings Great!</p>"

# New route to handle the Done function

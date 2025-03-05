import geomdl
from geomdl import fitting
from geomdl import utilities
import numpy as np
from scipy.integrate import quad
import os


def coordinate_extractor(file_path):
    """
    Reads airfoil data from a .dat file and returns coordinates as a list of tuples.
    """
    with open(file_path,'r') as file:
        lines = file.readlines()

    coordinates = []
    for line in lines[1:]:  # Skip the first line (header)
        parts = line.split()
        if len(parts) == 2:  # Ensure that each line has exactly two values
            x, y = map(float, parts)
            coordinates.append((x, y))

    return coordinates


def scale_coordinates(coordinates, chord_length):
    """
    Scales the airfoil coordinates based on the provided chord length.
    """
    max_x = max(coord[0] for coord in coordinates)
    scale_factor = chord_length / max_x
    scaled_coordinates = [(x * scale_factor, y * scale_factor) for x, y in coordinates]
    return scaled_coordinates


def calculate_curve_derivatives(curve, t):
    """
    Evaluates the first derivatives of the curve at parameter t.
    """
    derivatives = curve.derivatives(t, order=1)
    dx_dt, dy_dt = derivatives[1][0], derivatives[1][1]
    return dx_dt, dy_dt


def simpsons_rule(f, a, b, n=1000):
    """
    Approximate the integral of f from a to b using Simpson's rule with n intervals.
    """
    h = (b - a) / n
    result = f(a) + f(b)

    for i in range(1, n, 2):
        result += 4 * f(a + i * h)

    for i in range(2, n - 1, 2):
        result += 2 * f(a + i * h)

    result *= h / 3
    return result

def calculate_exact_perimeter(control_points, flag):
    """
    Computes the exact perimeter of the curve using numerical integration.
    The flag parameter determines the integration range:
    - flag == 1: Integrate over the full curve (0 to 1).
    - flag != 1: Integrate up to 0.15 times the parameter range (0 to 0.15).
    """
    # Interpolate the control points into a NURBS curve
    curve = fitting.interpolate_curve(control_points, degree=3)

    def integrand(t):
        dx_dt, dy_dt = calculate_curve_derivatives(curve, t)
        return np.sqrt(dx_dt**2 + dy_dt**2)
    
    # Decide the integration range based on the flag
    t_end = 1 if flag == 1 else 0.15

    try:
        perimeter, _ = quad(integrand, 0.0, t_end, limit=200)  # Integration
    except Exception as e:
        print(f"Warning using quad: {e}. Trying Simpson's rule instead.")
        perimeter = simpsons_rule(integrand, 0.0, t_end, n=1000)

    return abs(perimeter)



def calculate_area(control_points, degree=3):
    """
    Fits a NURBS curve to airfoil control points and calculates the enclosed area.
    """
    curve = fitting.interpolate_curve(control_points, degree)
    curve.delta = 0.001  # finer delta for high precision

    curve_points = np.array(curve.evalpts)
    x, y = curve_points[:, 0], curve_points[:, 1]

    if np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)) < 0:
        x = np.flip(x)
        y = np.flip(y)

    area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
    return abs(area)


def calculate_sum_distance_perimeter(control_points):
    """
    Computes the perimeter by summing distances between consecutive points.
    """
    perimeter = 0
    for i in range(len(control_points) - 1):
        x1, y1 = control_points[i]
        x2, y2 = control_points[i + 1]
        perimeter += np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    return perimeter


def calculate_rectangle_area(control_points):
    """
    Approximates the area as a rectangle using chord length and maximum thickness.
    """
    chord_length = max(pt[0] for pt in control_points) - min(pt[0] for pt in control_points)
    max_thickness = max(pt[1] for pt in control_points) - min(pt[1] for pt in control_points)
    return chord_length * max_thickness


def checker(control_points, chord_length):
    """
    Compares perimeter and area values obtained through integration with alternative methods.
    """
    scaled_points = scale_coordinates(control_points, chord_length)
    curve = fitting.interpolate_curve(scaled_points, degree=3)
    perimeter_integration = calculate_exact_perimeter(curve)
    perimeter_sum = calculate_sum_distance_perimeter(scaled_points)

    area_integration = calculate_area(scaled_points)
    area_rectangle = calculate_rectangle_area(scaled_points)

    print("Comparison Results:")
    print(f"Perimeter (Integration): {perimeter_integration:.6f} meters")
    print(f"Perimeter (Sum of distances): {perimeter_sum:.6f} meters")
    print(f"Area (Integration): {area_integration:.6f} square meters")
    print(f"Area (Rectangle approximation): {area_rectangle:.6f} square meters")

    return area_integration, perimeter_integration


def main():
    """
    Main execution function to run as a script.
    """
    file_path = input("Enter the path to the .dat file: ").strip()                
    if not os.path.exists(file_path):
        print("File does not exist. Please provide a valid file path.")
        return

    try:
        chord_length = float(input("Enter the chord length in meters: "))
    except ValueError:
        print("Invalid input for chord length. Please provide a numeric value.")
        return

    control_points = coordinate_extractor(file_path)
    scaled_points = scale_coordinates(control_points, chord_length)

    area_integration, perimeter_integration = checker(control_points, chord_length)

    print("\nResults:")
    print(f"Area of the fitted airfoil: {area_integration:.6f} square meters")
    print(f"Perimeter (Arc Length) of the fitted airfoil: {perimeter_integration:.6f} meters")
    

# Make this script usable as a module or standalone
if __name__ == "__main__":
    main()
else:
    def airfoil_geometry(file_path, chord_length):
        """
        Function to return area and perimeter when used as a module.
        """
        control_points = coordinate_extractor(file_path)
        scaled_points = scale_coordinates(control_points, chord_length)
        curve = fitting.interpolate_curve(scaled_points, degree=3)
        area_integration = calculate_area(scaled_points)
        perimeter_integration = calculate_exact_perimeter(curve)
        return area_integration, perimeter_integration

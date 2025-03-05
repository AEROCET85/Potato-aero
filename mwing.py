import airfoil_geometry as ag
import numpy as np

K = 0.41895951  # Centroid scaling coefficient

def calculate_mwing(b, aspect_ratio, v, g, Cl, p, pd, rib_spacing, l=0.8): #L IS LAMDA
    """
    Calculates the weight and center of mass of the wing.

    Returns:
    - Ww: Wing weight (kg)
    - L_kg: Lift in kg
    - s: Wing area (m²)
    - tw: Tip thickness (m)
    - Cgw: Wing center of gravity
    """
    sum_area = 0  # Initialize inside function
    sum_area_moment = 0  # Initialize inside function

    s = (b ** 2) / aspect_ratio  # Wing area (m²)
    cr = (2 * s) / (b * (1 + l))
    cw = l * cr
    tr = 0.1257 * cr  # 0.1257 IS THE MAX THICKNESS OF THE SELECTED AIRFOIL
    tw = l * tr
    if tw <= 0.02:  # Minimum thickness check
        return None
    cm = (2 / 3) * cr * ((1 + l + l ** 2) / (1 + l))
    Wr = 0
    L = 0.5 * p * v ** 2 * Cl * s  # Lift force in Newtons (N)
    L_kg = L / g  # Convert lift to kg

    # Airfoil calculations
    coordinates = ag.coordinate_extractor(
        r"C:\Users\adith\Desktop\neeraj ettan\AeroCET D2 SDG + NACA 4415.dat"
    )
    root_coordinates = ag.scale_coordinates(coordinates, cr)
    tip_coordinates = ag.scale_coordinates(coordinates, cw)

    carea = ag.calculate_area(root_coordinates)
    carear = carea

    for i in np.arange(0, b / 2 + 0.05, rib_spacing):
        c = cr - ((cr - cw) * (i / (b / 2)))
        carea = carear * (c ** 2) / (cr ** 2)
        Wc = carea * pd
        sum_area += carea
        sum_area_moment += carea * K * c
        
        Wr += 2 * Wc

    if sum_area == 0:
        return None  # Prevent division by zero error

    Cgw = sum_area_moment / sum_area  # Center of gravity of the wing

    root_perimeter = ag.calculate_exact_perimeter(root_coordinates, 1)
    tip_perimeter = ag.calculate_exact_perimeter(tip_coordinates, 1)

    Wm = (root_perimeter + tip_perimeter) * (b / 2) * 0.06909
    Ws = 3 * b * 0.0128
    skn_perimeter1 = ag.calculate_exact_perimeter(tip_coordinates, 0)
    skn_perimeter2 = ag.calculate_exact_perimeter(root_coordinates, 0)
    Wsk = (
        ((2 * skn_perimeter1) + (2 * skn_perimeter2)) * (b / 2) * 150 * 0.002 +
        ((cw / 4) + (cr * (1 - 0.75 * l))) * (b / 2) * pd
    )

    Ww = Wr + Wm + Ws + Wsk + 0.030  # Final wing weight
    aerodynamic_centre = (cm / 4)
    return Ww, L_kg, s, tw, Cgw,aerodynamic_centre, cr , cm

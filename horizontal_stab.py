import airfoil_geometry as ag
import numpy as np

def calculate_horizontal_stab(aspect_ratio, s, pd, hrib_spacing, l=0.7):
    bh = (aspect_ratio * 0.25 * s) ** 0.5
    ch = bh / aspect_ratio
    sh = (bh ** 2) / aspect_ratio

    crh = (2 * sh) / (bh * (1 + l))
    cwh = l * crh

    coordinates = ag.coordinate_extractor(r"C:\Users\adith\Desktop\neeraj ettan\naca 0015.dat")
    root_coordinates = ag.scale_coordinates(coordinates, crh)
    tip_coordinates = ag.scale_coordinates(coordinates, cwh)

    Whr = 0
    carea = ag.calculate_area(root_coordinates)
    carear = carea

    for i in np.arange(0, bh / 2 + 0.03, hrib_spacing):
        c = crh - (crh - cwh) * (i / (bh / 2))
        Wch = carea * pd
        carea = carear * (c ** 2) / (crh ** 2)
        Whr += 2 * Wch

    Whs = 2 * bh * 0.01285
    Whm = (
        (ag.calculate_exact_perimeter(root_coordinates, 1) +
         ag.calculate_exact_perimeter(tip_coordinates, 1)) * (bh / 2) * 0.06909
    )
    Whsk = (
        (ag.calculate_exact_perimeter(root_coordinates, 0) +
         ag.calculate_exact_perimeter(tip_coordinates, 0)) * (bh / 2) * 150 * 0.002
    )
    Wh = Whr + Whs + Whm + Whsk + 0.01
    return Wh

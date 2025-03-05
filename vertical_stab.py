import airfoil_geometry as ag
import numpy as np

def calculate_vertical_stab(aspect_ratio, s, pd, vrib_spacing, l=0.6):
    bv = (aspect_ratio * 0.10 * s) ** 0.5
    cv = bv / aspect_ratio
    sv = (bv ** 2) / aspect_ratio

    crv = (2 * sv) / (bv * (1 + l))
    cwv = l * crv

    coordinates = ag.coordinate_extractor(r"C:\Users\adith\Desktop\neeraj ettan\naca 0015.dat")
    root_coordinates = ag.scale_coordinates(coordinates, crv)
    tip_coordinates = ag.scale_coordinates(coordinates, cwv)

    Wvr = 0
    carea = ag.calculate_area(root_coordinates)
    carear = carea

    for i in np.arange(0, bv + 0.015, vrib_spacing):
        c = crv - (crv - cwv) * (i / bv)
        Wcv = carea * pd
        carea = carear * (c ** 2) / (crv ** 2)
        Wvr += Wcv

    Wvm = (
        (ag.calculate_exact_perimeter(root_coordinates, 1) +
         ag.calculate_exact_perimeter(tip_coordinates, 1)) * (bv / 2) * 0.06909
    )
    Wvsk = (
        (ag.calculate_exact_perimeter(root_coordinates, 0) +
         ag.calculate_exact_perimeter(tip_coordinates, 0)) * (bv / 2) * 150 * 0.002
    )
    Wv = Wvr + Wvm + Wvsk + 0.01
    return Wv

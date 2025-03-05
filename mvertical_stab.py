import airfoil_geometry as ag
import numpy as np


def calculate_mvertical_stab(aspect_ratio_vstab, s, pd, vrib_spacing, l=0.6):
    sum_area = 0
    sum_area_moment = 0
    K = 0.42090292

    bv = (aspect_ratio_vstab * 0.10 * s) ** 0.5
    cv = bv / aspect_ratio_vstab
    sv = (bv ** 2) /aspect_ratio_vstab 

    crv = (2 * sv) / (bv * (1 + l))
    cwv = l * crv

    Wvr = 0
    carea = ag.calculate_area(ag.scale_coordinates(ag.coordinate_extractor(r"C:\Users\adith\Desktop\neeraj ettan\naca 0015.dat"), crv))
    carear = carea

    for i in np.arange(0, bv + 0.015, vrib_spacing):
        c = crv - (crv - cwv) * (i / bv)
        Wcv = carea * pd
        carea = carear * (c ** 2) / (crv ** 2)
        Wvr += Wcv
        sum_area += carea
        sum_area_moment += K * carea * c
        
    Cgv = sum_area_moment / sum_area
    Wv = Wvr + 0.01
    return Wv, Cgv, sv, crv, cwv

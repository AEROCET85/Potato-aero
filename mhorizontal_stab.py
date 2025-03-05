import airfoil_geometry as ag
import numpy as np

sum_area = 0
sum_area_moment = 0
K = 0.42090292

def calculate_mhorizontal_stab(aspect_ratio_hstab, s, pd, hrib_spacing, l=0.7):
    sum_area = 0
    sum_area_moment = 0
    K = 0.42090292
    bh = (aspect_ratio_hstab * 0.25 * s) ** 0.5
    ch = bh / aspect_ratio_hstab
    sh = (bh ** 2) / aspect_ratio_hstab

    crh = (2 * sh) / (bh * (1 + l))
    cwh = l * crh

    Whr = 0
    carea = ag.calculate_area(ag.scale_coordinates(ag.coordinate_extractor(r"C:\Users\adith\Desktop\neeraj ettan\naca 0015.dat"), crh))
    carear = carea

    for i in np.arange(0, bh / 2 + 0.03, hrib_spacing):
        c = crh - (crh - cwh) * (i / (bh / 2))
        Wch = carea * pd
        carea = carear * (c ** 2) / (crh ** 2)
        sum_area += carea
        sum_area_moment += K * carea * c
        
        Whr += 2 * Wch

    Cgh = sum_area_moment / sum_area
    Wh = Whr + 2 * bh * 0.01285 + 0.01
    return Wh, Cgh, sh, crh, cwh

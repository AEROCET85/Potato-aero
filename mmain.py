# mmain.py
import numpy as np
import matplotlib.pyplot as plt
from wing import calculate_wing
from fuselage import calculate_fuselage
from horizontal_stab import calculate_horizontal_stab
from vertical_stab import calculate_vertical_stab
from moment import momenty_plane

def run_mmain():
    # ----- Define constants -----
    aspect_ratio = 6
    aspect_ratio_hstab = 3
    aspect_ratio_vstab = 1.5
    v = 10  # Airspeed (m/s)
    g = 9.81  # Gravity (m/s²)
    Cl = 0.72  # Lift coefficient
    p = 1.225  # Air density (kg/m³)
    pd = 225  # Material density (kg/m³)
    rib_spacing = 0.05
    hrib_spacing = 0.03
    vrib_spacing = 0.015
    fuselage_width = 0.08
    fuselage_height = 0.065
    carbon_fraction = 0.5

    b_values = np.arange(1.0, 2.1, 0.05)
    cg_diff_values = []
    valid_b_values = []

    # ----- Iterate over wingspan -----
    for b in b_values:
        fuselage_length = b * 0.75
        wing_data = calculate_wing(b, aspect_ratio, v, g, Cl, p, pd, rib_spacing)
        if wing_data is None:
            continue
        Ww, L_kg, s, tw, Cgw, aerodynamic_centre, cr, cm = wing_data
        Wf, Cgf = calculate_fuselage(b, pd, fuselage_width, fuselage_height, carbon_fraction)
        Wh, Cgh, sh = calculate_horizontal_stab(aspect_ratio_hstab, s, pd, hrib_spacing)
        Wv, Cgv = calculate_vertical_stab(aspect_ratio_vstab, s, pd, vrib_spacing)

        center_of_mass, wing_position, Lt = momenty_plane(b, Cgw, Ww, Cgf, Wf, Cgh, Wh, Cgv, Wv, s, sh, cm)

        aerodynamic_center = wing_position + 0.081
        cg_diff = aerodynamic_center - center_of_mass

        cg_diff_values.append(cg_diff)
        valid_b_values.append(b)

        print(f"Wingspan: {b:.2f} m | Center of Mass: {center_of_mass:.4f} m | Fuselage Length: {fuselage_length:.4f} m | Aerodynamic Center: {aerodynamic_center:.4f} m | Lt: {Lt:.4f}")
        print(f"s: {s} | sh: {sh} | cm: {cm}\n")

    # ----- Plotting -----
    plt.figure(figsize=(10, 6))
    plt.plot(valid_b_values, cg_diff_values, marker='o', linestyle='-', color='b', label='Aerodynamic Center - Center of Mass')
    plt.axhline(0, color='r', linestyle='--', label='Neutral Stability Line')
    plt.xlabel('Wingspan (m)')
    plt.ylabel('(Aerodynamic Center - Center of Mass) (m)')
    plt.title('CG Difference vs Wingspan')
    plt.legend()
    plt.grid(True)
    plt.show()

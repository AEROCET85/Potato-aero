from wing import calculate_wing
from fuselage import calculate_fuselage
from horizontal_stab import calculate_horizontal_stab
from vertical_stab import calculate_vertical_stab
import numpy as np
import matplotlib.pyplot as plt
from mwing import calculate_mwing
from mfuselage import calculate_mfuselage
from mhorizontal_stab import calculate_mhorizontal_stab
from mvertical_stab import calculate_mvertical_stab
from mpayload import calculate_mpayload
from mmoment import momenty_mplane
def main():
    # Constants
    v = 13 # Velocity (m/s)
    g = 9.81  # Gravitational acceleration (m/s^2)
    t = 0.004  # Balsa thickness (m)
    pd = 270 * t  # Weight of balsa per square meter (kg/m^2)
    p = 1.225  # Air density (kg/m^3)
    Cl = 0.79  # Lift coefficient (dimensionless)
    aspect_ratio = 6  # Wing aspect ratio
    aspect_ratio_hstab = 3
    aspect_ratio_vstab = 1.5
    rib_spacing = 0.05  # Rib spacing (m)
    fuselage_height = 0.06  # Fuselage height (m)
    fuselage_width = 0.10  # Fuselage width (m)
    carbon_fraction = 0.6  # Fraction of fuselage made of carbon fiber
    hrib_spacing = 0.03  # Horizontal stabilizer rib spacing (m)
    vrib_spacing = 0.015  # Vertical stabilizer rib spacing (m)
    We = 0.490  # Weight of electronic components (kg)
    TWR = 0.8  # Thrust-to-weight ratio
    T = 2  # Thrust of the selected motor

    max_payload_fraction = 0
    optimal_wingspan = 0
    optimal_total_weight = 0

    wingspans = []
    payload_fractions_lift = []
    payload_fractions_thrust = []

    
    b_values = np.arange(1.0, 2.1, 0.05)
    cg_diff_values = []
    valid_b_values = []

    intersection_found = False
    refined_intersection = None

    for b in np.arange(0.5, 2, 0.01):  # Refined Wingspan range for higher resolution
        wing_result = calculate_wing(b, aspect_ratio, v, g, Cl, p, pd, rib_spacing)
        if not wing_result:
            continue

        Ww, L_kg, s, tw, cw, l = wing_result
        Wf = calculate_fuselage(b, pd, fuselage_width, fuselage_height, carbon_fraction)
        Wh = calculate_horizontal_stab(3, s, pd, hrib_spacing)
        Wv = calculate_vertical_stab(1.5, s, pd, vrib_spacing)
        bh = (aspect_ratio_hstab * 0.25 * s) ** 0.5
        ch = bh / aspect_ratio_hstab

        # Total weight calculations
        Wt = Ww + Wf + Wh + Wv + We
        if Wt > 1.5:
            print(f"Weight has exceeded 1.5 kg. Current weight: {Wt:.2f} kg. Stopping the loop.")
            break
        Wp = max(L_kg - Wt, 0)
        pf = Wp / L_kg if Wp > 0 else 0
        W_twr = T / TWR  # Thrust-based maximum weight
        W_t_p = max(W_twr - Wt, 0)  # Thrust-based payload weight
        p_t_f = W_t_p / W_twr if W_t_p > 0 else 0

        wingspans.append(b)
        payload_fractions_lift.append(pf)
        payload_fractions_thrust.append(p_t_f)

        if not intersection_found and abs(pf - p_t_f) < 1e-4:
            intersection_found = True
            refined_intersection = {
                "wingspan": b,
                "lift_payload_fraction": pf,
                "thrust_payload_fraction": p_t_f,
                "lift_weight": L_kg,
                "twr_weight": W_twr,
                "wing_area": s,
                "total_weight": Wt
            }



            
        wing_data = calculate_mwing(b, aspect_ratio, v, g, Cl, p, pd, rib_spacing)
        if wing_data is None:
            continue
        Ww, L_kg, s, tw, Cgw, aerodynamic_centre, cr, cm = wing_data
        Wf, Cgf,cg_falone, Wfs = calculate_mfuselage(b, pd, fuselage_width, fuselage_height, carbon_fraction,W_t_p)
        Wh, Cgh, sh, crh, cwh = calculate_mhorizontal_stab(aspect_ratio_hstab, s, pd, hrib_spacing)
        Wv, Cgv, sv, crv, cwv = calculate_mvertical_stab(aspect_ratio_vstab, s, pd, vrib_spacing)
        center_of_mass, wing_position, Lt = momenty_mplane(b, Cgw, Ww, Cgf, Wf, Cgh, Wh, Cgv, Wv, s, sh, cm, W_t_p,fuselage_width,fuselage_height)

        aerodynamic_center = wing_position 
        cg_diff = aerodynamic_center - center_of_mass

        cg_diff_values.append(cg_diff)
        valid_b_values.append(b)    

        print(f"Wingspan: {b:.3f} m, Empty Weight: {Wt:.4f} kg, "
              f"Total Weight: {Wt + Wp:.4f} kg, Payload Weight: {Wp:.4f} kg, "
              f"Payload Fraction: {pf:.4f}, Wing Area: {s:.4f} m², Tip Thickness: {tw:.4f} m")
        print(f"Wingspan: {b:.2f} m | Fuselage Length: {0.75 * b:.4f} m | Center of Mass: {center_of_mass:.4f} m| Aerodynamic Center: {aerodynamic_center:.4f} m |cg difference: {cg_diff} m | Lt: {Lt:.4f}")
        print(f"s: {s} | sh: {sh} | cm: {cm} | cr: {cr} | ct: {cw}| lambda: {l} | tw: {tw}  ")
        print('')
        print(f" f_weight: {Wf:.4f} m| wing weight: {Ww:.4f} m| tail weight: {Wh + Wv:.4f} ")
        print(f" b_h: {(aspect_ratio_hstab * 0.25 * s) ** 0.5} m| , crh: {crh:.4f} m| cwh: {cwh:.4f}    " )
        print(f" v_h: {(aspect_ratio_vstab * 0.10 * s)** 0.5} m| , crv: {crv:.4f} m| cwv: {cwv:.4f}   " )
        print('')
        print('wh',Wh,' ','Wv',Wv)
        print(f" wing position:{(0.75 * b ) - (Lt )}")
        print(f" fuselage weight: { Wf:.4f}    , fuselage cg : {Cgf:.4f}")
        print('Wfs', Wfs,"         ","cg of fus alone", cg_falone)
        print('cgw = ',0.75*b-Lt + 0.081)
        print('')
        print('')
        print('')
        print('')

        #if cg_diff > 0.03:
         #   print('cg_diff is greater than 1.5cm')
          #  break
         
        if pf > max_payload_fraction:
            max_payload_fraction = pf
            optimal_wingspan = b
            optimal_total_weight = Wt

    print(f"\nOptimal Wingspan (Lift-Based): {optimal_wingspan:.3f} m")
    print(f"Maximum Payload Fraction (Lift-Based): {max_payload_fraction:.4f}")
    print(f"Total Weight at Maximum Payload Fraction: {optimal_total_weight:.4f} kg")

    if refined_intersection:
        print(f"\nIntersection Found at Wingspan: {refined_intersection['wingspan']:.3f} m")
        print(f"Lift-Based Payload Fraction: {refined_intersection['lift_payload_fraction']:.4f}, "
              f"Thrust-Based Payload Fraction: {refined_intersection['thrust_payload_fraction']:.4f}")
        print(f"Wing Area: {refined_intersection['wing_area']:.4f} m²")
        print(f"Lift Weight at Intersection: {refined_intersection['lift_weight']:.4f} kg")
        print(f"Weight due to TWR at Intersection: {refined_intersection['twr_weight']:.4f} kg")
        print(f"Total Weight at Intersection: {refined_intersection['total_weight']:.4f} kg")
        



    plt.figure(figsize=(10, 6))
    plt.plot(wingspans, payload_fractions_lift, label="Lift-Based Payload Fraction")
    plt.plot(wingspans, payload_fractions_thrust, label="Thrust-Based Payload Fraction")
    plt.xlabel("Wingspan (m)")
    plt.ylabel("Payload Fraction")
    plt.title("Payload Fraction vs Wingspan")
    plt.legend()
    plt.grid()
    plt.show()

    
    plt.figure(figsize=(10, 6))
    plt.plot(valid_b_values, cg_diff_values, marker='o', linestyle='-', color='b', label='Aerodynamic Center - Center of Mass')
    plt.axhline(0, color='r', linestyle='--', label='Neutral Stability Line')
    plt.xlabel('Wingspan (m)')
    plt.ylabel('(Aerodynamic Center - Center of Mass) (m)')
    plt.title('CG Difference vs Wingspan')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()


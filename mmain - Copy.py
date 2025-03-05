import numpy as np
import matplotlib.pyplot as plt  # Importing matplotlib for plotting
from wing import calculate_wing
from fuselage import calculate_fuselage
from horizontal_stab import calculate_horizontal_stab
from vertical_stab import calculate_vertical_stab
from moment import momenty_plane
'''
def momenty_plane(b, Cgw, Ww, Cgf, Wf, Cgh, Wh, Cgv, Wv, s, sh, cr):
    """
    Calculates the center of mass of the plane with respect to the motor shaft tip.

    Returns:
    center_of_mass : Center of mass of the plane (m)
    """
    Len = b * 0.75  # Approximate fuselage length
    V = 0.5  # horizontal tail volume coefficient (adjustable)
    Lt = V * (s / sh) * cr  # Tail arm length

    # Sum of moments about the motor shaft tip
    sum_of_moments = ((Len - Lt) * Ww) + (Cgf * Wf) + ((Len) * Wh) + ((Len) * Wv) #CHANGE MADE ON 8/2 ON THE LENGTH OF CGH AND CGV

    # Total mass of the plane
    sum_mass = Ww + Wf + Wh + Wv

    # Center of mass location
    center_of_mass = sum_of_moments / sum_mass

    return center_of_mass'''

# ----- Define constants -----
aspect_ratio = 6 # Wing aspect ratio
aspect_ratio_hstab = 3 #horizontal stabiliser aspect ratio
aspect_ratio_vstab = 1.5 #vertical stabiliser aspect ratio
v = 10  # Airspeed (m/s)
g = 9.81  # Gravity (m/s²)
Cl = 0.72  # Lift coefficient
p = 1.225  # Air density (kg/m³)
pd = 225  # Material density (kg/m³)
rib_spacing = 0.05  # Wing rib spacing (m)
hrib_spacing = 0.03  # Horizontal stab rib spacing (m)
vrib_spacing = 0.015  # Vertical stab rib spacing (m)
fuselage_width = 0.08 # Fuselage width (m)
fuselage_height = 0.065  # Fuselage height (m)
carbon_fraction = 0.5  # Fraction of carbon fiber material


b_values = np.arange(1.0, 2.1, 0.05)
cg_diff_values = []  # To store (aerodynamic_center - center_of_mass)
valid_b_values = []  # To store corresponding b values for valid data points

# ----- Iterate over wingspan (b) -----
b_values = np.arange(1.0, 2.1, 0.05)  # Example: b from 1.0m to 2.0m in steps of 0.1m

for b in b_values:
    fuselage_length = b * 0.75
    # Wing parameters
    wing_data = calculate_wing(b, aspect_ratio, v, g, Cl, p, pd, rib_spacing)
    if wing_data is None:
        continue  # Skip if wing thickness is too low
    Ww, L_kg, s, tw, Cgw,aerodynamic_centre, cr, cm = wing_data

    # Fuselage parameters
    Wf, Cgf = calculate_fuselage(b, pd, fuselage_width, fuselage_height, carbon_fraction)

    # Horizontal stabilizer parameters
    Wh, Cgh, sh = calculate_horizontal_stab(aspect_ratio_hstab, s, pd, hrib_spacing)

    # Vertical stabilizer parameters
    Wv, Cgv = calculate_vertical_stab(aspect_ratio_vstab, s, pd, vrib_spacing)

    # Calculate center of mass
    center_of_mass, wing_position, Lt = momenty_plane(b, Cgw, Ww, Cgf, Wf, Cgh, Wh, Cgv, Wv, s, sh, cm)
    if center_of_mass < wing_position + 0.081:
        print('cg infront of ac')
        #print('the value of b is',b,'value of cg is',center_of_mass,'value of ac is',wing_position + 0.081) 
        
    aerodynamic_center = wing_position + 0.081
    cg_diff = aerodynamic_center - center_of_mass

    # Store data for plotting
    cg_diff_values.append(cg_diff)
    valid_b_values.append(b)
    
    # Print results for the current iteration
    print(f"Wingspan: {b:.2f} m | Center of Mass: {center_of_mass:.4f} m | total fuselage lenth: {fuselage_length:.4f} m | aerodynamic centre: {wing_position + 0.081:.4f} m | lt: {Lt:.4f} ")
    print('s',s,'sh',sh,'cm',cm)
    print('')
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

def momenty_mplane(b, Cgw, Ww, Cgf, Wf, Cgh, Wh, Cgv, Wv, s, sh, cm, W_t_p, f_w, f_h):
    """
    Calculates the center of mass of the plane with respect to the motor shaft tip.

    Returns:
    center_of_mass : Center of mass of the plane (m)
    
    """
    motor_length = 0.081
    x = 0.5 * 0.75 * b    
    a = 0.01 # side lenght
    Len = b * 0.75  # Approximate fuselage length
    vh = 0.7  # horizontal volume coeficient
    Lt = (vh * s * cm ) / sh  # Tail arm length
    #Lt = ((s * vh * cm) / ( f_w + f_h)) ** 2
    # Sum of moments about the motor shaft tip
    sum_of_moments = ((Len - Lt) + motor_length )* Ww + (Cgf * Wf) + ((Len + motor_length) * Wh) + (( Len + motor_length)* Wv)  

    wing_position = Len - Lt + 0.081
    # Total mass of the plane
    sum_mass = Ww + Wf + Wh + Wv
    # Center of mass location
    center_of_mass = sum_of_moments / sum_mass

    return center_of_mass, wing_position, Lt

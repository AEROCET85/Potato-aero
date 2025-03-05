def calculate_mfuselage(b, pd, fuselage_width, fuselage_height, carbon_fraction ,W_t_p):
    l = 0.75 * b
    W = (
        2 * pd * (1 - carbon_fraction) * l * fuselage_height +
        2 * pd * (1 - carbon_fraction) * fuselage_width + 0.025
    )
    Wfs = W + ((3.14 * carbon_fraction * l) * (0.005** 2 - 0.004 ** 2) * 1500) + 2 * 0.04 * fuselage_width * pd

    moment_motor_prop = 0.141 * 0.0540  # weight in kg * cg distance from shaft tip
    moment_ESC = 0.070 * (0.051 + 0.081)
    moment_battery = 0.354 * (0.081 + 0.093 + 0.0775)
    moment_gyro = 0.040 *(0.081 + 0.093 + 0.05 + 0.025)
    moment_receiver = 0.040 * (0.081 + 0.093 + 0.025)
    moment_fuselage = W * (0.081 + (1 - carbon_fraction) * l / 2)
    moment_carbon_boom = (Wfs - W) * (0.081 + (1 - carbon_fraction) * l + (1 - carbon_fraction) * l / 2)
    moment_payload = W_t_p * (0.081 + 0.093 + 0.0635 + 0.01 + 0.155)
    sum_mass_moments = moment_motor_prop + moment_ESC + moment_battery + moment_gyro + moment_receiver + moment_fuselage + moment_carbon_boom  + moment_payload
    sum_mass = Wfs + 0.141 + 0.070 + 0.18 + 0.040 + 0.040 + W_t_p

    Cgf = sum_mass_moments / sum_mass
    Wf = sum_mass



    cg_falone = (moment_fuselage + moment_carbon_boom) / Wfs
    
    
    return Wf, Cgf, cg_falone, Wfs
'''
MOTOR LENGTH APROX = 43 + 36 +2 = 81 MM
ESC LENGTH = 93 MM
RECEIVER LENGTH = 25 MM
'''

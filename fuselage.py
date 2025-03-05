def calculate_fuselage(b, pd, fuselage_width, fuselage_height, carbon_fraction):
    l = 0.75 * b
    W = (
        2 * pd * (1 - carbon_fraction) * l * fuselage_height +
        2 * pd * (1 - carbon_fraction) * fuselage_width
    )
    Wf = W + 2 * ((3.14 * carbon_fraction * l) * (0.005 ** 2 - 0.004 ** 2) * 1500) + 2 * 0.04 * fuselage_width * pd + 0.025 #extra for 2 struct and other weights
    return Wf

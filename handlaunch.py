W = 2.0006 # weight of the plane in kg
CL = 1.5644  # CL max
t = 0.001  # incrementing time step
T = 1  # Thrust in Newton

while True:
    u = 0  # initial vertical velocity wrt ground while hand launching
    v = 5  # horizontal velocity wrt ground while hand launching
    h = 1.5  # height of plane release in m
    flag = 0

    while True:
        v = v + ((T / W) * t)  # change in horizontal velocity with increment of time
        L = 0.5 * 1.22 * (v ** 2) * CL * 0.24  # Lift

        if L >= (W * 9.8):  # check whether lift is greater than weight of the plane
            flag = 1  # if satisfied, flag is shown
            break

        u = u + (((W * 9.8) - L) / W) * t  # change in vertical velocity with increment of time
        s = (u * t) + (0.5 * ((W * 9.8) - L) * (t ** 2) / W)  # distance travelled in t
        h = h - s  # height of the plane from ground

        if h <= 0:
            flag = 0  # if plane touches the ground, the flag is not shown and required lift is not achieved, indicating higher thrust requirement
            break

    if flag == 1:
        print(T, "is the minimum thrust required")
        break

    T = T + 1  # incrementing thrust value by 1 after each iteration

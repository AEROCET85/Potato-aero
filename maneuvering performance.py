from matplotlib.pyplot import *
import math

W = 2.0006  # weight of the plane in kg
VL = list()  # list to contain velocity values
RL = list()  # list to contain radius values
CL = 1.5644  # max CL value
S = 0.24  # planform area of wing in m^2
vinf = 10  # velocity of plane in m/s

for vinf in range(8, 21, 2):
    L = 0.5 * 1.225 * (vinf ** 2) * CL * S  # lift
    if L <= (W * 9.8):
        continue
    n = L / (W * 9.8)  # load factor
    R = (vinf ** 2) / (9.81 * math.sqrt((n ** 2) - 1))  # radius of maneuvering
    VL.append(vinf)
    RL.append(R)

plot(VL, RL)
xlabel('Velocity (m/s)')
ylabel('Radius (m)')
show()


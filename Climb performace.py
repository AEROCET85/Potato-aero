import numpy as np
import matplotlib.pyplot as plt
import math

# Parameters
rho = 1.225
S=0.24
Cd0 = 0.02004
W=2.1 *9.8 #In Newton
pr_eff=0.85 #Propeller efficiency
Pmax=457.66
Pa=Pmax*pr_eff
k = 0.05198
Clmax=1.87


#Computations
p=0.5*rho*S


gamma_ascend= []
gamma_descend= []
vel_ascend = []
vel_descend=[]
Stall_vel=[]


# Loop through gamma_angle values
for gamma_angle in np.arange(0, 30, 0.1):
    # Define the polynomial coefficients
    coefficients = [
        ((p**2)*Cd0),0,(W*p * math.sin(math.radians(gamma_angle))),
        -(Pa*p),
        (k * (W ** 2)*(math.cos(math.radians(gamma_angle))**2)),
    ]

    # Find the roots of the polynomial
    roots = np.roots(coefficients)
    # Extract only real positive roots
    real_positive_roots = [r.real for r in roots if np.isreal(r) and r.real > 0]

    # Store the results
    for root in real_positive_roots:
        Lmax_minvel=p*(min(real_positive_roots)**2)*Clmax
        vel_ascend.append(min(real_positive_roots))
        gamma_ascend.append(gamma_angle)
        Lmax_maxvel = p * (max(real_positive_roots) ** 2) * Clmax
        vel_descend.insert(0,max(real_positive_roots))
        gamma_descend.insert(0,gamma_angle)

    #For stall velocity
    V_stall=math.sqrt((W*math.cos(math.radians(gamma_angle)))/(p*Clmax))
    Stall_vel.append(V_stall)

Velocity=vel_ascend+vel_descend
Gamma=gamma_ascend+gamma_descend
Gamma_stall=np.linspace(0,30,len(Stall_vel))

print(vel_ascend)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(gamma_descend,vel_descend, color='b', linestyle='-',label='Max velocity')
plt.plot(gamma_ascend,vel_ascend, color='g', linestyle='-',label='Min velocity')
plt.plot(Gamma_stall, Stall_vel, color='r', linestyle='-',label='Stall velocity')
plt.xlabel('Gamma Angle')
plt.ylabel('Velocity(m/s)')
plt.title('Maximum and minimum velocities vs Gamma')
plt.legend()
plt.grid(True)
plt.show()
import numpy as np
import matplotlib.pyplot as plt

# Constants
Cd0 = 0.02004
rho = 1.225
s = 0.24
Pmax=457.66
pr_eff=0.85
Pa=Pmax*pr_eff
k = 0.05198
w = 2.1*9.8
Cl = 1.87

# Lists to store pa values and corresponding real positive roots
pa_values = []
real_positive_roots_list = []

# Loop over pa values
for pa in np.arange(700, 0, -10):
    # Define the polynomial coefficients
    coefficients = [((s**2) * Cd0 * (rho ** 2) * 0.25), 0, 0, (-rho * s * pa * 0.5), (k * (w ** 2))]

    # Find the roots of the polynomial
    roots = np.roots(coefficients)

    # Filter for real and positive roots
    real_positive_roots = [root.real for root in roots if np.isreal(root) and root.real > 0]

    # Store pa and corresponding real positive roots
    pa_values.append(pa)
    real_positive_roots_list.append(real_positive_roots)

# Calculate v_stall
v_stall1 = (2 * w) / (rho * s * Cl)
v_stall = np.sqrt(v_stall1)

# Find the pa value corresponding to v_stall
pa_at_v_stall = None
for i, roots in enumerate(real_positive_roots_list):
    if np.any(np.isclose(roots, v_stall, atol=1e-2)):  # Check if v_stall is close to any root
        pa_at_v_stall = pa_values[i]
        break

# Plotting
plt.figure(figsize=(10, 6))
for i, roots in enumerate(real_positive_roots_list):
    pa = pa_values[i]
    if roots:  # If there are real positive roots
        plt.scatter(roots, [pa] * len(roots), color='blue', label='Velocity' if i == 0 else "")

# Plot v_stall as a vertical line
plt.axvline(x=v_stall, color='red', linestyle='--', label=f'v_stall = {v_stall:.2f} m/s')
plt.axhline(y=Pa, color='orange', linestyle='--', label=f'Max Power = {Pa:.2f} W')


# Add labels and title
plt.ylabel('Power(W)')  # pa on y-axis
plt.xlabel('Velocity(m/s)')  # Real positive roots on x-axis
plt.title('Power vs Velocity')
plt.grid(True)
plt.legend()
plt.show()
import seaborn as sns
import matplotlib.pyplot as plt
import Beams

x_sf = Beams.x_array
x_bm = Beams.x2_array
y_sf = Beams.sf_array
y_bm = Beams.bm_array
span = Beams.beam_length

sns.set_style('whitegrid')

# Create the subplots
fig, (ax_sf, ax_bm) = plt.subplots(2, 1, sharex=True, figsize=(8, 8))

# Plot the shear force diagram on the first subplot
ax_sf.plot(x_sf, y_sf, label='Shear Force', color='green')
ax_sf.axhline(y=0, color='black', linewidth=1)
ax_sf.set_ylabel('Shear Force (kN)')
ax_sf.set_title('Shear Force and Bending Moment Diagrams')

# Plot the bending moment diagram on the second subplot
ax_bm.plot(x_bm, y_bm, label='Bending Moment', color='blue')
ax_bm.axhline(y=0, color='black', linewidth=1)
ax_bm.set_xlabel('Distance (m)')
ax_bm.set_ylabel('Bending Moment (kNm)')

# Set the axis limits
ax_sf.set_xlim([-1, span+1])
ax_bm.set_xlim([-1, span+1])

# Set the title and legend for the entire figure
fig.suptitle('Shear Force and Bending Moment Diagrams')
fig.legend()

# Show the plot
plt.show()

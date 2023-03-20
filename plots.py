import seaborn as sns
import matplotlib.pyplot as plt
import Beams

x = Beams.x_array
y = Beams.sf_array
span = Beams.beam_length

sns.set_style('whitegrid')

# Create the plot
plt.plot(x, y, label='Shear Force', color='green')

plt.axhline(y=0, color='black', linewidth=1)

# Set the axis labels
plt.xlabel('Distance (m)')
plt.ylabel('Shear Force (kN)')

# Set the axis limits
plt.xlim([-1, span+1])

# Set the title and legend
plt.title('Shear Force Diagram')
plt.legend()

# Show the plot
plt.show()

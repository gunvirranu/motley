import matplotlib.pyplot as plt
import numpy as np

"""
Bifurcation Diagram
"""

# Number of `r` steps in closed interval [0.5, 4]
rsteps = 5000
# Values of r between [0.5, 4], but can be changed to zoom
#  in on a specific area
rar, step = np.linspace(1, 4, rsteps, retstep=True)
# rar, step = np.linspace(2.8, 3.4, rsteps, retstep=True)


# Initialize empty list `b` to hold final data
b = []
# Iterate over all the values of `r`
for r in rar:
    # Initialize iterations list with starting value of 0.5
    a = [0.5]
    # Do fixed point iteration 299 times so the final
    #  length of `a` is 300, because starting value
    # All iterations use the same `r` value
    for it in range(499):
        # Add new value computed using function
        # Computed using last values of iterations
        #  and current `r` value
        a.append(r * a[-1] * (1 - a[-1]))
    # Now you have a list `a` with values of 199
    #  iterations of the function using some `r` value
    # Since it takes a few iterations for the oscillations
    #  to settle down between certain values, you only take
    #  the final 100 values instead of all 300, but the
    #  final 100 should all be very close anyway because
    #  they are just oscillating between specific values
    # You just don't want the initial ones where the
    #  oscillating values are still settling

    # So you ignore the first 200, and append `a` to `b`,
    #  so you are adding a list to a list, making it 2D
    b.append(a[300:])

# After all that is done, `b` is a 2D list, which just
#  means each element is a list itself
# The rows in `b` are different `r` values, in accordance
#  to `rar`, which was used to generate the `r` values
# So each row in `b` corresponds to some `r` value in `rar`
# Accessing a 2D list is done as follows:
#  element = some_2D_list[row][column]
# Example: The following list of iterations uses the `r`
#  value in the same position in the `rar` list:
#  `r` value: `rar[3]`, all_iterations: `b[3]`
# Each column in `b` is a different iteration, but
#  remember we ignored the first 100 iteration
# This means there are going to be 100 columns, each
#  a different iteration, from 100 to 200
# So to get the value after 220 iterations (remember only
#  have last 100) using the fourth (zero indexing) `r`
#  value in `rar`, you would do the following:
#  `value = b[3][20]`

# So the bifurcation diagram x-axis is the `r` value,
#  y-axis is the value of the function, and iterations
#  are mutliple y points for the same `r` value on the x
# This means for each `r` value, we need to plot all the
#  values of the iteration, which is essentially like
#  plotting every single column independantly, but indexing
#  columns is not so simple in Python, because you have to
#  select a row and then a column like I explained above
# It can still be done with two for loops and this is how
#  it would be done, so this needs to be understood
#  for i in range(100):
#      tmp = []
#      for it in range(rsteps):
#          tmp.append(b[it][i])
#      plt.plot(rar, tmp, ',')
# You could run the above code and it would work
# You are looping over the iterations (columns), and then
#  the `r` values (rows), making a temporary list for
#  holding the column
# You then plot the whole column on the x-axis, which
#  represents all the values for a different `r`, but the
#  same iteration
# The `rar` is just there for the x-axis values

# BUT, there is a much easier way to do this
# The matplotlib plot function works very well with 2D
#  input arrays and actually plots in the exact way we
#  want it to be plotted, so we don't need to loop over
#  the data, and can instead just pass the `b` 2D list to
#  the plot function without doing anything
# Of course we still want the x-axis values, so we just put
#  `rar` before it for the x-axis `r` values
# And the comma is just for the marker used for plotting

# Plot this and a bifurcation diagram appears
# :)

plt.plot(rar, b, ',', color='0.3')
plt.show()
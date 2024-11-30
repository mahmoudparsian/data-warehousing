# python3 -m pip install -U pip
# python3 -m pip install -U matplotlib
# python3 visual_x_y_01.py

import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Sine Wave')
plt.show()

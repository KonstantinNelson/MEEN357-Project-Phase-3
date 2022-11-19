import matplotlib.pyplot as plt
import scipy.interpolate as inte
import numpy as np
mach = [0.25,0.5,0.65,0.7,0.8,0.9,0.95,1.0,1.1,1.2,\
    1.3,1.4,1.5,1.6,1.8,1.9,2.0,2.2,2.5,2.6]

MEF = [1.0,1,1,.98,.9,.72,.66,.76,.9,.96,.99,.999,\
    .992,.98,.9,.85,.82,.75,.65,.62]

fun = inte.interp1d(mach, MEF,kind='cubic',)
mach_s = np.linspace(.25,2.6, 200)
MEF_s = fun(mach_s)

fig, ax = plt.subplots()
ax.scatter(mach,MEF)
ax.plot(mach_s, MEF_s)
ax.set_title('cubic')
plt.show()
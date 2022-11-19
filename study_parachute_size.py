import numpy as np
import matplotlib.pyplot as plt
from define_edl_system import *
from subfunctions_EDL import *
from define_planet import *
from define_mission_events import *

# *************************************
# load dicts that define the EDL system (includes rover), planet,
# mission events and so forth.
edl_system = define_edl_system_1()
mars = define_planet()
mission_events = define_mission_events()

tmax = 2000   # [s] maximum simulated time

param = []
sim_time = []
rover_speed = []
success = []

diam = np.arange(14.0,19.5,0.5)
for i in diam:
    edl_system['altitude'] = 11000    # [m] initial altitude
    edl_system['velocity'] = -578     # [m/s] initial velocity
    edl_system['parachute']['deployed'] = True   # our parachute is open
    edl_system['parachute']['ejected'] = False   # and still attached
    edl_system['heat_shield']['ejected'] = False   #reattach the heat  shield
    edl_system['sky_crane']['on'] = False   #disable sky crane
    edl_system['rocket']['on'] = False          #disable rockets
    edl_system['speed_control']['on'] = False       #disable speed control
    edl_system['position_control']['on'] = False    #disable position control
    edl_system['rover']['on_ground'] = False # the rover has not yet landed
    edl_system['parachute']['diameter'] = float(i) #change the value of parachute diameter
    print('Simulation with parachute of diameter of',i,'meters:\n')
    print('-'*54+'\n')
    [t, Y, edl_system] = simulate_edl(edl_system, mars, mission_events, tmax, True)     #retrieve simulation data
    param.append([t,Y,edl_system])
    sim_time.append(max(t))     #add the simulation time to sim_time
    rover_speed.append(Y[0,-1])     #add the final rover speed to rover_speed
    if Y[0,-1] <= 1 and edl_system['altitude'] >= 4.5:  #if the rover meets the critical conditions, the simulation succeeded
        success.append(1)
    else:
        success.append(0)



f = plt.figure(figsize=(8,7))
ax=f.add_subplot(311,xlabel='Diameter [m]',ylabel='Time [s]')
ax.title.set_text('Simulation Time vs. Parachute Diamater')
ax2=f.add_subplot(312,xlabel='Diameter [m]',ylabel='Velocity [m/s]')
ax2.title.set_text('Final Rover Velocity vs. Parachute Diameter')
ax3=f.add_subplot(313,xlabel='Diameter [m]',ylabel='Success')
ax3.title.set_text('Rover Landing Success vs. Parachute Diameter')
ax.plot(diam,sim_time)
ax2.plot(diam,rover_speed)
ax3.plot(diam,success)
plt.tight_layout()
plt.savefig('Task5.png',format='png')

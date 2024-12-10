"""
Getting figures and plots for Q4 of TMM coursework
"""

import matplotlib.pyplot as plt
import numpy as np

tau = 1
d_c = 12
v_0 = 20
v_a = 10

# plotting traffic jam scenario
import ovm_spec1_2 as ovm_spec1
import ovm_spec2_2 as ovm_spec2
import polygon

# Show window

dt = 0.05
spec1_sim = ovm_spec1.Simulation()
spec2_sim = ovm_spec2.Simulation()

# initialise matplot lib figure with 2 axes
fig, (ax1, ax2) = plt.subplots(2, 1)
# Adjust vertical spacing
plt.subplots_adjust(hspace=0.5)  # Increase hspace to add more space

# initialise free flow study
# spec1_sim.traffic = False
# spec1_sim.crash = False
# spec2_sim.traffic = False
# spec2_sim.crash = False
# initialise traffic study
# spec1_sim.traffic_queue()
# spec2_sim.traffic_queue()
# spec1_sim.crash = False
# spec2_sim.crash = False
# initialise crash study
spec1_sim.traffic = False
spec1_sim.crash = True
spec2_sim.traffic = False
spec2_sim.crash = True

# changing values in order to mimic real traffic scenarios
# max safe acceleration/deceleration = 4.6m/s^2
# https://copradar.com/chapts/references/acceleration.html

# # Free flow motorway traffic 70mph = 31 m/s
# spec1_sim.base_v = 31
# spec2_sim.base_v = 31

# # Therefore find tau: 4.6 = 31/tau
# spec1_sim.tau = 6.7
# spec2_sim.tau = 6.7

# # decide on characteristic distance, safe distance 2s
# spec1_sim.d_c = 62
# spec2_sim.d_c = 62



for i in range(int(120/dt)):
    spec1_sim.update(dt)
    spec2_sim.update(dt)
    if i%20==0:
        ax1.cla()
        ax2.cla()
        spec1_sim.render(ax1)
        spec2_sim.render(ax2)
        # plt.show()
        plt.pause(0.001)

plt.ioff()  # Turn off interactive mode
plt.show()

spec1_sim.print_traj("test_sim1_3",r"C:\Users\Sez26\Documents\MATLAB\Yr5\TMM\Coursework\Serena\Q4\Sim_op")
spec2_sim.print_traj("test_sim2_3",r"C:\Users\Sez26\Documents\MATLAB\Yr5\TMM\Coursework\Serena\Q4\Sim_op")

# Starting from stopped (off boarding a ferry)

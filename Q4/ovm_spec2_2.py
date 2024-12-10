# Author: Anders Johansson (a.johansson@bristol.ac.uk)
# Description: This file contains functionality to simulate pedestrian crowds.
# Date: 2024-10-10

from matplotlib import pyplot as plt
import random
import math
import numpy as np
import sys
import csv
import os

# this is a file
from polygon import join_all_polygons

# oml these are kill buttons
def keyboard_event(event):
    if event.key=='escape' or event.key=="q":
        print('You pressed:', event.key, " - bye!")
        exit()
# but they don't work lol

# Show window
plt.ion()

class Vehicle:
    def __init__(self, x, v, v_desired):
        self.x = x                          # Current vehicle position (m)
        self.v = v                          # Current vehicle speed (m/s)
        self.v_desired = v_desired          # Desired (free) vehicle speed (m/s

class Simulation:
    def __init__(self):
        self.time = 0
        # Vehicle data
        self.vehicles = []                               # List of vehicles currently on the road
        self.trajectories = {                            # Vehicle trajectories
            "t": [], 
            "x": [], 
            "density": [],
            "flow": [],
            "velocity": [],
            "crash_count": [],
        }                                 
        # Model parameters
        self.inflow = 0.1                                # Cars per second
        self.dt = 0.1                                    # Time step (s)
        self.Lc = 5                                      # Car length (m)
        self.Lr = 1000                                   # Road length (m)
        self.tau = 4.6                                     # Relaxation time (s)
        self.d_c = 96                                    # Model parameter, characteristic distance (m)
        self.base_v = 3
        self.var_v = 0

        # Traffic Light Scenario
        self.traffic = True
        self.num_queue = 10
        self.queue_dx = 10
        self.green_light_t = 30
        self.light_loc = 200

        # Crash Scenario
        self.crash = False
        self.crash_time = 60                             # Time of Crash
        self.crash_c = 0                                 # Crash counter
        self.crash_loc = 0                               # Crash location

    def traffic_queue(self):
        for i in range(self.num_queue):
                self.vehicles.append(Vehicle(x=(self.light_loc-((self.num_queue-i)*self.queue_dx)), v=0, v_desired=0))

    def update(self, dt):
        self.time += dt
        # Introduce new cars onto the road
        if random.random()<self.inflow*dt:
            if self.traffic:
                # do nothing, no new incoming cars whilst traffic light is red
                pass
            # Make sure that there is free space
            elif len(self.vehicles)==0 or self.vehicles[0].x>self.Lc: # if there are no cars and no cars in the first car length
                speed = self.base_v + self.var_v*random.random()
                self.vehicles.insert(0, Vehicle(x=0, v=0, v_desired=speed))
            
        # Traffic Light Scenario
        if self.traffic and self.time>self.green_light_t:
            # let the cars go
            self.vehicles = [] # clear queuing vehicles
            for i in range(self.num_queue):
                speed = self.base_v + self.var_v*random.random()
                self.vehicles.append(Vehicle(x=(self.light_loc-((self.num_queue-i)*self.queue_dx)), v=0, v_desired=speed))
            self.traffic = False
        else:
            # normal sim after this
            pass
        # Update vehicles
        n = len(self.vehicles)
        for i in range(n-1, -1, -1):

            d_alpha = self.vehicles[i+1].x - self.vehicles[i].x if n>1 and i<n-1 else 999999.0
            if d_alpha>10:
                f = math.tanh((d_alpha/(self.vehicles[i].v + 1e-10)))+math.tanh(1)
            else:
                f = 0

            v_e = self.vehicles[i].v_desired/2*f
            acc = (v_e - self.vehicles[i].v)/self.tau

            # Add traffic jam
            # if self.vehicles[i].x>=700 and self.vehicles[i].x<=710:
            #    self.vehicles[i].v = min(0, self.vehicles[i].v)

            # # Add breakdown (set self.crash condition)
            if self.crash:
                if self.time > self.crash_time:
                    # find the leading car
                    lead_car_idx = max(range(len(self.vehicles)), key=lambda i: self.vehicles[i].x)
                    # make the lead car breakdown!
                    self.vehicles[lead_car_idx].v = 0
                    if self.crash_c == 0: # initial loop
                        self.crash_loc = self.vehicles[lead_car_idx].x
                        self.crash_c = 1
                    else:
                        self.vehicles[lead_car_idx].x = self.crash_loc  
                  
            # Prevent crashes
            if i<n-1 and self.vehicles[i].x > self.vehicles[i+1].x - 0.01:
                # self.vehicles[i].x = self.vehicles[i+1].x - 0.01
                # this is fucking with my plot
                self.vehicles[i].x = self.vehicles[i+1].x - 0.01
                self.vehicles[i].v = 0
                self.vehicles[i+1].v = 0
                self.crash_c += 1
                self.trajectories["crash_count"].append(self.crash_c)
            else:
                self.vehicles[i].v += dt*acc
                self.vehicles[i].x += dt*self.vehicles[i].v

            # Add current position to trajectories
            self.trajectories["t"].append(self.time)
            self.trajectories["x"].append(self.vehicles[i].x)
            self.trajectories["density"].append(len(self.vehicles) / self.Lr)
            self.trajectories["flow"].append(len(self.vehicles) / self.Lr * self.vehicles[i].v)
            self.trajectories["velocity"].append(self.vehicles[i].v)
            self.trajectories["crash_count"].append(self.crash_c)

        # Remove vehicles outside road
        for i in range(n):
            if self.vehicles[i].x > self.Lr:
                self.vehicles.pop(i)

    def render(self,ax):
        # Plot current state
        ax.fill([0, self.Lr, self.Lr, 0], [-3, -3, 3, 3], facecolor="gray", edgecolor="gray")
        for i in range(len(self.vehicles)):
            ax.plot(self.vehicles[i].x, 0.0, "ko", linewidth=5)

        ax.set_xlim(-5, self.Lr + 5)
        # plt.ylim(-5, self.Lr/4)
        ax.set_title("Model 2: " + str(round(100*self.time)/100.0) + " s")

    def print_traj(self, file_name, save_dir):
        # File name for the CSV
        # Ensure the directory exists
        os.makedirs(save_dir, exist_ok=True)

        # Construct the full file path
        file_path = os.path.join(save_dir, file_name)

    # Open a file in write mode
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            
            # Write the header (keys of the dictionary)
            writer.writerow(self.trajectories.keys())
            
            # Write the rows (values of the dictionary)
            # Transpose the values to match the structure
            rows = zip(*self.trajectories.values())
            writer.writerows(rows)

        print(f"CSV file '{file_name}' created successfully!")


# dt = 0.05
# sim = Simulation()
# for i in range(int(120/dt)):
#     sim.update(dt)
#     if i%20==0:
#         sim.render()

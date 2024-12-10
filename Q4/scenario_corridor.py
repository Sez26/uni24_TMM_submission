# Author: Anders Johansson (a.johansson@bristol.ac.uk)
# Description: This file contains functionality to simulate pedestrian crowds.
# Date: 2024-10-10

from world import World, normalise_vector, vector_length, get_nearest_position
import math
import numpy as np

def pedestrian_initialisation(pedestrian, polygons, statistics):
    pass

def update_directions(pedestrians, boundaries, polygons):
    for i, ped in pedestrians.items():
        destination_polygon_centroid = polygons[ped.destination]["nodes"].mean(axis=0)
        ped.desired_direction = normalise_vector(destination_polygon_centroid - ped.pos)

def process_interactions(pedestrians, boundaries, polygons):
    # Parameters
    tau = 0.5
    A_boundary_social, B_boundary_social = .5, 2
    A_boundary_physical = 50
    A_social, B_social = .5, 2
    A_physical = 4
    Lambda = 0.2
    for i, ped_i in pedestrians.items():
        ped_i.acc = (ped_i.desired_walking_speed*ped_i.desired_direction - ped_i.vel) * (1/tau)
        # Pairwise forces from other pedestrians
        for j, ped_j in pedestrians.items():
            if i!=j:
                distance = vector_length(ped_i.pos - ped_j.pos)
                tangent = normalise_vector(ped_i.pos - ped_j.pos)
                # Angular dependency
                vec_ij = normalise_vector(ped_j.pos - ped_i.pos)
                cos_phi = normalise_vector(ped_i.vel).dot(vec_ij)
                angular_dependency = Lambda + (1.0 - Lambda)*((1+cos_phi)/2.0)
                # Apply physical force
                if distance <= ped_i.radius+ped_j.radius:
                    ped_i.acc += A_physical*tangent
                # Apply social force
                ped_i.acc += A_social*angular_dependency*math.exp(-(distance)/B_social)*tangent
        # Forces from boundaries
        for boundary in boundaries:
            pos_b  = get_nearest_position(ped_i.pos, boundary)
            distance = vector_length(ped_i.pos - pos_b)
            tangent = normalise_vector(ped_i.pos - pos_b)
            # Apply physical boundary force
            if distance <= ped_i.radius:
                ped_i.acc += A_boundary_physical*tangent
            # Apply social boundary force
            ped_i.acc += A_boundary_social*math.exp(-(distance)/B_boundary_social)*tangent


# Define modelling scenario
corridor_width = 4
corridor_length = 20
world_definition = {
    "space": {
        "corridor": {"type": "rectangle", "coordinates": [0, 0, corridor_length, corridor_width], "colour": "gray", "add_boundaries": False},
        "right": {"type": "rectangle", "coordinates": [corridor_length+1, 0, corridor_length+2, corridor_width], "colour": "green", "add_boundaries": False},
    },
    "pedestrians": {
        "group1": {"source": "corridor", "destination": "right", "colour": "red", "birth_rate": 99, "max_count": 10}
    },
    "boundaries": [[0, 0, corridor_length, 0], [0, corridor_width, corridor_length, corridor_width]],
    "periodic_boundaries": {"axis": "x", "pos1": 0, "pos2": corridor_length},
    "functions": {
        "update_directions": update_directions,
        "process_interactions": process_interactions,
        "pedestrian_initialisation": pedestrian_initialisation
    }
}

world = World(world_definition)

# Run simulation for 60 seconds
for i in range(1200):
    world.update(0.05)
    if i%20==0:
        world.render()

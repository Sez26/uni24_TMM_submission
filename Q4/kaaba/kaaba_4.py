from world_4 import World, normalise_vector, vector_length, get_nearest_position
import math
import numpy as np

def pedestrian_initialisation(pedestrian, polygons, statistics):
    pass

def update_directions(pedestrians, boundaries, polygons, centre=np.array([0, 0])):
    for i, ped in pedestrians.items():
        # Initialize the starting position if not already recorded
        if not hasattr(ped, 'start_angle'):
            ped.start_angle = math.atan2(ped.pos[1] - centre[1], ped.pos[0] - centre[0])  # Record the initial angle
        
        else:
            # check if cicles have been completed
            if not ped.complete:
                # Calculate different direction cases
                # circular walking behaviour
                destination_weight = 0.02 * (vector_length(centre - ped.pos)-6) # offset because cannot get into kaaba # how much they want to be close to the kaaba
                #destination_polygon_centroid = polygons[ped.destination]["nodes"].mean(axis=0)
                #ped.desired_direction = normalise_vector(destination_polygon_centroid - ped.pos)
                direction_to_destination = normalise_vector(centre - ped.pos)
                direction_to_center = normalise_vector(centre - ped.pos)
                # Perpendicular direction to ensure counter-clockwise motion (tangent to the circle)
                tangent_direction = np.array([direction_to_center[1], -direction_to_center[0]])  # 90-degree counter-clockwise rotation
                # Set the desired direction to be tangential (circular walking)
                combined_direction = normalise_vector(tangent_direction + destination_weight * direction_to_destination)
                if ped.num_circles < 2: # this isn't working well
                    
                    ped.desired_direction = combined_direction
                    
                    # rotations counter
                    if (ped.pos[0]<0 and ped.prev_pos[0]>0 and ped.pos[1]>0):
                        ped.num_circles += 1
                    else:
                        pass
                else:
                    # setting finish direction
                    ped.desired_direction = tangent_direction
                    ped.complete = True
            else:
                ped.colour = "blue"
                # don't update direction

def process_interactions(pedestrians, boundaries, polygons):
    # Parameters
    tau = 0.5
    A_boundary_social, B_boundary_social = .5, 2
    A_boundary_physical = 50
    A_social, B_social = .5, 2
    A_physical = 4
    Lambda = 0.2
    centre = np.array([0, 0])  # Assuming the central point is at (0, 0)
    radius_threshold = 6  # Density threshold in persons per square meter
    radius_check = 5  # Radius to check local density (in meters)
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

        # 2. Local Density Check and Social Force for High Density Areas
        local_density = 0
        for j, ped_j in pedestrians.items():
            if i != j:
                distance_to_ped_j = vector_length(ped_i.pos - ped_j.pos)
                if distance_to_ped_j <= radius_check:
                    local_density += 1
        # Calculate the area of the circle (for density calculation)
        area_of_circle = math.pi * radius_check**2
        # Density in persons per square meter
        density = local_density / area_of_circle
        # If density exceeds the threshold, apply a force pushing away from the center
        # exception after spawning
        if world.time - ped_i.birth_time < 10:
            pass
        elif density > radius_threshold:
            # Force pushing away from the central point to reduce density
            away_from_center = normalise_vector(ped_i.pos - centre)
            ped_i.acc += A_social * away_from_center  # You can adjust this force as needed

# Define modelling scenario
# Define the radius of the circle
r = 12  # for example, radius = 5

circle = []
for i in range(128):
    x = r * math.cos(2 * math.pi * i / 16.0)  # Multiply by radius
    y = r * math.sin(2 * math.pi * i / 16.0)  # Multiply by radius
    circle.append([x, y])

circle = np.array(circle)

from shapely.geometry import Polygon, Point
# or create another bigger circle around the kaaba where the people are generated
# walk around it counter clockwise 7 times
# kinda want to start with people already there and with a random amount of circles completed
   
world_definition = {
    "space": {
        # "out_kaaba": {"type": "polygon", "coordinates": list.area_with_hole.exterior.coods, "colour": "white", "add_boundaries": False},
        "walking space": {"type": "rectangle", "coordinates": [-40, -40, 40, 40], "colour": "lightyellow", "add_boundaries": False},
        "kaaba": {"type": "rectangle", "coordinates": [-5, -5, 5, 5], "colour": "black", "add_boundaries": True},
        # "kaaba2": {"type": "polygon", "coordinates": circle, "colour": "black", "add_boundaries": True}, # it was -5 -5 5 10
        #"irrelevant": {"type": "rectangle", "coordinates": [-40, -38, 40, -40], "colour": "black", "add_boundaries": False},
        "end": {"type": "polygon", "coordinates": [[-40, -40], [-40, -38], [38, -38], [38, 38], [-38, 38], [-38,-38], [-40,-38], [-40, 40], [40, 40], [40, -40]], "colour": "white", "add_boundaries": False},
        # need to make it so that pedestrians cannot spawn inside kaaba
        # create 4 spawn points
        "spawn1": {"type": "rectangle", "coordinates": [-35, -35, -34, -34], "colour": "magenta", "add_boundaries": False},        
        "spawn2": {"type": "rectangle", "coordinates": [34, 34, 35, 35], "colour": "magenta", "add_boundaries": False},        
        "spawn3": {"type": "rectangle", "coordinates": [-35, 34, -34, 35], "colour": "magenta", "add_boundaries": False},        
        "spawn4": {"type": "rectangle", "coordinates": [35, -35, 34, -34], "colour": "magenta", "add_boundaries": False},        
    },
    "pedestrians": {
        # make four possible input points, initialised destination centre of kaaba
        "group1": {"source": "spawn1", "destination": "end", "colour": "red", "birth_rate": 0.1, "max_count": 80},
        "group2": {"source": "spawn2", "destination": "end", "colour": "red", "birth_rate": 0.1, "max_count": 80},
        "group3": {"source": "spawn3", "destination": "end", "colour": "red", "birth_rate": 0.1, "max_count": 80},
        "group4": {"source": "spawn4", "destination": "end", "colour": "red", "birth_rate": 0.1, "max_count": 80},
        # "group1": {"source": "walking space", "destination": "end", "colour": "red", "birth_rate": 0.5, "max_count": 80},
    },
    #"boundaries": [[2, 0, corridor_length, 0], [2, corridor_width, corridor_length, corridor_width]],
    #"periodic_boundaries": {"axis": "x", "pos1": 0, "pos2": corridor_length},
    "functions": {
        "update_directions": update_directions,
        "process_interactions": process_interactions,
        "pedestrian_initialisation": pedestrian_initialisation
    }
}

world = World(world_definition)

# Run simulation for 60 seconds
# for i in range(2000):
#     world.update(0.1)
#     if i%50==0:
#         world.render()
#         pass

world.save_animation('./Serena/Q4/kaaba4_2.gif')
"""
DIGM 131 - Assignment 3: Function Library (scene_functions.py)
===============================================================

OBJECTIVE:
    Create a library of reusable functions that each generate a specific
    type of scene element. This module will be imported by main_scene.py.

REQUIREMENTS:
    1. Implement at least 5 reusable functions.
    2. Every function must have a complete docstring with Args and Returns.
    3. Every function must accept parameters for position and/or size so
       they can be reused at different locations and scales.
    4. Every function must return the name(s) of the Maya object(s) it creates.
    5. Follow PEP 8 naming conventions (snake_case for functions/variables).

GRADING CRITERIA:
    - [30%] At least 5 functions, each creating a distinct scene element.
    - [25%] Functions accept parameters and use them (not hard-coded values).
    - [20%] Every function has a complete docstring (summary, Args, Returns).
    - [15%] Functions return the created object name(s).
    - [10%] Clean, readable code following PEP 8.
"""

import maya.cmds as cmds
import math


# Function Library

#Creates a green groud plane, places it, and returns it.

def create_ground(name="ground", width=50, depth=50, position=(0, 0, 0)):
    """Create a ground plane in Maya and return its name."""
    ground = cmds.polyPlane(name=name, w=width, h=depth)[0]
    cmds.move(position[0], position[1], position[2], ground)
    return ground

#Creats a building, places it and returns it.

def create_building(name="building", position=(0, 0, 0), scale=1.0):
    """Create a building made of a base and roof and return both parts."""
    base = cmds.polyCube(name=f"{name}_base", w=4*scale, h=6*scale, d=4*scale)[0]
    roof = cmds.polyCube(name=f"{name}_roof", w=4.5*scale, h=2*scale, d=4.5*scale)[0]

    cmds.move(position[0], position[1] + 3*scale, position[2], base)
    cmds.move(position[0], position[1] + 7*scale, position[2], roof)

    return [base, roof]

#Creats a scaled rock, places it and returns it.

def create_rock(position=(0, 0, 0), scale=1.0):
    """Create a rock object at a position and return its name."""
    rock = cmds.polySphere(r=1 * scale, name="rock")[0]
    cmds.scale(scale, scale * 0.6, scale, rock)
    cmds.move(position[0], position[1], position[2], rock)
    return rock

#Creates and scatters cloud clusters, places it and returns it

def create_cloud(position=(0, 10, 0), scale=1.0):
    """Create a cloud made of multiple spheres and return all parts."""
    parts = []

    for i in range(3):
        cloud_part = cmds.polySphere(r=1 * scale, name=f"cloud_{i}")[0]
        cmds.move(position[0] + i * scale, position[1], position[2], cloud_part)
        parts.append(cloud_part)

    return parts

#Creats a sun sphere with orbiting rays arranged around it procedurally, places it and returns it

def create_sun(position=(0, 30, 0), scale=3.0):
    """Create a sun sphere and return its name."""
    sun = cmds.polySphere(r=2 * scale, name="sun")[0]
    cmds.move(position[0], position[1], position[2], sun)
    return sun


def create_sun_rays(count=8, radius=6, position=(0, 30, 0)):
    """Create sun rays arranged in a circle and return all ray names."""
    rays = []

    for i in range(count):
        angle = (2 * math.pi / count) * i
        x = position[0] + math.cos(angle) * radius
        z = position[2] + math.sin(angle) * radius

        ray = cmds.polyCube(w=0.5, h=3, d=0.5, name=f"ray_{i}")[0]
        cmds.move(x, position[1], z, ray)
        rays.append(ray)

    return rays


#creates a lambert shader and applies a given RGB color

def apply_color(obj, color):
    """Apply a Lambert color shader to a Maya object and return shader name."""
    shader = cmds.shadingNode('lambert', asShader=True)
    cmds.setAttr(shader + ".color", *color, type="double3")

    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)
    cmds.connectAttr(shader + ".outColor", sg + ".surfaceShader")

    cmds.sets(obj, edit=True, forceElement=sg)
    return shader


def flatten(items):
    """Flatten a nested list of Maya objects into a single list."""
    result = []
    for i in items:
        if isinstance(i, list):
            result.extend(i)
        else:
            result.append(i)
    return result


def color_all(objects, color):
    """Apply color to all objects in a list and return the list of objects."""
    for obj in objects:
        apply_color(obj, color)
    return objects


#Creates and randomly scatters rocks, buildings, and clouds around the center point with various different sizes

def build_scene():
    """Build the full Maya scene and return all created objects."""
    cmds.file(new=True, force=True)

    ground = create_ground(width=60, depth=60)

    rocks = scatter_rocks()
    buildings = place_buildings()
    clouds = scatter_clouds()

    sun = create_sun()
    rays = create_sun_rays()

    circle_rocks = [
        create_rock((math.cos(i)*6, 0, math.sin(i)*6), scale=0.8)
        for i in [j * (2*math.pi/8) for j in range(8)]
    ]

    #Color Edits

    apply_color(ground, (0.2, 0.7, 0.2))

    color_all(rocks, (0.75, 0.75, 0.75))
    color_all(circle_rocks, (0.75, 0.75, 0.75))

    color_all(flatten(buildings), (0.55, 0.75, 0.95))

    color_all(flatten(clouds), (1.0, 1.0, 1.0))

    apply_color(sun, (1.0, 0.9, 0.2))

    color_all(rays, (1.0, 0.6, 0.1))
    apply_color(rays[0], (1.0, 0.2, 0.0))


    #Builds a full procedural scene with ground, buildings, rocks, clouds, and a sun, then applies colors and combines all objects.

    all_objects = (
        [ground]
        + rocks
        + circle_rocks
        + flatten(buildings)
        + flatten(clouds)
        + [sun]
        + rays
    )

    print("Total objects:", len(all_objects))
    cmds.viewFit(allObjects=True)
    print("Scene built successfully!")


# RUN
build_scene()

# RUN
build_scene()

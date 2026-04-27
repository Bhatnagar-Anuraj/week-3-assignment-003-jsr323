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
    ground = cmds.polyPlane(name=name, w=width, h=depth)[0]
    cmds.move(*position, ground)
    return ground

#Creats a building, places it and returns it.
def create_building(position=(0, 0, 0), scale=1.0):
    base = cmds.polyCube(w=4*scale, h=6*scale, d=4*scale)[0]
    roof = cmds.polyCube(w=4.5*scale, h=2*scale, d=4.5*scale)[0]

    cmds.move(position[0], position[1] + 3*scale, position[2], base)
    cmds.move(position[0], position[1] + 7*scale, position[2], roof)

    return [base, roof]

#Creats a scaled rock, places it and returns it.
def create_rock(position=(0, 0, 0), scale=1.0):
    rock = cmds.polySphere(r=1 * scale)[0]
    cmds.scale(scale, scale * 0.6, scale, rock)
    cmds.move(*position, rock)
    return rock

#Creates and scatters cloud clusters, places it and returns it
def create_cloud(position=(0, 10, 0), scale=1.0):
    parts = []
    for i in range(3):
        c = cmds.polySphere(r=1 * scale)[0]
        cmds.move(position[0] + i * scale, position[1], position[2], c)
        parts.append(c)
    return parts

#Creats a sun sphere with orbiting rays arranged around it procedurally, places it and returns it
def create_sun(position=(0, 30, 0), scale=3.0):
    sun = cmds.polySphere(r=2 * scale)[0]
    cmds.move(*position, sun)
    return sun


def create_sun_rays(count=8, radius=6, position=(0, 30, 0)):
    rays = []

    for i in range(count):
        angle = (2 * math.pi / count) * i
        x = position[0] + math.cos(angle) * radius
        z = position[2] + math.sin(angle) * radius

        ray = cmds.polyCube(w=0.5, h=3, d=0.5)[0]
        cmds.move(x, position[1], z, ray)
        rays.append(ray)

    return rays


#creates a lambert shader and applies a given RGB color
def apply_color(obj, color):
    shader = cmds.shadingNode('lambert', asShader=True)
    cmds.setAttr(shader + ".color", *color, type="double3")

    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)
    cmds.connectAttr(shader + ".outColor", sg + ".surfaceShader")

    cmds.sets(obj, edit=True, forceElement=sg)


def flatten(items):
    result = []
    for i in items:
        if isinstance(i, list):
            result.extend(i)
        else:
            result.append(i)
    return result


def color_all(objects, color):
    for obj in objects:
        apply_color(obj, color)


#Creates and randomly scatters rocks, buildings, and clouds around the center point with various different sizes
def scatter_rocks(count=12, radius=20, center=(0, 0)):
    rocks = []

    for i in range(count):
        angle = (2 * math.pi / count) * i
        x = center[0] + math.cos(angle) * radius
        z = center[1] + math.sin(angle) * radius

        rocks.append(create_rock((x, 0, z), scale=1.0))

    return rocks


def scatter_clouds(count=6, radius=25, height=25):
    clouds = []

    for i in range(count):
        angle = (2 * math.pi / count) * i
        x = math.cos(angle) * radius
        z = math.sin(angle) * radius

        clouds.append(create_cloud((x, height, z)))

    return clouds


def place_buildings():
    return [
        create_building((-7, 0, -12)),
        create_building((-15, 0, -8)),
        create_building((-3, 0, -10)),
        create_building((8, 0, -5)),
        create_building((10, 0, -15)),
        create_building((6, 0, -10)),
    ]


#Builds a full procedural scene with ground, buildings, rocks, clouds, and a sun, then applies colors and combines all objects.
def build_scene():
    cmds.file(new=True, force=True)

    ground = create_ground(width=60, depth=60)

    rocks = scatter_rocks()
    buildings = place_buildings()
    clouds = scatter_clouds()

    sun = create_sun()
    rays = create_sun_rays()
    sun_group = [sun] + rays

    circle_rocks = [
        create_rock((math.cos(i)*6, 0, math.sin(i)*6), scale=0.8)
        for i in [j * (2*math.pi/8) for j in range(8)]
    ]


#fixing errors

    apply_color(ground, (0.3, 0.8, 0.3))

    # ALL rocks colored (FIXED)
    color_all(rocks, (0.5, 0.5, 0.5))
    color_all(circle_rocks, (0.5, 0.5, 0.5))

    # ALL buildings colored (FIXED)
    color_all(flatten(buildings), (0.55, 0.75, 0.95))

    # ALL clouds colored (FIXED)
    color_all(flatten(clouds), (1.0, 1.0, 1.0))

    # Sun body
    apply_color(sun, (1.0, 0.9, 0.2))

    # ALL rays colored (FIXED)
    color_all(rays, (1.0, 0.6, 0.1))

    # ONLY ONE ray highlighted differently
    apply_color(rays[0], (1.0, 0.2, 0.0))

#Final Output
    all_objects = (
        [ground]
        + rocks
        + circle_rocks
        + flatten(buildings)
        + flatten(clouds)
        + sun_group
    )

    print("Total objects:", len(all_objects))
    cmds.viewFit(allObjects=True)
    print("Scene built successfully!")


# RUN
build_scene()

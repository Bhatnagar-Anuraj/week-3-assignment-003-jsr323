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
import random




# Function Library

#Creates a green groud plane, places it, and returns it.
def create_ground(name="ground", width=50, depth=50, position=(0, 0, 0)):
    """Create a ground plane in Maya and return its name.

    Args:
        name: The name to assign to the ground plane object.
        width: The width of the ground plane along the X axis.
        depth: The depth of the ground plane along the Z axis.
        position: A tuple (x, y, z) for where to place the plane.

    Returns:
        The string name of the created ground plane object.
    """
    ground = cmds.polyPlane(name=name, w=width, h=depth)[0]
    cmds.move(position[0], position[1], position[2], ground)
    return ground

#Creats a building, places it and returns it.
def create_building(name="building", position=(0, 0, 0), scale=1.0):
    """Create a building made of a base cube and a roof cube.

    Args:
        name: The base name used to label the building parts.
        position: A tuple (x, y, z) for the building's center position.
        scale: A float that uniformly scales the building's size.

    Returns:
        A list containing the string names of the base and roof objects.
    """
    base = cmds.polyCube(name=f"{name}_base", w=4*scale, h=6*scale, d=4*scale)[0]
    roof = cmds.polyCube(name=f"{name}_roof", w=4.5*scale, h=2*scale, d=4.5*scale)[0]

    cmds.move(position[0], position[1] + 3*scale, position[2], base)
    cmds.move(position[0], position[1] + 7*scale, position[2], roof)

    return [base, roof]

#Creats a scaled rock, places it and returns it.
def create_rock(position=(0, 0, 0), scale=1.0):
    """Create a flattened sphere to represent a rock at a given position.

    Args:
        position: A tuple (x, y, z) for where to place the rock.
        scale: A float that controls the overall size of the rock.

    Returns:
        The string name of the created rock object.
    """
    rock = cmds.polySphere(r=1 * scale, name="rock")[0]
    cmds.scale(scale, scale * 0.6, scale, rock)
    cmds.move(position[0], position[1], position[2], rock)
    return rock

#Creates and scatters cloud clusters, places it and returns it
def create_cloud(position=(0, 10, 0), scale=1.0):
    """Create a cloud made of three overlapping spheres.

    Args:
        position: A tuple (x, y, z) for the starting position of the cloud.
        scale: A float that controls the size of each sphere in the cloud.

    Returns:
        A list of string names for all sphere objects that make up the cloud.
    """
    parts = []
    for i in range(3):
        cloud_part = cmds.polySphere(r=1 * scale, name=f"cloud_{i}")[0]
        cmds.move(position[0] + i * scale, position[1], position[2], cloud_part)
        parts.append(cloud_part)
    return parts

#Creats a sun sphere with orbiting rays arranged around it procedurally, places it and returns it
def create_sun(position=(0, 30, 0), scale=3.0):
    """Create a large sphere to represent the sun.

    Args:
        position: A tuple (x, y, z) for where to place the sun.
        scale: A float that controls the radius of the sun sphere.

    Returns:
        The string name of the created sun sphere object.
    """
    sun = cmds.polySphere(r=2 * scale, name="sun")[0]
    cmds.move(position[0], position[1], position[2], sun)
    return sun


def create_sun_rays(count=8, radius=6, position=(0, 30, 0)):
    """Create small cubes arranged in a circle to represent sun rays.

    Args:
        count: The number of rays to create around the sun.
        radius: The distance from the sun's center to each ray.
        position: A tuple (x, y, z) matching the sun's position.

    Returns:
        A list of string names for all ray cube objects.
    """
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
    """Create a Lambert shader with the given RGB color and apply it to an object.

    Args:
        obj: The string name of the Maya object to shade.
        color: A tuple of three floats (r, g, b) each in the range 0.0 to 1.0.

    Returns:
        The string name of the created Lambert shader node.
    """
    shader = cmds.shadingNode('lambert', asShader=True)
    cmds.setAttr(shader + ".color", *color, type="double3")

    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)
    cmds.connectAttr(shader + ".outColor", sg + ".surfaceShader")
    cmds.sets(obj, edit=True, forceElement=sg)
    return shader


def flatten(items):
    """Flatten a nested list of Maya object names into a single flat list.

    Uses cmds.ls to verify each object exists in the scene before including it.

    Args:
        items: A list that may contain strings or nested lists of strings.

    Returns:
        A flat list of string object names that exist in the Maya scene.
    """
    result = []
    for i in items:
        if isinstance(i, list):
            result.extend(i)
        else:
            result.append(i)
    # Use cmds.ls to confirm objects exist in scene
    return cmds.ls(result)


def color_all(objects, color):
    """Apply the same color shader to every object in a list.

    Args:
        objects: A list of string Maya object names to colorize.
        color: A tuple of three floats (r, g, b) each in the range 0.0 to 1.0.

    Returns:
        A list of string names of all objects that had color applied,
        as confirmed by cmds.ls.
    """
    for obj in objects:
        apply_color(obj, color)
    return cmds.ls(objects)

#Creates and randomly scatters rocks, buildings, and clouds around the center point with various different sizes
def scatter_rocks(count=6, spread=20):
    """Randomly scatter rocks across the ground within a given area.

    Args:
        count: The number of rocks to create.
        spread: The maximum distance from center (x and z) rocks can appear.

    Returns:
        A list of string names for all created rock objects.
    """
    rocks = []
    for _ in range(count):
        x = random.uniform(-spread, spread)
        z = random.uniform(-spread, spread)
        scale = random.uniform(0.5, 1.5)
        rock = create_rock(position=(x, 0, z), scale=scale)
        rocks.append(rock)
    return rocks


def place_buildings(count=4, spread=15):
    """Place buildings at random positions across the scene.

    Args:
        count: The number of buildings to create.
        spread: The maximum distance from center (x and z) buildings can appear.

    Returns:
        A list of lists, where each inner list contains the base and roof
        object names for one building.
    """
    buildings = []
    for i in range(count):
        x = random.uniform(-spread, spread)
        z = random.uniform(-spread, spread)
        scale = random.uniform(0.8, 1.5)
        building = create_building(name=f"building_{i}", position=(x, 0, z), scale=scale)
        buildings.append(building)
    return buildings


def scatter_clouds(count=4, spread=15, height=15):
    """Create and scatter cloud clusters at a given height across the scene.

    Args:
        count: The number of cloud clusters to create.
        spread: The maximum distance from center (x and z) clouds can appear.
        height: The Y position at which clouds are placed.

    Returns:
        A list of lists, where each inner list contains the sphere names
        for one cloud cluster.
    """
    clouds = []
    for _ in range(count):
        x = random.uniform(-spread, spread)
        z = random.uniform(-spread, spread)
        scale = random.uniform(0.8, 1.4)
        cloud = create_cloud(position=(x, height, z), scale=scale)
        clouds.append(cloud)
    return clouds

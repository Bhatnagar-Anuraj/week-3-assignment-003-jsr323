"""
DIGM 131 - Assignment 3: Function Library (main_scene.py)
==========================================================

OBJECTIVE:
    Use the functions you wrote in scene_functions.py to build a complete
    scene. This file demonstrates how importing and reusing functions makes
    scene creation clean and readable.

REQUIREMENTS:
    1. Import scene_functions (the module you completed).
    2. Call each of your 5+ functions at least once.
    3. Use place_in_circle with at least one of your create functions.
    4. The final scene should contain at least 15 objects total.
    5. Comment your code explaining what you are building.

GRADING CRITERIA:
    - [30%] All 5+ functions from scene_functions.py are called.
    - [25%] place_in_circle is used at least once.
    - [20%] Scene contains 15+ objects and looks intentional.
    - [15%] Code is well-commented.
    - [10%] Script runs without errors from top to bottom.
"""

import maya.cmds as cmds
import math

cmds.file(new=True, force=True)

# Function Library

#Creates a green groud plane, places it, and returns it.
def create_ground(x=0, z=0, width=50, depth=50):
    """Create and shade a ground plane. Returns the ground node name."""
    ground = cmds.polyPlane(width=width, height=depth, name="ground")[0]
    shader = cmds.shadingNode("lambert", asShader=True, name="groundShader")
    cmds.setAttr(shader + ".color", 0.20, 0.30, 0.20, type="double3")
    cmds.select(ground)
    cmds.hyperShade(assign=shader)
    cmds.move(x, 0, z, ground)
    return ground

#Creats a building, places it and returns it.
def create_building(x, z, width=2.0, height=6.0, depth=2.0):
    """Create a single building at (x, z)."""
    building = cmds.polyCube(
        width=width,
        height=height,
        depth=depth,
        name="Building")[0]
    cmds.move(x, height / 2.0, z, building)
    return building

#Creats a scaled rock, places it and returns it.
def create_rock(x, z, scale=1.0):
    """Create a rock at (x, z)."""
    rock = cmds.polySphere(radius=1.0, name="rock")[0]
    cmds.scale(scale, scale * 0.7, scale, rock)
    cmds.move(x, scale / 2.0, z, rock)
    return rock

#Creates and scatters cloud clusters, places it and returns it
def create_cloud(x, y, z, scale=1.5):
    """Create a cloud made of oval spheres."""
    parts = []

    offsets = [
        (0, 0, 0),
        (1.2 * scale, 0.2 * scale, 0),
        (-1.2 * scale, 0.1 * scale, 0.8 * scale)]

    for ox, oy, oz in offsets:
        cloud = cmds.polySphere(radius=1.0, name="cloud")[0]
        cmds.scale(scale * 1.5, scale * 0.8, scale * 1.2, cloud)
        cmds.move(x + ox, y + oy, z + oz, cloud)
        parts.append(cloud)

    return parts


def scatter_clouds(count=6, area=25, height=30):
    clouds = []

    for i in range(count):
        angle = math.sin(i * 9.123) * 1000.0
        x = math.sin(angle) * area
        z = math.cos(angle * 1.3) * area
        y = height + (math.sin(i) * 3)

        clouds.extend(create_cloud(x, y, z, scale=1.5))

    return clouds

#Creats a sun sphere with orbiting rays arranged around it procedurally, places it and returns it
def create_sun(x, y, z, radius=6):
    """Create the main sun sphere."""
    sun = cmds.polySphere(radius=radius, name="sun")[0]
    cmds.move(x, y, z, sun)
    return sun


def create_sun_ray(sun_x, sun_y, sun_z, direction, scale=1.0):
    """Create a sun ray."""
    ray = cmds.polyCone(radius=0.5, height=2.5, name="sunray")[0]

    cmds.rotate(90, 0, 0, ray, relative=True)
    cmds.scale(scale, scale * 2.0, scale, ray)

    x = sun_x + direction[0]
    y = sun_y + direction[1]
    z = sun_z + direction[2]

    cmds.move(x, y, z, ray)
    cmds.delete(ray, constructionHistory=True)

    return ray


def build_sun(center_x=0, center_y=40, center_z=-40, ray_count=14):
    elements = []

    sun = create_sun(center_x, center_y, center_z, radius=6)
    elements.append(sun)

    for i in range(ray_count):
        angle = (2 * math.pi / ray_count) * i
        radius = 10

        dx = math.cos(angle) * radius
        dz = math.sin(angle) * radius
        dy = math.sin(angle * 2.0) * 3.0

        ray = create_sun_ray(
            center_x,
            center_y,
            center_z,
            direction=(dx, dy, dz),
            scale=1.0)

        elements.append(ray)

    return elements

#creates a lambert shader and applies a given RGB color
def apply_color(nodes, r, g, b, shader_name="shader"):
    shader = cmds.shadingNode("lambert", asShader=True, name=shader_name)
    cmds.setAttr(shader + ".color", r, g, b, type="double3")

    for n in nodes:
        cmds.select(n)
        cmds.hyperShade(assign=shader)

    return shader
    
#Creates and randomly scatters rocks around the center point with various different sizes
def scatter_rocks(center_x, center_z, count=20, spread=10.0):
    rocks = []

    for i in range(count):
        angle = math.sin(i * 12.9898) * 43758.5453
        x_offset = math.sin(angle) * spread
        z_offset = math.cos(angle * 1.7) * spread

        x = center_x + x_offset
        z = center_z + z_offset

        scale = 0.5 + (math.sin(i * 3.1) * 0.5 + 0.5)
        rocks.append(create_rock(x, z, scale))

    return rocks

#Places objects evenly in a circle around a center point
#I had AI help with the math
def place_in_circle(create_func, count, radius, center_x=0, center_z=0):
    results = []

    for i in range(count):
        angle = (2 * math.pi / count) * i
        x = center_x + math.cos(angle) * radius
        z = center_z + math.sin(angle) * radius

        results.append(create_func(x, z))

    return results

#Builds a full procedural scene with ground, buildings, rocks, clouds, and a sun, then applies colors and combines all objects.
def build_scene():
    global ground

    ground = create_ground(width=60, depth=60)

    rocks = scatter_rocks(0, 0, count=25, spread=12)

    buildings_left = [
        create_building(-7, -12, width=3.5, height=10, depth=3.5),
        create_building(-15, -8, width=4.0, height=12, depth=4.0),
        create_building(-3, -10, width=3.2, height=9, depth=3.2)]

    buildings_right = [
        create_building(8, -5, width=3.5, height=11, depth=3.5),
        create_building(10, -15, width=4.5, height=14, depth=4.5),
        create_building(6, -10, width=3.8, height=10, depth=3.8)]

    all_buildings = buildings_left + buildings_right
    apply_color(all_buildings, 0.55, 0.75, 0.95, shader_name="buildingBlue")

    circle_rocks = place_in_circle(
        lambda x, z: create_rock(x, z, scale=0.8),
        count=8,
        radius=6,
        center_x=0,
        center_z=5)

    clouds = scatter_clouds(count=6, area=20, height=25)
    apply_color(clouds, 1.0, 1.0, 1.0, shader_name="cloudWhite")

    sun_elements = build_sun(center_x=0, center_y=45, center_z=-45, ray_count=14)
    apply_color(sun_elements, 1.0, 0.9, 0.2, shader_name="sunYellow")

    all_objects = (
        [ground]
        + rocks
        + all_buildings
        + circle_rocks
        + clouds
        + sun_elements)
        
#Builds the full scene, fits the camera to view all objects, and prints a completion message.
    print("Total objects:", len(all_objects))
    cmds.viewFit(allObjects=True)
    print("Sunny scene built successfully!")


ground = create_ground()
build_scene()

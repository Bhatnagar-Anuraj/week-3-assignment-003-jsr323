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
 
# Import all reusable functions from our scene function library
from scene_functions import (
    create_ground,
    create_building,
    create_rock,
    create_cloud,
    create_sun,
    create_sun_rays,
    apply_color,
    flatten,
    color_all,
    scatter_rocks,
    place_buildings,
    scatter_clouds,
    place_in_circle,
)
 
 
def build_scene():
    """Build a complete Maya scene using imported scene functions.
 
    Constructs a town-like environment with a ground plane, scattered
    buildings, rocks, clouds, a sun with rays, and a ceremonial ring
    of rocks placed using place_in_circle.
 
    Returns:
        A list of string names of every object created in the scene.
    """
 
    # clearing scene
    cmds.file(new=True, force=True)
 
    # Create a large green ground plane for base of the scene
    ground = create_ground(name="ground", width=60, depth=60, position=(0, 0, 0))
 
    # Scatter 4 randomly placed buildings around the scene
    buildings = place_buildings(count=4, spread=15)
 
    # Add one large landmark building at the center-back of the scene
    landmark = create_building(name="landmark", position=(0, 0, -10), scale=1.8)
 
    # Scatter random rocks across the ground for detail
    rocks = scatter_rocks(count=6, spread=20)
 
    # Place 8 rocks in a ceremonial ring around the center landmark
    # using place_in_circle for clean procedural placement
    circle_rocks = place_in_circle(
        create_func=create_rock,
        count=8,
        radius=6,
        y=0,
        func_kwargs={"scale": 0.8}
    )
 
    # Scatter cloud clusters high in the sky
    clouds = scatter_clouds(count=4, spread=18, height=18)
 
    # Place the sun in the upper-left area of the sky
    sun = create_sun(position=(-15, 30, -15), scale=3.0)
 
    # Create rays radiating outward from the sun's position
    rays = create_sun_rays(count=8, radius=6, position=(-15, 30, -15))
 
    #Adding color to objects
 
    # Ground - bright green
    apply_color(ground, (0.2, 0.7, 0.2))
 
    # All scattered and circle rocks - grey stone color
    color_all(rocks, (0.75, 0.75, 0.75))
    color_all(circle_rocks, (0.6, 0.6, 0.6))
 
    # All building parts (flattened from nested lists) - light blue
    color_all(flatten(buildings), (0.55, 0.75, 0.95))
 
    # Landmark building - a slightly warmer tan to stand out
    color_all(landmark, (0.9, 0.8, 0.6))
 
    # Clouds - white
    color_all(flatten(clouds), (1.0, 1.0, 1.0))
 
    # Sun - bright yellow
    apply_color(sun, (1.0, 0.9, 0.2))
 
    # Rays - orange, with the first ray highlighted in red
    color_all(rays, (1.0, 0.6, 0.1))
    apply_color(rays[0], (1.0, 0.2, 0.0))
 
    # Compile all objects and build the scene
 
    all_objects = (
        [ground]
        + flatten(buildings)
        + landmark
        + rocks
        + circle_rocks
        + flatten(clouds)
        + [sun]
        + rays
    )
 
    print(f"Total objects in scene: {len(all_objects)}")
    cmds.viewFit(allObjects=True)
    print("Scene built successfully!")
 
    return all_objects
 
 
# Run the scene builder when this script is run directly
build_scene()

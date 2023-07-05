import sys

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

import planning_parser

DELAY_CONSTRUCTION = 0.08


app = Ursina()

# Entity.default_shader = lit_with_shadows_shader
ground = Entity(
    model="plane", collider="box", scale=64, texture="grass", texture_scale=(4, 4), y=-1
)
Sky()


class Voxel(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
            model="cube",
            origin_y=0.5,
            texture="white_cube",
            color=color.color(0, 0, random.uniform(0.9, 1.0)),
            highlight_color=color.lime,
        )


player = FirstPersonController(z=-5, x=-5)
editor_camera = EditorCamera(enabled=False)

world = {}


def input(key):
    if key == "left mouse down":
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
            Voxel(position=hit_info.entity.position + hit_info.normal)
    if key == "right mouse down" and mouse.hovered_entity:
        destroy(mouse.hovered_entity)

    if key == "e":
        if not editor_camera.enabled:
            editor_camera.enable()
        else:
            editor_camera.disable()


def apply_action(a):
    action, location, block = a
    if action == planning_parser.PLACE_BLOCK:
        world[location] = Voxel(position=location)
    if action == planning_parser.REMOVE_BLOCK:
        if location in world:
            destroy(world[location])
            del world[location]
        else:
            print(f"Error: bock at {location} not found in world!")


def init_world(hddl_filename: str):
    for predicate, location, block in planning_parser.parse_world(hddl_filename):
        if predicate == planning_parser.BLOCKAT:
            world[location] = Voxel(position=location)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <filename>")
        print(f"Example: {sys.argv[0]} out/p-9-9-9-10.out")
        print("\nError: filename is required")
        exit(1)

    init_world(f"in/{sys.argv[1].rsplit('/', 1)[1].split('.out')[0]}.hddl")

    for index, action in enumerate(planning_parser.parse_actions(sys.argv[1])):
        invoke(apply_action, action, delay=index * DELAY_CONSTRUCTION)

    app.run()

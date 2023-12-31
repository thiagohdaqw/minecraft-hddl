import sys
import pathlib

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

import planning_parser

DELAY_CONSTRUCTION = 0.09


app = Ursina()

window.fullscreen = True
window.title = "Minecraft HDDL"

Entity.default_shader = lit_with_shadows_shader
ground = Entity(
    model="plane",
    collider="box",
    scale=64,
    texture="textures/grass.jpg",
    texture_scale=(64, 64),
    y=-1,
)
Sky()



class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture=None):
        super().__init__(
            parent=scene,
            position=position,
            model="cube",
            origin_y=0.5,
            texture="white_cube" if texture is None else texture,
            color=color.color(0, 0, random.uniform(0.9, 1.0)),
            highlight_color=color.lime,
        )


player = FirstPersonController(z=-10)
arm = Entity(
    parent=camera.ui,
    model="cube",
    color=color.blue,
    position=(0.75, -0.6),
    rotation=(150, -10, 6),
    scale=(0.2, 0.2, 2),
)
editor_camera = EditorCamera(enabled=False)

world = {}

textures = {
    "stone": "textures/stone.png",
    "earth": "textures/earth.png",
    "wood": "textures/wood.png",
}


def input(key):
    if key == "left mouse down":
        hit_info = raycast(camera.world_position, camera.forward, distance=10)
        if hit_info.hit:
            Voxel(
                position=hit_info.entity.position + hit_info.normal,
                texture=textures["wood"],
            )
    if (
        key == "right mouse down"
        and mouse.hovered_entity
        and mouse.hovered_entity != ground
    ):
        destroy(mouse.hovered_entity)

    if key == "e":
        if not editor_camera.enabled:
            editor_camera.enable()
        else:
            editor_camera.disable()


def update():
    if held_keys["left mouse"]:
        arm.position = (0.6, -0.5)
    elif held_keys["right mouse"]:
        arm.position = (0.6, -0.5)
    else:
        arm.position = (0.75, -0.6)


def add_block(location, block):
    world[location] = Voxel(position=location, texture=textures.get(block, None))


def apply_action(a):
    action, location, block = a
    if action == planning_parser.PLACE_BLOCK:
        add_block(location, block)
    if action == planning_parser.REMOVE_BLOCK:
        if location in world:
            destroy(world[location])
            del world[location]
        else:
            print(f"Error: bock at {location} not found in world!")


def init_world(hddl_filepath: pathlib.Path):
    for predicate, location, block in planning_parser.parse_world(hddl_filepath):
        if predicate == planning_parser.BLOCKAT:
            add_block(location, block)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <filename>")
        print(f"Example: {sys.argv[0]} out/p-9-9-9-10.out")
        print("\nError: filename is required")
        exit(1)

    path = pathlib.Path(sys.argv[1])
    filename = path.stem
    init_world(path.parent / ".." / "in" / f"{filename}.hddl")

    for index, action in enumerate(planning_parser.parse_actions(path)):
        invoke(apply_action, action, delay=index * DELAY_CONSTRUCTION)

    app.run()

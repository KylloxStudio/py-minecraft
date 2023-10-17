from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

jump_height = 1.5 # Default: 2
jump_duration = 0.5 # Default: 0.5
jump_fall_after = 0.05 # Default: 0.35
gravity_scale = 1.25 # Default: 1
mouse_sensitivity = Vec2(50,50) # Default: (40,40)
run_speed = 7.5 # Default: 5

window.fps_counter.enabled = False
window.exit_button.visible = False
mouse.visible = False

#cursor =  Cursor(
#    model=Mesh(
#        vertices=[(-.5,0,0),(.5,0,0),(0,-.5,0),(0,.5,0)],
#        triangles=[(0,1),(2,3)],
#        mode='line',
#        thickness=2
#    ),
#    scale=0.02
#)

punch = Audio('assets/punch', autoplay=False)

cube = Entity(
    model='cube',
    color=color.blue,
    texture='white_cube',
    position=Vec3(10, 5, 5),
    scale=2
)

blocks = [
    load_texture('assets/grass.png'), # 0
    load_texture('assets/grass.png'), # 1
    load_texture('assets/stone.png'), # 2
    load_texture('assets/gold.png'),  # 3
    load_texture('assets/lava.png'),  # 4
]

block_id = 1

def input(key):
    global block_id, hand
    if key.isdigit():
        block_id = int(key)
        if block_id >= len(blocks):
            block_id = len(blocks) - 1
        hand.texture = blocks[block_id]

sky = Entity(
    parent=scene,
    model='sphere',
    texture=load_texture('assets/sky.jpg'),
    scale=500,
    double_sided=True
)

hand = Entity(
    parent=camera.ui,
    model='assets/block',
    texture=blocks[block_id],
    scale=0.2,
    rotation=Vec3(-10, -10, 10),
    position=Vec2(0.6, -0.6)
)

def update():
    if held_keys['left mouse'] or held_keys['right mouse']:
        punch.play()
        hand.position = Vec2(0.4, -0.5)
    else:
        hand.position = Vec2(0.6, -0.6)
    cube.rotation_x = cube.rotation_x + 0.25
    cube.rotation_y = cube.rotation_y + 0.5

class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture='assets/grass.png'):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1.0)),
            scale=0.5
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                destroy(self)
            elif key == 'right mouse down':
                Voxel(position=self.position + mouse.normal, texture=blocks[block_id])

for z in range(20):
    for x in range(20):
        voxel = Voxel(position=(x, 0, z))

player = FirstPersonController()

player.jump_height = jump_height
player.jump_up_duration = jump_duration
player.mouse_sensitivity = mouse_sensitivity
player.speed = run_speed
player.gravity = gravity_scale

app.run()

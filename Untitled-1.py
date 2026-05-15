from ursina.prefabs.first_person_controller import FirstPersonController

player = FirstPersonController(
    position=(0,3,0),
    speed=6
)
player.cursor.visible = False

# third person camera
camera.parent = player
camera.position = (0, 6, -12)
camera.rotation_x = 20
camera.fov = 90

# ---------- LIGHT ----------
Sky()
sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))
AmbientLight(color=color.rgba(170,170,170,1))

# ---------- MAP ----------
ground = Entity(
    model='plane',
    scale=(180,1,180),
    texture='white_cube',
    texture_scale=(90,90),
    color=color.rgb(70,170,70),
    collider='box'
)

# Buildings
for _ in range(30):
    h = random.randint(5,18)
    Entity(
        model='cube',
        position=(random.randint(-75,75), h/2, random.randint(-75,75)),
        scale=(random.randint(4,10), h, random.randint(4,10)),
        color=color.gray,
        collider='box'
    )

# Trees
for _ in range(60):
    x = random.randint(-80,80)
    z = random.randint(-80,80)
    Entity(model='cube', scale=(0.7,5,0.7), position=(x,2.5,z), color=color.brown)
    Entity(model='sphere', scale=3, position=(x,6,z), color=color.green)

# Rocks
for _ in range(35):
    Entity(
        model='sphere',
        scale=random.uniform(1,3),
        position=(random.randint(-80,80),1,random.randint(-80,80)),
        color=color.dark_gray,
        collider='box'
    )

# ---------- PLAYER ----------
player = ThirdPersonController(
    position=(0,3,0),
    speed=6,
    jump_height=3
)
player.health = 100

# Real model fallback
player_model_name = 'player.glb' if os.path.exists('player.glb') else 'cube'
player_visual = Entity(
    parent=player,
    model=player_model_name,
    scale=1 if player_model_name != 'cube' else (1.2,2,1.2),
    color=color.azure if player_model_name == 'cube' else color.white,
    position=(0,-1,0)
)

# Gun
gun = Entity(
    parent=camera.ui,
    model='cube',
    scale=(.18,.10,.8),
    position=(.55,-.35),
    rotation=(15,-20,0),
    color=color.black
)

# Crosshair
Text("+", origin=(0,0), scale=2)

# ---------- LOOT ----------
loot_boxes = []
for _ in range(12):
    box = Entity(
        model='cube',
        color=color.yellow,
        scale=1,
        position=(random.randint(-70,70),1,random.randint(-70,70)),
        collider='box'
    )
    loot_boxes.append(box)

# ---------- ENEMIES ----------
enemies = []

class Enemy(Entity):
    def __init__(self):
        super().__init__(
            position=(random.randint(-70,70),1,random.randint(-70,70)),
            collider='box'
        )

        model_name = 'enemy.glb' if os.path.exists('enemy.glb') else 'cube'

        self.visual = Entity(
            parent=self,
            model=model_name,
            scale=1 if model_name != 'cube' else (1.2,2,1.2),
            color=color.red if model_name == 'cube' else color.white
        )

        self.health = 100
        self.speed = random.uniform(2.5,4.5)

    def update(self):
        d = distance(self, player)

        if d < 45:
            self.look_at(player.position)
            self.position += self.forward * time.dt * self.speed

        if d < 2:
            player.health -= 15 * time.dt

for _ in range(15):
    enemies.append(Enemy())

# ---------- ZONE ----------
zone = Entity(
    model='sphere',
    scale=140,
    color=color.rgba(0,100,255,35),
    wireframe=True
)
zone_radius = 70

# ---------- UI ----------
health_text = Text("", position=(-.87,.45), scale=1.5)
enemy_text = Text("", position=(-.87,.40), scale=1.5)
loot_text = Text("", position=(-.87,.35), scale=1.5)

# ---------- SHOOT ----------
def shoot():
    hit = raycast(camera.world_position, camera.forward, distance=120)

    gun.position = (.48,-.38)
    invoke(setattr, gun, 'position', (.55,-.35), delay=.08)

    if hit.hit:
        Entity(
            model='sphere',
            color=color.yellow,
            scale=.2,
            position=hit.world_point,
            lifetime=.15
        )

        for e in enemies[:]:
            if hit.entity == e or hit.entity.parent == e:
                e.health -= 50
                if e.health <= 0:
                    enemies.remove(e)
                    destroy(e)

def input(key):
    global sun

    if key == 'left mouse down':
        shoot()

    # Sprint
    if key == 'left shift':
        player.speed = 12
    if key == 'left shift up':
        player.speed = 6

    # Day/Night
    if key == 'n':
        AmbientLight(color=color.rgba(
            random.randint(40,200),
            random.randint(40,200),
            random.randint(40,200),
            1
        ))

# ---------- UPDATE ----------
def update():
    global zone_radius

    # Loot pickup
    for box in loot_boxes[:]:
        if distance(player, box) < 2:
            player.health = min(100, player.health + 25)
            loot_boxes.remove(box)
            destroy(box)

    # Zone shrink
    if zone_radius > 12:
        zone_radius -= time.dt * 0.25
        zone.scale = zone_radius * 2

    dist = math.sqrt(player.x**2 + player.z**2)
    if dist > zone_radius:
        player.health -= 7 * time.dt

    # UI
    health_text.text = f"Health: {int(player.health)}"
    enemy_text.text = f"Enemies: {len(enemies)}"
    loot_text.text = f"Loot: {len(loot_boxes)}"

    # End game
    if player.health <= 0:
        Text("GAME OVER", origin=(0,0), scale=4, color=color.red)
        application.pause()

    if len(enemies) == 0:
        Text("YOU WIN!", origin=(0,0), scale=4, color=color.yellow)
        application.pause()

app.run()
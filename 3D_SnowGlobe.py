from numpy.ma.core import angle
from vpython import *
from random import uniform
from time import *

scene = canvas(title="Snow Globe", width=800, height=600)
scene.background = vector(0.2, 0.15, 0.3)  # Deep indigo
globe = sphere(pos=vector(0, 0, 0), radius=6.8, color=color.white, opacity=0.2)

# Shadow effect (slightly larger semi-transparent sphere around the main globe)
shadow_glow = sphere(pos=vector(0, 0, 0), radius=7.1, color=color.cyan, opacity=0.1)

# Add light
dlight = local_light(pos=vector(0, 5, 0), color=color.blue)

# Crescent Moon setup
moon = sphere(pos=vector(3, 4, 0), radius=0.5, color=color.white, emissive=True)  # Main body of the moon

# Shadow sphere to create the crescent effect
shadow = sphere(pos=vector(3.2, 4, 0), radius=0.5, color=scene.background, emissive=True, opacity=0)  # Slightly offset to cut into the moon

# Moon glow light
moon_glow = distant_light(direction=vector(-3, -3, 0), color=color.white)  # Light from the crescent moon

#label(pos=vector(0, 2, 0), text='Happy Holidays!', height=20, color=color.white, box=False, opacity=0)

# Function to create a stand for the snow globe
def create_stand():
    # Base of the stand (wide, flat cylinder)
    base = cylinder(pos=vector(0, -7, 0), axis=vector(0, 0.5, 0), radius=4.5, color=vector(0.65,0.33,0.16)) #color=vector(0.65,0.33,0.16)
    # Column of the stand (tall, narrow cylinder)
    column = cylinder(pos=vector(0, -6.5, 0), axis=vector(0, 1, 0), radius=3.5, color=vector(0.65,0.33,0.16)) #color=vector(0.65,0.33,0.16)

# Function to create a larger snowman with visible features
def create_snowman(x, z):
    # Snowman body (3 spheres of increasing size)
    bottom = sphere(pos=vector(x, -2.2, z), radius=1.2, color=color.white)  # Larger bottom
    middle = sphere(pos=vector(x, -0.6, z), radius=0.9, color=color.white)   # Larger middle
    head = sphere(pos=vector(x, 0.4, z), radius=0.6, color=color.white)      # Larger head

    # Eyes (increase size and adjust position)
    eye1 = sphere(pos=vector(x - 0.2, 0.6, z + 0.45), radius=0.1, color=color.black)
    eye2 = sphere(pos=vector(x + 0.2, 0.6, z + 0.45), radius=0.1, color=color.black)

    # Nose (larger and adjusted for new head size)
    nose = cone(pos=vector(x, 0.4, z + 0.6), axis=vector(0, 0, 0.3), radius=0.1, color=color.orange)

    # Buttons (small black spheres on the middle part)
    button1 = sphere(pos=vector(x, -0.4, z + 0.9), radius=0.1, color=color.black)
    button2 = sphere(pos=vector(x, -0.8, z + 0.9), radius=0.1, color=color.black)

    # Hat (larger size for the base and top)
    hat_base = cylinder(pos=vector(x, 0.8, z), axis=vector(0, 0.15, 0), radius=0.6, color=color.black)
    hat_top = box(pos=vector(x, 1, z), size=vector(0.7, 0.45, 0.7), color=color.black)

# Function to create snowflakes
def create_snowflakes(num_flakes):
    snowflakes = []
    for _ in range(num_flakes):
        x = uniform(-4.5, 4.5)
        y = uniform(2, 4)  # Start above the snowman
        z = uniform(-4.5, 4.5)
        snowflake = sphere(pos=vector(x, y, z), radius=0.05, color=color.white, opacity=0.8, emissive=True)
        snowflakes.append(snowflake)
    return snowflakes

# Function to animate snowflakes
def animate_snowflakes(snowflakes):
    while True:
        rate(50)  # Increase the rate for smoother animation
        for snowflake in snowflakes:
            snowflake.pos.y -= 0.1
            if snowflake.pos.y < -3:
                snowflake.pos.y = uniform(2, 4)
                snowflake.pos.x = uniform(-4.5, 4.5)
                snowflake.pos.z = uniform(-4.5, 4.5)

# Function to create a larger snow pile, limited to the sphere radius
def create_large_snow_pile(x, y, z, layers=3, num_spheres=20, base_radius=0.4):
    for layer in range(layers):
        for i in range(num_spheres):
            # Randomize the position slightly within each layer to keep it inside the sphere
            pos_x = x + uniform(-1.0, 1.0) * (layers - layer) * 0.3
            pos_y = y + layer * base_radius * 0.5
            pos_z = z + uniform(-1.0, 1.0) * (layers - layer) * 0.3

            # Ensure the snow pile is within the sphere's radius
            if pos_x**2 + pos_y**2 + pos_z**2 < 6.5**2:  # 6.5 is the radius of the globe
                snow_clump = sphere(pos=vector(pos_x, pos_y, pos_z), radius=uniform(base_radius * 0.8, base_radius * 1.2),
                                    color=color.white, opacity=0.9)

# Function to create a larger pine tree
def create_pine_tree(x, z):
    # Tree trunk
    trunk = cylinder(pos=vector(x, -3.2, z), axis=vector(0, 0.6, 0), radius=0.15, color=vector(0.55, 0.27, 0.07))

    # Tree foliage (3 layers of cones with larger sizes)
    foliage1 = cone(pos=vector(x, -2.6, z), axis=vector(0, 0.7, 0), radius=0.8, color=color.green)
    foliage2 = cone(pos=vector(x, -2.0, z), axis=vector(0, 0.6, 0), radius=0.6, color=color.green)
    foliage3 = cone(pos=vector(x, -1.5, z), axis=vector(0, 0.5, 0), radius=0.4, color=color.green)


# Updated function to create a larger gift box
def create_gift(x, y, z, gift_color, ribbon_color):
    # Make the gift box larger
    gift_box = box(pos=vector(x, y, z), size=vector(0.6, 0.6, 0.6), color=gift_color)

    # Larger ribbon (adjusted size to match gift box)
    ribbon_horizontal = cylinder(pos=vector(x, y + 0.3, z - 0.3), axis=vector(0, 0, 0.6), radius=0.07, color=ribbon_color)
    ribbon_vertical = cylinder(pos=vector(x - 0.3, y + 0.3, z), axis=vector(0.6, 0, 0), radius=0.07, color=ribbon_color)

# New positions to place gifts closer to each other, forming a bunch
create_gift(-0.6, -2.6, -1.2, color.red, color.yellow)    # Red gift with yellow ribbon
create_gift(0, -2.6, -0.8, color.blue, color.white)       # Blue gift with white ribbon
create_gift(0.6, -2.6, -0.4, color.green, color.red)      # Green gift with red ribbon

# Position for the bottom snow pile
create_large_snow_pile(0, -5, 0, layers=5, num_spheres=50, base_radius=0.8)
create_large_snow_pile(1, -5, 0, layers=4, num_spheres=50, base_radius=0.8)
create_large_snow_pile(-2.5, -5, -1, layers=4, num_spheres=40, base_radius=0.8)
create_large_snow_pile(-2, -5, -1, layers=4, num_spheres=40, base_radius=0.8)
create_large_snow_pile(-3, -5, -2, layers=4, num_spheres=40, base_radius=0.8)
create_large_snow_pile(2.5, -5, -1, layers=4, num_spheres=40, base_radius=0.8)
create_large_snow_pile(-2, -5, 1, layers=3, num_spheres=40, base_radius=0.8)
create_large_snow_pile(-2, -5, 0, layers=4, num_spheres=40, base_radius=0.8)
create_large_snow_pile(-2.7, -4.70, 1, layers=5, num_spheres=35, base_radius=0.8)
create_large_snow_pile(3, -5, -2, layers=4, num_spheres=40, base_radius=0.8)
create_large_snow_pile(3, -4.6, 1.5, layers=4, num_spheres=30, base_radius=0.8)
create_large_snow_pile(0, -4.85, 2, layers=4, num_spheres=30, base_radius=0.8)

# Arrange pine trees
create_pine_tree(-4, -2)
create_pine_tree(-2, -3)
create_pine_tree(-1, -2.5)
create_pine_tree(1.5, -3)
create_pine_tree(3, -1)
create_pine_tree(4, -2)

#stand for snow globe
create_stand()

# Add a snowman inside the snow globe
create_snowman(-1.5, -2.5)

# Add snowflakes and store them in a variable
snowflakes = create_snowflakes(200)

# Start animating the snowflakes
animate_snowflakes(snowflakes)

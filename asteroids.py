# program template for Spaceship
# Wait for soundtrack to load(if it doesn't). Awesome stuff.
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://i.space.com/images/i/000/023/673/wS1/vista-look-at-helix-nebula-1600.jpg?1352931499")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("https://ia801703.us.archive.org/15/items/StarWarsThemeSongByJohnWilliams/Star%20Wars%20Theme%20Song%20By%20John%20Williams.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group(canvas, group):
    for sprite in set(group):
        sprite.draw(canvas)
        sprite.update()
        if sprite.update():
            group.remove(sprite)
        
def group_collide(group, other_object):
    global collide_flag
    collisions = 0
    remove_set = set([])
    for sprite in set(group):
        if sprite.collide(other_object):
            remove_set.add(sprite)
            collisions += 1
            explosion = Sprite(sprite.get_pos(),[0, 0], 0, 0, explosion_image,
                                explosion_info, explosion_sound)
            explosion_group.add(explosion)
    group.difference_update(remove_set)
    return collisions

def group_group_collide(rocks, missiles):
    collision_counter = 0
    for rock in set(rocks):
        if group_collide(missiles, rock):
            collision_counter += 1
            rocks.discard(rock)
    return collision_counter
        
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
        
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def anticlock(self):
        self.angle_vel -= 0.07
        
    def clock(self):
        self.angle_vel += 0.07
    
    def zeroanvel(self):
        self.angle_vel = 0
        
    def thruster(self, thrust):
        self.thrust = thrust
        if self.thrust == True:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
        
    def draw(self,canvas):
        global ship_image, ship_info
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        if self.thrust == True:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(ship_image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
            
    def update(self):
        c = 0.02
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel
        self.vel[0] *= (1 - c)
        self.vel[1] *= (1 - c)
        forward = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += forward[0]*0.3
            self.vel[1] += forward[1]*0.3
            
        if self.pos[0] < 0:
            self.pos[0] = 800
        elif self.pos[0] > 800:
            self.pos[0] = 0
        if self.pos[1] < 0:
            self.pos[1] = 600
        elif self.pos[1] > 600:
            self.pos[1] = 0
            
    def shoot(self):
        global missile_group
        missile_center = [self.pos[0] + angle_to_vector(self.angle)[0]*45, 
                          self.pos[1] + angle_to_vector(self.angle)[1]*45]
        missile_vel = [self.vel[0] + 10*angle_to_vector(self.angle)[0],
                       self.vel[1] + 10*angle_to_vector(self.angle)[1]]
        missile = Sprite(missile_center, missile_vel, 
                           0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(missile)

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.init_vel = [vel[0], vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        
        if sound:
            sound.rewind()
            sound.play()
            
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def draw(self, canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + (self.age * self.image_size[0]), self.image_center[1]], self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel
        if self.pos[0] < 0:
            self.pos[0] = 800
        elif self.pos[0] > 800:
            self.pos[0] = 0
        if self.pos[1] < 0:
            self.pos[1] = 600
        elif self.pos[1] > 600:
            self.pos[1] = 0
        self.age += 1
        if self.age > self.lifespan:
            return True
        else:
            return False
        if self.animated == True:
            self.image_center[0] += self.image_size[1]
            
    def collide(self, other_object):
        if dist(self.pos, other_object.get_pos()) <= (self.radius + other_object.get_radius()):
            return True
        else:
            return False
            
def draw(canvas):
    global time, score, lives, started, rock_group, missile_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    for rock in rock_group:
        for i in range(2):
            rock.vel[i] = rock.init_vel[i] + rock.init_vel[i]*0.05

    # draw ship and sprites
    my_ship.draw(canvas)
    
    if group_collide(rock_group, my_ship):
        lives = lives - 1
    score += group_group_collide(rock_group, missile_group)*10
    
    if lives == 0:
        rock_group = set([])
        started = False
    
    canvas.draw_text('Lives: ', [20, 50], 40, 'White')
    canvas.draw_text(str(lives), [130, 50], 40, 'White')
    
    canvas.draw_text('Score:', [600, 50], 40, 'White')
    canvas.draw_text(str(score), [720, 50], 40, 'White')
    
    # update ship and sprites
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)
    process_sprite_group(canvas, explosion_group)
    my_ship.update()
    
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    
def keydown(key):
    
    if key == simplegui.KEY_MAP['left']:
        my_ship.anticlock()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.clock()
    
    if key == simplegui.KEY_MAP['up']:
        my_ship.thruster(True)
        
    if key == simplegui.KEY_MAP['space']:
         my_ship.shoot()
        
def keyup(key):
    
    if key == simplegui.KEY_MAP['left']:
        my_ship.zeroanvel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.zeroanvel()
    
    if key == simplegui.KEY_MAP['up']:
        my_ship.thruster(False)
    
def click(pos):
    global started, lives, score, soundtrack
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0
        soundtrack.rewind()
        soundtrack.play()
    
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, started
    if len(rock_group) > 12 or not started:
        return
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
    rock_avel = random.random() * .2 - .1
    rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
    rock_group.add(rock)
    if dist(rock_pos, my_ship.pos) < 100:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_keyup_handler(keyup)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()

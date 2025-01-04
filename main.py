import pygame, random, json

wall_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

pygame.init()

width, height = 816, 576
ekran = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()
fps = 60

class Wall():
    def __init__(self, x, y, en, boy):        
        self.rect = pygame.Rect(x, y, en, boy)

    def draw(self):
        pygame.draw.rect(ekran, (244, 122, 122), self.rect)

class SnowBall():
    def __init__(self, x, y, radius, color, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)

    def move(self):
        self.y += self.speed
        self.rect.y = int(self.y)

        if self.y - self.radius > height:
            self.y = -self.radius
            self.x = random.randint(0, width)
            self.rect.x = self.x - self.radius

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.y = -self.radius
                self.x = random.randint(0, width)
                self.rect.x = self.x - self.radius

    def draw(self):
        pygame.draw.circle(ekran, self.color, (int(self.x), int(self.y)), self.radius)

class Map():
    def __init__(self, x, y):        
        self.image = pygame.image.load('smap.png')
        self.rect = pygame.Rect(x, y, 2240, 2240)

    def draw(self):
        ekran.blit(self.image, self.rect)

class Particle():
    def __init__(self, x, y, radius, color, lifetime):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.lifetime = lifetime

    def update(self):
        self.lifetime -= 1
        self.radius *= 0.95

    def draw(self, ekran):
        if self.lifetime > 0:
            pygame.draw.circle(ekran, self.color, (int(self.x), int(self.y)), int(self.radius))

class Player():
    def __init__(self, x, y, radius, color, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        self.min_radius = 5
        self.gravity = 0.5  
        self.velocity_y = 0
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.jumping = False 
        self.particles = []

    def move(self, walls):
        global score
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_LEFT]:
            dx -= self.speed
            self.shrink()
            self.create_particle()
        if keys[pygame.K_RIGHT]:
            dx += self.speed
            self.shrink()
            self.create_particle()
        
        if keys[pygame.K_SPACE] and not self.jumping or keys[pygame.K_UP] and not self.jumping : 
            self.velocity_y = -10
            self.jumping = True 

        self.velocity_y += self.gravity
        dy += self.velocity_y

        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: 
                    self.rect.right = wall.rect.left
                if dx < 0:  
                    self.rect.left = wall.rect.right

        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dy > 0:  
                    self.rect.bottom = wall.rect.top
                    self.velocity_y = 0
                    self.jumping = False 
                if dy < 0:  
                    self.rect.top = wall.rect.bottom
                    self.velocity_y = 0

        if self.rect.x <= 0:
            self.rect.left = 0
        if self.rect.right >= width:
            self.rect.right = width

        for snowball in snowballs:
          if self.rect.colliderect(snowball.rect):
            self.radius += 2
            score += 5
            self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
            snowball.y = -snowball.radius
            snowball.x = random.randint(0, width)
            snowball.rect.x = snowball.x - snowball.radius

        for stoneball in stoneballs:
          if self.rect.colliderect(stoneball.rect):
            self.radius -= 4
            score -= 5
            self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
            stoneball.y = -stoneball.radius
            stoneball.x = random.randint(0, width)
            stoneball.rect.x = stoneball.x - stoneball.radius

        self.x, self.y = self.rect.center
        
    def die(self):
        global die
        if self.radius <= self.min_radius:
            text = pygame.font.Font('Limelight-Regular.ttf',70).render('Game Over',True,(0,0,0))
            ekran.blit(text,(width//2-200,170))
            die = 1

    def create_particle(self):
        particle = Particle(self.x, self.y + self.radius, random.randint(3, 7), (255, 255, 255), random.randint(20, 40))
        self.particles.append(particle)

    def shrink(self):
        if self.radius > self.min_radius:
            self.radius -= 0.1
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def draw(self):
        pygame.draw.circle(ekran, self.color, (int(self.x), int(self.y)), int(self.radius))
    
    def update(self, walls):
        self.move(walls)
        self.draw()
        self.die()

        for particle in self.particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                self.particles.remove(particle)
            else:
                particle.draw(ekran)

def create_walls(wall_map):
    walls = []
    cell_size = 48
    for y, row in enumerate(wall_map):
        for x, value in enumerate(row):
            if value == 1: 
                wall = Wall(x * cell_size, y * cell_size, cell_size, cell_size)
                walls.append(wall)
    return walls

player = Player(width // 2, height // 2, 35, (255, 255, 255), 5)
walls = create_walls(wall_map)
map = Map(0,48)
bg = pygame.image.load('sbg.png')
snowballs = [SnowBall(random.randint(20, width-20), random.randint(-50, 0), random.randint(9, 18), (240, 240, 255), random.randint(2,3)) for _ in range(5)]
stoneballs = [SnowBall(random.randint(20, width-20), random.randint(-50, 0), random.randint(9, 18), (89, 101, 105), random.randint(2,3)) for _ in range(3)]

score = 0
die = 0

running = True
try:
    with open('score.txt') as score_file:
        scorex = json.load(score_file)
except (FileNotFoundError, json.JSONDecodeError):
    scorex = {'score': 0}  

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if score > scorex['score']:
        scorex['score'] = score
        with open('score.txt', 'w') as score_file:
            json.dump(scorex, score_file)

    ekran.blit(bg,(0,0))
    map.draw()
    if die == 0:
        text2 = pygame.font.Font('Limelight-Regular.ttf', 40).render(f'Best score: {scorex["score"]}', True, (0, 0, 0))
        text = pygame.font.Font('Limelight-Regular.ttf',40).render(f'Score:{score}',True,(0,0,0))
        ekran.blit(text,(10,10))
        ekran.blit(text2,(10,60))
        for snowball in snowballs:
            snowball.move()
            snowball.draw()
        for stoneball in stoneballs:
            stoneball.move()
            stoneball.draw()
        player.update(walls)
    else:
        text3 = pygame.font.Font('Limelight-Regular.ttf',50).render(f'You Score:{score}',True,(0,0,0))
        ekran.blit(text3,(width//2-160,270))
        player.die()
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
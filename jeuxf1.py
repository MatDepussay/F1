import math
from dataclasses import dataclass

import pygame

@dataclass
class Car:
    x: float
    y: float
    angle: float
    speed: float

@dataclass
class Track:
    width: int
    height: int



pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

track = Track(400, 300)
car = Car(400, 200, 0, 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # background
    screen.fill((30, 30, 30))

    # track shape (rectangle)
    track_rect_ext = pygame.Rect(
        (800 - track.width) // 2,
        (600 - track.height) // 2,
        track.width,
        track.height,
    )
    

    track_rect_int = pygame.Rect(0, 0, track.width // 2, track.height // 2)
    
    track_rect_int.center = track_rect_ext.center
    
    pygame.draw.ellipse(screen, (255, 0, 0), track_rect_ext)
    pygame.draw.ellipse(screen, (30, 30, 30), track_rect_int)
    
    pygame.draw.circle(screen, (0, 220, 0), (int(car.x), int(car.y)), 12)
    
    pygame.display.flip()
    
    if pygame.key.get_pressed()[pygame.K_UP]:
        car.speed += 0.1
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        car.speed -= 0.1
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        car.angle -= 2
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        car.angle += 2

    car.x += math.cos(math.radians(car.angle)) * 0.1*car.speed
    car.y += math.sin(math.radians(car.angle)) * 0.1*car.speed


pygame.quit()
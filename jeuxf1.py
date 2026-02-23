import math
from dataclasses import dataclass

import pygame

@dataclass
class Car:
    x: float
    y: float
    angle: float
    speed: float
    max_speed: float = 5.0

@dataclass
class Track:
    width: int
    height: int
    center_x: int
    center_y: int



pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

track = Track(400, 300, center_x=400, center_y=300)
car = Car(400, 200, 0, 0, 5.0)

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
    
    rayon_x_ext = track.width // 2
    rayon_y_ext = track.height // 2
    center_x, center_y = track_rect_ext.center
    
    track_rect_int = pygame.Rect(0, 0, rayon_x_ext, rayon_y_ext)
    track_rect_int.center = track_rect_ext.center
    rayon_x_int = rayon_x_ext // 2
    rayon_y_int = rayon_y_ext // 2
    
    car_depart = car.x, car.y
    lenght_sens = 20
    pts_arrive_x = car.x + math.cos(math.radians(car.angle)) * lenght_sens
    pts_arrive_y = car.y + math.sin(math.radians(car.angle)) * lenght_sens

    
    pygame.draw.ellipse(screen, (255, 0, 0), track_rect_ext)
    pygame.draw.ellipse(screen, (30, 30, 30), track_rect_int)

    pygame.draw.circle(screen, (0, 220, 0), (int(car.x), int(car.y)), 12)
    pygame.draw.line(screen, (0, 255, 0), car_depart, (pts_arrive_x, pts_arrive_y), 2)
    pygame.display.flip()
    
    if pygame.key.get_pressed()[pygame.K_UP]:
        car.speed += 0.03
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        car.speed -= 0.03
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        car.angle -= 0.5
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        car.angle += 0.5
    if not pygame.key.get_pressed()[pygame.K_UP] and not pygame.key.get_pressed()[pygame.K_DOWN]:
        car.speed *= 0.95
    if car.speed > car.max_speed:
        car.speed = car.max_speed
    prev_x, prev_y = car.x, car.y
            
    car.x += math.cos(math.radians(car.angle)) * 0.1*car.speed
    car.y += math.sin(math.radians(car.angle)) * 0.1*car.speed
    
    if ((car.x - center_x)/ rayon_x_ext)**2 + ((car.y - center_y)/ rayon_y_ext)**2 > 1:
        car.speed = 0
        car.x = prev_x
        car.y = prev_y
    if ((car.x - center_x)/ rayon_x_int)**2 + ((car.y - center_y)/ rayon_y_int)**2 < 1:
        car.speed = 0
        car.x = prev_x
        car.y = prev_y


pygame.quit()
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

@dataclass
class Sensor:
    car_depart: tuple
    pts_arrive_x: float
    pts_arrive_y: float
    touched: bool = False


def calculate_track_rects(track):
    """Calcule les rectangles et rayons du circuit"""
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
    
    return track_rect_ext, track_rect_int, rayon_x_ext, rayon_y_ext, rayon_x_int, rayon_y_int, center_x, center_y


def calculate_sensors(car, sensor_length=20):
    """Calcule les 5 capteurs autour de la voiture"""
    angles = [-40, -20, 0, 20, 40]
    sensors = []
    
    for angle_offset in angles:
        real_angle = car.angle + angle_offset
        pts_x = car.x + math.cos(math.radians(real_angle)) * sensor_length
        pts_y = car.y + math.sin(math.radians(real_angle)) * sensor_length
        sensor = Sensor((car.x, car.y), pts_x, pts_y)
        sensors.append(sensor)
    
    return sensors


def check_sensors_collision(sensors, center_x, center_y, rayon_x_ext, rayon_y_ext, rayon_x_int, rayon_y_int):
    """Vérifie si les capteurs touchent les bords"""
    for sensor in sensors:
        # Vérifie si le point d'arrivée est dehors l'ellipse externe
        outside_ext = ((sensor.pts_arrive_x - center_x) / rayon_x_ext)**2 + ((sensor.pts_arrive_y - center_y) / rayon_y_ext)**2 > 1
        
        # Vérifie si le point d'arrivée est dedans l'ellipse interne
        inside_int = ((sensor.pts_arrive_x - center_x) / rayon_x_int)**2 + ((sensor.pts_arrive_y - center_y) / rayon_y_int)**2 < 1
        
        sensor.touched = outside_ext or inside_int


def check_car_collision(car, center_x, center_y, rayon_x_ext, rayon_y_ext, rayon_x_int, rayon_y_int):
    """Vérifie si la voiture sort du circuit et la replace"""
    prev_x, prev_y = car.x, car.y
    
    car.x += math.cos(math.radians(car.angle)) * 0.1 * car.speed
    car.y += math.sin(math.radians(car.angle)) * 0.1 * car.speed
    
    # Dehors l'ellipse externe
    if ((car.x - center_x) / rayon_x_ext)**2 + ((car.y - center_y) / rayon_y_ext)**2 > 1:
        car.speed = 0
        car.x = prev_x
        car.y = prev_y
    
    # Dedans l'ellipse interne
    if ((car.x - center_x) / rayon_x_int)**2 + ((car.y - center_y) / rayon_y_int)**2 < 1:
        car.speed = 0
        car.x = prev_x
        car.y = prev_y


def handle_car_input(car):
    """Gère les entrées clavier pour la voiture"""
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP]:
        car.speed += 0.03
    if keys[pygame.K_DOWN]:
        car.speed -= 0.03
    if keys[pygame.K_LEFT]:
        car.angle -= 0.5
    if keys[pygame.K_RIGHT]:
        car.angle += 0.5
    
    # Friction
    if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
        car.speed *= 0.95
    
    # Limite de vitesse
    if car.speed > car.max_speed:
        car.speed = car.max_speed


def draw_game(screen, track_rect_ext, track_rect_int, car, sensors):
    """Dessine tous les éléments du jeu"""
    screen.fill((30, 30, 30))
    
    # Track
    pygame.draw.ellipse(screen, (255, 0, 0), track_rect_ext)
    pygame.draw.ellipse(screen, (30, 30, 30), track_rect_int)
    
    # Sensors
    for sensor in sensors:
        color = (255, 0, 0) if sensor.touched else (0, 255, 0)
        pygame.draw.line(screen, color, sensor.car_depart, (sensor.pts_arrive_x, sensor.pts_arrive_y), 2)
    
    # Voiture
    pygame.draw.circle(screen, (0, 220, 0), (int(car.x), int(car.y)), 12)
    
    pygame.display.flip()


# Main game loop
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
    
    # Calculs
    track_rect_ext, track_rect_int, rayon_x_ext, rayon_y_ext, rayon_x_int, rayon_y_int, center_x, center_y = calculate_track_rects(track)
    sensors = calculate_sensors(car)
    
    # Logique
    handle_car_input(car)
    check_sensors_collision(sensors, center_x, center_y, rayon_x_ext, rayon_y_ext, rayon_x_int, rayon_y_int)
    check_car_collision(car, center_x, center_y, rayon_x_ext, rayon_y_ext, rayon_x_int, rayon_y_int)
    
    # Affichage
    draw_game(screen, track_rect_ext, track_rect_int, car, sensors)
    
    clock.tick(60)

pygame.quit()
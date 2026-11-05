"""
A simple radar simulation using fuzzy logic
Authors: Mateusz Aftanas, Nikifor Koseda

The program simulates moving objects on a radar
Each object receives a threat score calculated using
the Sugeno fuzzy inference method

The system uses three inputs:
- Distance from radar center (km)
- Object speed (m/s)
- Movement angle (degrees)

The output is a threat score between 0 and 100.

To run, install the libraries from requirements.txt
and execute main.py with Python
"""

import pygame
import math
from objects import radar_objects, status_colors, create_object, update_objects

pygame.init()

background  = pygame.Color("#030306")
darkgray    = pygame.Color("#03070C")
gray        = pygame.Color("#26282b")
lightgray   = pygame.Color("#4b4e53")
white       = pygame.Color("#FFFFFF")

H2    = pygame.font.SysFont("consolas", 14)
H3    = pygame.font.SysFont("consolas", 14)
H4    = pygame.font.SysFont("consolas", 12)
H5    = pygame.font.SysFont("consolas", 10)

degree_label = H2.render("°", True, gray)

screen  = pygame.display.set_mode((840, 800))

pygame.display.set_caption("Air Defense Threat Assessment System")

clock = pygame.time.Clock()
running = True

spawn_interval_seconds = 1
spawn_elapsed_seconds = spawn_interval_seconds
time_scale = 20

# Main simulation loop
while running:
    elapsed_seconds = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update object positions and generate new objects
    update_objects(radar_objects, elapsed_seconds * time_scale)
    spawn_elapsed_seconds += elapsed_seconds

    if spawn_elapsed_seconds >= spawn_interval_seconds:
        radar_objects.append(create_object())
        spawn_elapsed_seconds = 0

    screen.fill(background) # BACKGROUND

    # Draw the radar background, range circles and grid
    pygame.draw.circle(screen, darkgray, (420, 400), 350, 0) # RADAR BACKGROUND
    pygame.draw.circle(screen, lightgray, (420, 400), 353, 3) # RADIUS - Frame

    #pygame.draw.circle(screen, gray, (420, 400), 350, 2) # RADIUS - 100 KM
    pygame.draw.circle(screen, gray, (420, 400), 280, 1) # RADIUS - 80 KM
    pygame.draw.circle(screen, gray, (420, 400), 210, 1) # RADIUS - 60 KM
    pygame.draw.circle(screen, gray, (420, 400), 140, 1) # RADIUS - 40 KM
    pygame.draw.circle(screen, gray, (420, 400), 70,  1) # RADIUS - 20 KM

    # Draw angle lines and labels around the radar
    for angle_degrees in range(0, 360, 30):
        angle_radians = math.radians(angle_degrees)

        x = 420 + 350 * math.sin(angle_radians)
        y = 400 - 350 * math.cos(angle_radians)

        pygame.draw.line(screen, gray, (420, 400), (x, y), 1)

        angle_label = H2.render(str(angle_degrees), True, lightgray)

        x = 420 + 375 * math.sin(angle_radians)
        y = 400 - 375 * math.cos(angle_radians)

        angle_rect = angle_label.get_rect(center=(x, y))

        if angle_degrees > 180:
            angle_rect.x -= degree_label.get_width()

        screen.blit(angle_label, angle_rect)
        screen.blit(degree_label, (angle_rect.right, angle_rect.top))

    for distance_km in range(20, 101, 20):
        radius_pixels = distance_km * 3.5

        distance_label = H3.render(f"{distance_km}", True, gray)
        distance_rect = distance_label.get_rect(topright=(420 + radius_pixels - 5, 405))

        screen.blit(distance_label, distance_rect)

    # Draw detected objects using colors based on their threat levels
    for radar_object in radar_objects:
        x = radar_object["x"]
        y = radar_object["y"]
        status = radar_object["status"]
        object_color = status_colors[status]

        if status in ("mid", "high", "critical"):
            polygon_points = [ # Romb
                (x, y - 10), # (lewy brzeg)
                (x + 10, y), # (górny brzeg)
                (x, y + 10), # (szerokość)
                (x - 10, y), # (wysokość)
            ]
        else:
            triangle_height = 20 * math.sqrt(3) / 2
            polygon_points = [ # Trójkąt
                (x, y - 2 * triangle_height / 3),
                (x + 10, y + triangle_height / 3),
                (x - 10, y + triangle_height / 3),
            ]

        pygame.draw.polygon(
            screen,
            object_color,
            polygon_points,
            width = 2 # grubość
        )

        # Display object ID, threat score, distance and speed
        if radar_object["status"] != "player":
            distance_pixels = math.hypot(x - 420, y - 400)
            distance_km = distance_pixels * 100 / 350

            score_text = "N/A"
            if radar_object["score"] is not None:
                score_text = f"{radar_object['score']:.0f}" # ".0f" zaokrąglanie scoringu do liczby całkowitej

            header_label = H4.render(
                f"{radar_object['id']} - {score_text}",
                True,
                background
            )

            header_rect = pygame.Rect(
                x + 22,
                y - 16,
                header_label.get_width() + 12,
                header_label.get_height() + 2,
            )

            pygame.draw.rect(screen, object_color, header_rect)
            screen.blit(header_label, (header_rect.x + 6, header_rect.y + 4))

            distance_label = H4.render(f"{distance_km:.0f} km {radar_object['speed']:.0f} m/s", True, object_color)
            screen.blit(distance_label, (header_rect.x, header_rect.bottom + 4))
    
    pygame.display.flip()

pygame.quit()
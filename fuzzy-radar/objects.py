"""
Object generation and movement for the radar simulation

Objects are randomly generated and moved across the radar
Their threat scores are calculated using fuzzy.py
"""

import pygame
import math
import random
from itertools import count
from fuzzy import calc_threat_score, get_threat_status

object_ids = count(4000)

status_colors = {
    "player":   pygame.Color("#1FBBED"),
    "unknown":  pygame.Color("#858991"),
    "low":      pygame.Color("#1FED84"),
    "mid":      pygame.Color("#FAC642"),
    "high":     pygame.Color("#FA8142"),
    "critical": pygame.Color("#ED1F3B"),
}

radar_objects = []

def create_object():

    """
    Create a random object at the edge of the radar

    Returns:
    dict: Object with ID, position, speed, direction,
    threat score and status
    """

    angle_radians = random.uniform(0, 2 * math.pi)
    direction_radians = angle_radians + math.pi + random.uniform(-math.pi / 3, math.pi / 3)

    return {
        "id":   next(object_ids),
        "score": None,
        "status":   "unknown",
        "speed":    random.randint(400, 6000),
        "x": 420 + 350 * math.sin(angle_radians),
        "y": 400 - 350 * math.cos(angle_radians),
        "direction_radians": direction_radians,
    }

def update_objects(radar_objects, elapsed_seconds):

    """
    Update object positions and calculate threat scores

    Parameters:
    radar_objects (list): List of radar objects
    elapsed_seconds (float): Simulation time since last update

    Returns:
    None: Objects are updated directly in the list
    """

    for radar_object in radar_objects.copy():
        step_pixels = radar_object["speed"] * elapsed_seconds * 350 / 100000
        direction_radians = radar_object["direction_radians"]

        radar_object["x"] += math.sin(direction_radians) * step_pixels
        radar_object["y"] -= math.cos(direction_radians) * step_pixels

        dx = 420 - radar_object["x"]
        dy = 400 - radar_object["y"]
        distance_pixels = math.hypot(dx, dy)

        if distance_pixels > 350:
            radar_objects.remove(radar_object)
            continue

        distance_km = distance_pixels * 100 / 350
        angle_degree = 0

        if distance_pixels > 0:
            angle_cosine = (dx * math.sin(direction_radians) - dy * math.cos(direction_radians)) / distance_pixels

            angle_cosine = max(-1, min(1, angle_cosine))
            angle_degree = math.degrees(math.acos(angle_cosine))

        radar_object["score"] = calc_threat_score(distance_km, radar_object["speed"], angle_degree)
        radar_object["status"] = get_threat_status(radar_object["score"])
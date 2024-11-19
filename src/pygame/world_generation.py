import pygame
import random
import sys
import heapq

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 1000
TILE_SIZE = 20
WIDTH = SCREEN_WIDTH // TILE_SIZE
HEIGHT = SCREEN_HEIGHT // TILE_SIZE
MAX_ROOMS = 10
MIN_ROOMS = 6
ROOM_MIN_SIZE = 5
ROOM_MAX_SIZE = 15


def generate_dungeon():
    game_map = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
    rooms = []
    attempts = 0
    max_attempts = 200

    while len(rooms) < MIN_ROOMS and attempts < max_attempts:
        w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        x = random.randint(2, WIDTH - w - 2)
        y = random.randint(2, HEIGHT - h - 2)

        new_room = {"x1": x, "y1": y, "x2": x + w, "y2": y + h}
        overlap = any(
            new_room["x1"] - 2 <= room["x2"]
            and new_room["x2"] + 2 >= room["x1"]
            and new_room["y1"] - 2 <= room["y2"]
            and new_room["y2"] + 2 >= room["y1"]
            for room in rooms
        )

        if not overlap:
            rooms.append(new_room)
            for x in range(new_room["x1"], new_room["x2"]):
                for y in range(new_room["y1"], new_room["y2"]):
                    game_map[y][x] = "R"

        attempts += 1

    if len(rooms) < MIN_ROOMS:
        print("Not enough rooms were created. Please try again.")
        sys.exit()

    room_centers = [
        ((room["x1"] + room["x2"]) // 2, (room["y1"] + room["y2"]) // 2)
        for room in rooms
    ]

    connected_rooms = {room_centers[0]}
    edges = [
        (abs(cx1 - cx2) + abs(cy1 - cy2), (cx1, cy1), (cx2, cy2))
        for (cx1, cy1) in connected_rooms
        for (cx2, cy2) in room_centers
        if (cx1, cy1) != (cx2, cy2)
    ]
    heapq.heapify(edges)

    corridor_map = set()
    corridor_doors = {}

    while len(connected_rooms) < len(room_centers):
        cost, (cx1, cy1), (cx2, cy2) = heapq.heappop(edges)
        if (cx2, cy2) not in connected_rooms:
            connected_rooms.add((cx2, cy2))
            for cx3, cy3 in room_centers:
                if (cx3, cy3) not in connected_rooms:
                    heapq.heappush(
                        edges, (abs(cx2 - cx3) + abs(cy2 - cy3), (cx2, cy2), (cx3, cy3))
                    )

            corridor_segments = []
            if random.randint(0, 1) == 0:
                for x in range(min(cx1, cx2), max(cx1, cx2) + 1):
                    if game_map[cy1][x] == " ":
                        corridor_segments.append((x, cy1))
                for y in range(min(cy1, cy2), max(cy1, cy2) + 1):
                    if game_map[y][cx2] == " ":
                        corridor_segments.append((cx2, y))
            else:
                for y in range(min(cy1, cy2), max(cy1, cy2) + 1):
                    if game_map[y][cx1] == " ":
                        corridor_segments.append((cx1, y))
                for x in range(min(cx1, cx2), max(cx1, cx2) + 1):
                    if game_map[cy2][x] == " ":
                        corridor_segments.append((x, cy2))

            # Introduce deviations to make corridors less direct
            deviation_chance = 0.5  # 50% chance to add deviation
            for i in range(len(corridor_segments) - 1):
                if random.random() < deviation_chance:
                    deviation_length = random.randint(1, 3)
                    direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
                    for _ in range(deviation_length):
                        last_segment = corridor_segments[-1]
                        new_segment = (
                            last_segment[0] + direction[0],
                            last_segment[1] + direction[1],
                        )
                        if (
                            0 <= new_segment[0] < WIDTH
                            and 0 <= new_segment[1] < HEIGHT
                            and game_map[new_segment[1]][new_segment[0]] == " "
                        ):
                            corridor_segments.append(new_segment)
                        else:
                            break

            if len(corridor_segments) >= 3:
                for x, y in corridor_segments:
                    game_map[y][x] = "."
                    corridor_map.add((x, y))
                    corridor_doors[(x, y)] = 0

    for room in rooms:
        room_connected = False
        for x in range(room["x1"] - 1, room["x2"] + 1):
            for y in range(room["y1"] - 1, room["y2"] + 1):
                if game_map[y][x] == ".":
                    room_connected = True
                    break
            if room_connected:
                break

        if not room_connected:
            room_center = (
                (room["x1"] + room["x2"]) // 2,
                (room["y1"] + room["y2"]) // 2,
            )
            closest_corridor = min(
                corridor_map,
                key=lambda c: abs(c[0] - room_center[0]) + abs(c[1] - room_center[1]),
            )
            cx, cy = closest_corridor

            if random.randint(0, 1) == 0:
                for x in range(min(cx, room_center[0]), max(cx, room_center[0]) + 1):
                    if game_map[cy][x] == " ":
                        game_map[cy][x] = "."
                for y in range(min(cy, room_center[1]), max(cy, room_center[1]) + 1):
                    if game_map[y][room_center[0]] == " ":
                        game_map[y][room_center[0]] = "."
            else:
                for y in range(min(cy, room_center[1]), max(cy, room_center[1]) + 1):
                    if game_map[y][cx] == " ":
                        game_map[y][cx] = "."
                for x in range(min(cx, room_center[0]), max(cx, room_center[0]) + 1):
                    if game_map[room_center[1]][x] == " ":
                        game_map[room_center[1]][x] = "."

    for room in rooms:
        room_perimeter = set()
        for x in range(room["x1"] - 2, room["x2"] + 2):
            for y in range(room["y1"] - 2, room["y2"] + 2):
                if game_map[y][x] == ".":
                    room_perimeter.add((x, y))

        corridor_entrances = []
        for cx, cy in room_perimeter:
            if (
                (cx > 0 and game_map[cy][cx - 1] == "R")
                or (cx < WIDTH - 1 and game_map[cy][cx + 1] == "R")
                or (cy > 0 and game_map[cy - 1][cx] == "R")
                or (cy < HEIGHT - 1 and game_map[cy + 1][cx] == "R")
            ):
                corridor_entrances.append((cx, cy))

        chosen_entrances = []
        corridor_to_room = {}
        for entrance in corridor_entrances:
            adjacent_corridors = [
                (ex, ey)
                for ex, ey in corridor_map
                if abs(ex - entrance[0]) <= 1 and abs(ey - entrance[1]) <= 1
            ]
            if not any(e in chosen_entrances for e in adjacent_corridors):
                chosen_entrances.append(entrance)
                for corridor in adjacent_corridors:
                    corridor_to_room[corridor] = room

        for entrance in chosen_entrances:
            if entrance not in corridor_doors:
                corridor_doors[entrance] = 0
            if (
                corridor_doors[entrance] < 1
            ):  # Ensure only one corridor tile touches room tiles
                corridor_doors[entrance] += 1
                game_map[entrance[1]][entrance[0]] = "D"

    entrance_room = rooms[0] if rooms else None
    if entrance_room:
        e_x = (entrance_room["x1"] + entrance_room["x2"]) // 2
        e_y = (entrance_room["y1"] + entrance_room["y2"]) // 2
        game_map[e_y][e_x] = "E"

    rooms_without_entrance = [room for room in rooms if room != entrance_room]
    selected_room_for_p = random.choice(rooms_without_entrance)

    while True:
        p_x = random.randint(
            selected_room_for_p["x1"] + 1, selected_room_for_p["x2"] - 1
        )
        p_y = random.randint(
            selected_room_for_p["y1"] + 1, selected_room_for_p["y2"] - 1
        )
        if game_map[p_y][p_x] == "R":
            game_map[p_y][p_x] = "P"
            break

    # Add dead ends
    for _ in range(random.randint(3, 6)):  # Random number of dead ends
        if corridor_map:
            dead_end_start = random.choice(list(corridor_map))
            # Ensure dead end start is at least one block away from any room
            while any(
                room["x1"] - 1 <= dead_end_start[0] <= room["x2"] + 1
                and room["y1"] - 1 <= dead_end_start[1] <= room["y2"] + 1
                for room in rooms
            ):
                dead_end_start = random.choice(list(corridor_map))

            dead_end_length = random.randint(2, 5)
            direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            for _ in range(dead_end_length):
                new_segment = (
                    dead_end_start[0] + direction[0],
                    dead_end_start[1] + direction[1],
                )
                if (
                    0 <= new_segment[0] < WIDTH
                    and 0 <= new_segment[1] < HEIGHT
                    and game_map[new_segment[1]][new_segment[0]] == " "
                ):
                    game_map[new_segment[1]][new_segment[0]] = "."
                    corridor_map.add(new_segment)
                    dead_end_start = new_segment
                else:
                    break

    return game_map, (e_x, e_y)

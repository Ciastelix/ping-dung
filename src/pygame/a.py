import pygame
import random
import sys
import heapq
from button import Button

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Tile settings

TILE_SIZE = 20
WIDTH = SCREEN_WIDTH // TILE_SIZE
HEIGHT = SCREEN_HEIGHT // TILE_SIZE
MAX_ROOMS = 10
MIN_ROOMS = 6  # Minimum number of rooms
ROOM_MIN_SIZE = 5
ROOM_MAX_SIZE = 15

# Load images
dirt_img = pygame.image.load("dirt.jpg")
grass_img = pygame.image.load("grass.jpeg")

# Scale images to tile size
dirt_img = pygame.transform.scale(dirt_img, (TILE_SIZE, TILE_SIZE))
grass_img = pygame.transform.scale(grass_img, (TILE_SIZE, TILE_SIZE))


def generate_dungeon():
    game_map = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
    rooms = []
    attempts = 0  # Counter to prevent infinite loops
    max_attempts = 200  # Maximum attempts to place rooms

    while len(rooms) < MIN_ROOMS and attempts < max_attempts:
        w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        x = random.randint(
            2, WIDTH - w - 2
        )  # Leave a 2-tile buffer on the left and right
        y = random.randint(
            2, HEIGHT - h - 2
        )  # Leave a 2-tile buffer on the top and bottom

        new_room = {"x1": x, "y1": y, "x2": x + w, "y2": y + h}
        overlap = False
        for room in rooms:
            if (
                new_room["x1"] - 1 <= room["x2"]
                and new_room["x2"] + 1 >= room["x1"]
                and new_room["y1"] - 1 <= room["y2"]
                and new_room["y2"] + 1 >= room["y1"]
            ):
                overlap = True
                break

        if not overlap:
            rooms.append(new_room)
            for x in range(new_room["x1"], new_room["x2"]):
                for y in range(new_room["y1"], new_room["y2"]):
                    game_map[y][x] = "R"  # Mark room tiles with "R"

        attempts += 1

    if len(rooms) < MIN_ROOMS:
        print("Not enough rooms were created. Please try again.")
        sys.exit()

    # Get the center points of all rooms
    room_centers = [
        ((room["x1"] + room["x2"]) // 2, (room["y1"] + room["y2"]) // 2)
        for room in rooms
    ]

    # Prim's algorithm to create a MST
    connected_rooms = {room_centers[0]}
    edges = [
        (abs(cx1 - cx2) + abs(cy1 - cy2), (cx1, cy1), (cx2, cy2))
        for (cx1, cy1) in connected_rooms
        for (cx2, cy2) in room_centers
        if (cx1, cy1) != (cx2, cy2)
    ]
    heapq.heapify(edges)

    while len(connected_rooms) < len(room_centers):
        cost, (cx1, cy1), (cx2, cy2) = heapq.heappop(edges)
        if (cx2, cy2) not in connected_rooms:
            connected_rooms.add((cx2, cy2))
            for cx3, cy3 in room_centers:
                if (cx3, cy3) not in connected_rooms:
                    heapq.heappush(
                        edges, (abs(cx2 - cx3) + abs(cy2 - cy3), (cx2, cy2), (cx3, cy3))
                    )

            # Create corridors
            if random.randint(0, 1) == 0:
                for x in range(min(cx1, cx2), max(cx1, cx2) + 1):
                    if game_map[cy1][x] == " ":
                        game_map[cy1][x] = "."
                for y in range(min(cy1, cy2), max(cy1, cy2) + 1):
                    if game_map[y][cx2] == " ":
                        game_map[y][cx2] = "."
            else:
                for y in range(min(cy1, cy2), max(cy1, cy2) + 1):
                    if game_map[y][cx1] == " ":
                        game_map[y][cx1] = "."
                for x in range(min(cx1, cx2), max(cx1, cx2) + 1):
                    if game_map[cy2][x] == " ":
                        game_map[cy2][x] = "."

    def is_adjacent_to_door(x, y):
        adjacent_tiles = [
            (x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
        ]
        return any(
            0 <= adj_x < WIDTH and 0 <= adj_y < HEIGHT and game_map[adj_y][adj_x] == "D"
            for adj_x, adj_y in adjacent_tiles
        )

    for room in rooms:
        room_doors = set()
        for x in range(room["x1"] - 1, room["x2"] + 2):
            for y in range(room["y1"] - 1, room["y2"] + 2):
                if game_map[y][x] == "R":
                    adjacent_corridors = [(0, -1), (0, 1), (-1, 0), (1, 0)]
                    for dx, dy in adjacent_corridors:
                        if game_map[y + dy][x + dx] == "." and not is_adjacent_to_door(
                            x, y
                        ):
                            if (x, y) not in room_doors:
                                game_map[y][x] = "D"
                                room_doors.add((x, y))
                            break

    entrance_room = rooms[0] if rooms else None
    if entrance_room:
        # Place the entrance in the center of the entrance room
        e_x = (entrance_room["x1"] + entrance_room["x2"]) // 2
        e_y = (entrance_room["y1"] + entrance_room["y2"]) // 2
        game_map[e_y][e_x] = "E"

    # Ensure "P" is not in the same room as "E"
    rooms_without_entrance = [room for room in rooms if room != entrance_room]
    selected_room_for_p = random.choice(rooms_without_entrance)

    while True:
        p_x = random.randint(
            selected_room_for_p["x1"] + 1, selected_room_for_p["x2"] - 1
        )
        p_y = random.randint(
            selected_room_for_p["y1"] + 1, selected_room_for_p["y2"] - 1
        )
        if (
            game_map[p_y][p_x] == "R"
        ):  # Ensure the position is inside the room and not a door
            game_map[p_y][p_x] = "P"
            break
    return game_map, (e_x, e_y)


def draw_dungeon(game_map):
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile == " ":
                pygame.draw.rect(screen, BLACK, rect)  # Empty space
            elif tile == "R":
                screen.blit(dirt_img, rect)  # Rooms with dirt image
            elif tile == ".":  # Corridors
                screen.blit(grass_img, rect)  # Corridors with grass image
            elif tile == "D":
                pygame.draw.rect(screen, BLACK, rect)  # Doors as black for now
            elif tile == "E":
                pygame.draw.rect(screen, GREEN, rect)  # Entrance in green
            elif tile == "P":
                pygame.draw.rect(screen, BLUE, rect)  # Player in blue


def main():
    clock = pygame.time.Clock()
    game_map, entrance_pos = generate_dungeon()

    play_button = pygame.image.load("play.png")

    play_button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, play_button)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(60)
        keys = pygame.key.get_pressed()

        screen.fill(BLACK)
        draw_dungeon(game_map)

        pygame.display.flip()
        play_button.draw(screen)


if __name__ == "__main__":
    main()

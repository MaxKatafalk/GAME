from settings import TILE_SIZE
from objects import GameObject, Tank
import pygame as pg

tiles = [
    pg.transform.scale(pg.image.load("Sprites/map/tileGrass1.png").convert(), (TILE_SIZE, TILE_SIZE)),
    pg.transform.scale(pg.image.load("Sprites/map/tileGrass2.png").convert(), (TILE_SIZE, TILE_SIZE)),
    pg.transform.scale(pg.image.load("Sprites/map/tileSand1.png").convert(), (TILE_SIZE, TILE_SIZE)),
    pg.transform.scale(pg.image.load("Sprites/map/tileSand2.png").convert(), (TILE_SIZE, TILE_SIZE)),
    pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadCrossing.png").convert(), (TILE_SIZE, TILE_SIZE)),
    pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadCornerLL.png").convert(), (TILE_SIZE, TILE_SIZE)),
    pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadCornerLR.png").convert(), (TILE_SIZE, TILE_SIZE)),
    pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadCornerUL.png").convert(), (TILE_SIZE, TILE_SIZE)),
    pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadCornerUR.png").convert(), (TILE_SIZE, TILE_SIZE)),
    pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadNorth.png").convert(), (TILE_SIZE, TILE_SIZE)),
    pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadEast.png").convert(), (TILE_SIZE, TILE_SIZE)),
    pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadTransitionE.png").convert(), (TILE_SIZE, TILE_SIZE)),
    pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadTransitionE_dirt.png").convert(), (TILE_SIZE, TILE_SIZE)),
    pg.transform.scale(pg.image.load("Sprites/map/tileSand_roadCornerLL.png").convert(), (TILE_SIZE, TILE_SIZE)),
    pg.transform.scale(pg.image.load("Sprites/map/tileSand_roadCornerLR.png").convert(), (TILE_SIZE, TILE_SIZE)),
    pg.transform.scale(pg.image.load("Sprites/map/tileSand_roadCornerUL.png").convert(), (TILE_SIZE, TILE_SIZE)),
    pg.transform.scale(pg.image.load("Sprites/map/tileSand_roadCornerUR.png").convert(), (TILE_SIZE, TILE_SIZE)),
    pg.transform.scale(pg.image.load("Sprites/map/tileSand_roadCrossing.png").convert(), (TILE_SIZE, TILE_SIZE)),
    pg.transform.scale(pg.image.load("Sprites/map/tileSand_roadNorth.png").convert(), (TILE_SIZE, TILE_SIZE)),
    pg.transform.scale(pg.image.load("Sprites/map/tileSand_roadEast.png").convert(), (TILE_SIZE, TILE_SIZE)),
    pg.transform.scale(pg.image.load("Sprites/map/tileGrass_transitionW1.png").convert(), (TILE_SIZE, TILE_SIZE)),
    pg.transform.scale(pg.image.load("Sprites/map/tileGrass_transitionW2.png").convert(), (TILE_SIZE, TILE_SIZE)),
    pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadSplitS.png").convert(), (TILE_SIZE, TILE_SIZE)),
    pg.transform.scale(pg.image.load("Sprites/map/tileSand_roadSplitS.png").convert(), (TILE_SIZE, TILE_SIZE)),
]

base_map_matrix1 = [
    [0, 9, 0, 6, 11, 19, 19, 13, 2],
    [10, 4, 10, 7, 21, 2, 3, 18, 2],
    [1, 9, 1, 0, 21, 2, 3, 18, 2],
    [0, 8, 22, 10, 12, 23, 19, 17, 19],
    [1, 0, 9, 1, 21, 18, 2, 18, 2]
]

base_map_matrix2 = [
    [2, 18, 2, 18, 20, 1, 9, 0, 1],
    [19, 17, 19, 15, 20, 1, 8, 5, 0],
    [2, 18, 3, 2, 20, 0, 1, 9, 1],
    [2, 18, 3, 2, 20, 6, 10, 4, 10],
    [2, 16, 19, 13, 20, 9, 0, 9, 0]
]

base_objects1 = [
    (200, 200, "Sprites/objects/treeGreen_twigs.png", 30, 30, False, False),
    (210, 500, "Sprites/objects/treeGreen_twigs.png", 30, 30, False, False),
    (1000, 200, "Sprites/objects/treeBrown_twigs.png", 30, 30, False, False),
    (1100, 700, "Sprites/objects/treeBrown_twigs.png", 30, 30, False, False),
    (210, 400, "Sprites/objects/treeGreen_small.png", 50, 50, True, False),
    (800, 890, "Sprites/objects/treeGreen_small.png", 50, 50, True, False),
    (150, 720, "Sprites/objects/treeGreen_small.png", 50, 50, True, False),
    (400, 600, "Sprites/objects/treeGreen_small.png", 50, 50, True, False),
    (1050, 500, "Sprites/objects/treeBrown_small.png", 50, 50, True, False),
    (1610, 450, "Sprites/objects/treeBrown_small.png", 50, 50, True, False),
    (1000, 500, "Sprites/objects/treeBrown_large.png", 100, 100, True, False),
    (1550, 400, "Sprites/objects/treeBrown_large.png", 100, 100, True, False),
    (100, 700, "Sprites/objects/treeGreen_large.png", 100, 100, True, False),
    (800, 820, "Sprites/objects/treeGreen_large.png", 100, 100, True, False),
    (1300, 500, "Sprites/objects/sandbagBrown.png", 40, 30, True, True),
    (1350, 600, "Sprites/objects/sandbagBrown.png", 40, 30, True, True),
    (1400, 500, "Sprites/objects/sandbagBrown.png", 40, 30, True, True),
    (1250, 600, "Sprites/objects/sandbagBrown.png", 40, 30, True, True),
    (1200, 500, "Sprites/objects/sandbagBrown.png", 40, 30, True, True),
    (600, 370, "Sprites/objects/sandbagBeige.png", 30, 40, True, True),
    (630, 410, "Sprites/objects/sandbagBeige.png", 30, 40, True, True),
    (660, 450, "Sprites/objects/sandbagBeige.png", 30, 40, True, True),
    (690, 490, "Sprites/objects/sandbagBeige.png", 30, 40, True, True),
    (600, 700, "Sprites/objects/crateMetal.png", 40, 40, True, True),
    (650, 670, "Sprites/objects/crateMetal.png", 40, 40, True, True),
    (640, 770, "Sprites/objects/crateMetal.png", 40, 40, True, True),
    (1500, 200, "Sprites/objects/crateWood.png", 40, 40, True, True),
    (1550, 260, "Sprites/objects/crateWood.png", 40, 40, True, True),
    (1570, 190, "Sprites/objects/crateWood.png", 40, 40, True, True),
    (600, 300, "Sprites/objects/fenceRed.png", 30, 100, True, False),
    (800, 200, "Sprites/objects/fenceRed.png", 30, 100, True, False),
    (800, 500, "Sprites/objects/fenceYellow.png", 100, 30, True, False),
]

base_objects2 = [
    (1530, 50, "Sprites/objects/treeGreen_twigs.png", 30, 30, False, False),
    (1790, 950, "Sprites/objects/treeGreen_twigs.png", 30, 30, False, False),
    (400, 100, "Sprites/objects/treeBrown_twigs.png", 30, 30, False, False),
    (300, 900, "Sprites/objects/treeBrown_twigs.png", 30, 30, False, False),
    (1590, 150, "Sprites/objects/treeGreen_small.png", 50, 50, True, False),
    (1600, 800, "Sprites/objects/treeGreen_small.png", 50, 50, True, False),
    (1050, 200, "Sprites/objects/treeGreen_small.png", 50, 50, True, False),
    (1600, 600, "Sprites/objects/treeGreen_small.png", 50, 50, True, False),
    (400, 400, "Sprites/objects/treeBrown_small.png", 50, 50, True, False),
    (400, 700, "Sprites/objects/treeBrown_small.png", 50, 50, True, False),
    (100, 500, "Sprites/objects/treeBrown_large.png", 100, 100, True, False),
    (500, 500, "Sprites/objects/treeBrown_large.png", 100, 100, True, False),
    (1500, 100, "Sprites/objects/treeGreen_large.png", 100, 100, True, False),
    (1300, 800, "Sprites/objects/treeGreen_large.png", 100, 100, True, False),
    (700, 300, "Sprites/objects/sandbagBrown.png", 40, 30, True, True),
    (750, 350, "Sprites/objects/sandbagBrown.png", 40, 30, True, True),
    (800, 300, "Sprites/objects/sandbagBrown.png", 40, 30, True, True),
    (650, 350, "Sprites/objects/sandbagBrown.png", 40, 30, True, True),
    (600, 300, "Sprites/objects/sandbagBrown.png", 40, 30, True, True),
    (950, 200, "Sprites/objects/sandbagBeige.png", 30, 40, True, True),
    (950, 300, "Sprites/objects/sandbagBeige.png", 30, 40, True, True),
    (950, 400, "Sprites/objects/sandbagBeige.png", 30, 40, True, True),
    (950, 500, "Sprites/objects/sandbagBeige.png", 30, 40, True, True),
    (950, 600, "Sprites/objects/sandbagBeige.png", 30, 40, True, True),
    (950, 700, "Sprites/objects/sandbagBeige.png", 30, 40, True, True),
    (1200, 500, "Sprites/objects/sandbagBrown_open.png", 40, 30, True, True),
    (1300, 600, "Sprites/objects/sandbagBrown_open.png", 40, 30, True, True),
    (1250, 500, "Sprites/objects/sandbagBrown_open.png", 40, 30, True, True),
    (500, 700, "Sprites/objects/sandbagBeige_open.png", 30, 40, True, True),
    (540, 750, "Sprites/objects/sandbagBeige_open.png", 30, 40, True, True),
    (600, 780, "Sprites/objects/sandbagBeige_open.png", 30, 40, True, True),
    (600, 650, "Sprites/objects/crateMetal.png", 40, 40, True, True),
    (650, 620, "Sprites/objects/crateMetal.png", 40, 40, True, True),
    (640, 720, "Sprites/objects/crateMetal.png", 40, 40, True, True),
    (1200, 300, "Sprites/objects/crateWood.png", 40, 40, True, True),
    (1250, 360, "Sprites/objects/crateWood.png", 40, 40, True, True),
    (1270, 290, "Sprites/objects/crateWood.png", 40, 40, True, True),
    (900, 100, "Sprites/objects/fenceRed.png", 30, 100, True, False),
    (1550, 850, "Sprites/objects/fenceRed.png", 30, 100, True, False),
    (950, 750, "Sprites/objects/fenceYellow.png", 100, 30, True, False)

]

base_tank_positions1 = [
    (1200, 700, (0, 255, 0), "Sprites/tanks/tank_blue.png"),
    (300, 300, (0, 0, 255), "Sprites/tanks/tank_green.png"),
]

base_tank_positions2 = [
    (1400, 300, (0, 255, 0), "Sprites/tanks/tank_blue.png"),
    (300, 600, (0, 0, 255), "Sprites/tanks/tank_green.png"),
]

maps_data = [
    {"map_matrix": base_map_matrix1, "objects": base_objects1, "tanks_positions": base_tank_positions1},
    {"map_matrix": base_map_matrix2, "objects": base_objects2, "tanks_positions": base_tank_positions2},
    
]

def init_map(map_index):
    data = maps_data[map_index]
    matrix = data["map_matrix"]
    rows = len(matrix)
    cols = len(matrix[0])
    bg_w = cols * TILE_SIZE
    bg_h = rows * TILE_SIZE
    background = pg.Surface((bg_w, bg_h))
    for r, row in enumerate(matrix):
        for c, tile_id in enumerate(row):
            background.blit(tiles[tile_id], (c * TILE_SIZE, r * TILE_SIZE))
    boxes = []
    for (x, y, sprite, w, h, flag1, flag2) in data["objects"]:
        boxes.append(GameObject(x, y, sprite, w, h, flag1, flag2))
    tanks = []
    for (x, y, color, sprite) in data["tanks_positions"]:
        tanks.append(Tank(x, y, 60, 55, color, sprite))
    bullets = []
    explosions = []
    winner = None

    return background, boxes, tanks, bullets, explosions, winner

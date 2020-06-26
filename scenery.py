import pygame
import os
from random import choice, randint
from math import sqrt

class Tile():
    def __init__(self, path_to_image, x, y, rotate=False):
        self.x = x ; self.y = y
        self.image = pygame.image.load(path_to_image)

        if rotate:
            rots = [0, 90, 180, 270]
            self.image = pygame.transform.rotate(self.image, choice(rots))

class Bushes():
    def __init__(self, screen, quantity, collideables=[]):
        w, h = screen.get_size()
        self.screen = screen
        self.tiles = []

        path_to_tiles = 'Data/Bushes/'

        if collideables == []:
            positions = []
            for _ in range(100):
                x, y = randint(0, w), randint(0, h)

                if len(positions) == 0:
                    positions.append((x, y))
                    self.tiles.append(Tile(path_to_tiles + choice(os.listdir(path_to_tiles)), x - 16, y - 16))

                valid = True
                for try_x, try_y in positions:
                    if sqrt((try_x - x)**2 + (try_y - y)**2) < 32:
                        valid = False
                        break

                if valid:
                    positions.append((x, y))
                    self.tiles.append(Tile(path_to_tiles + choice(os.listdir(path_to_tiles)), x - 16, y - 16))
        else:
            w, h = screen.get_size()
            self.screen = screen
            self.tiles = []

            path_to_tiles = 'Data/Bushes/'

            for _ in range(quantity):
                x, y = randint(0, w), randint(0, h)

                if pygame.Rect(x, y, 32, 32).collidelist(collideables) == -1:
                    self.tiles.append(Tile(path_to_tiles + choice(os.listdir(path_to_tiles)), x, y))
                    collideables.append(pygame.Rect(x, y, 32, 32))

    def draw(self):
        for tile in self.tiles:
            self.screen.blit(tile.image, (tile.x, tile.y))
    
    def get_collideables(self):
        collideables = []

        for i in self.tiles:
            rect = i.image.get_rect()
            rect[0] += i.x
            rect[1] += i.y

            collideables.append(rect)     

        return collideables 

class Trees():
    def __init__(self, screen, quantity):
        w, h = screen.get_size()
        self.screen = screen
        self.tiles = []

        path_to_tiles = 'Data/Trees/'

        for _ in range(quantity):
            path = path_to_tiles + choice(os.listdir(path_to_tiles))
            tile = pygame.image.load(path)

            x, y = randint(0, w), randint(0, h)
            width, height = tile.get_size()

            if pygame.Rect(x, y, width, height).collidelist(self.get_collideables()) == -1:
                self.tiles.append(Tile(path, x, y))

    def draw(self):
        for tile in self.tiles:
            self.screen.blit(tile.image, (tile.x, tile.y))

    def get_collideables(self):
        collideables = []

        for tree in self.tiles:
            x, y, w, h = tree.image.get_rect()
            x += tree.x
            y += tree.y

            collideables.append(pygame.Rect(x, y, w, h))

        return collideables

class Ground():
    def __init__(self, screen):
        w, h = screen.get_size()
        self.screen = screen
        self.tiles = []

        path_to_tiles = 'Data/Ground/'

        for i in range(int(h / 64)):
            for j in range(int(w / 64)):
                self.tiles.append(Tile(path_to_tiles + choice(os.listdir(path_to_tiles)), j * 64, i * 64, rotate=True))

    def draw(self):
        for tile in self.tiles:
            self.screen.blit(tile.image, (tile.x, tile.y))

class Birds():
    def __init__(self, trees, screen):
        path_to_birds = 'Data/Birds/'
        self.bird = pygame.image.load(path_to_birds + choice(os.listdir(path_to_birds)))
        self.screen = screen

        tree = choice(trees)
        self.trees = trees

        self.x = tree.x + tree.w/2
        self.y = tree.y

        self.state = 'idle'
        self.wait_time = (600, 1200)
        self.stay_on_tree_timer = randint(self.wait_time[0], self.wait_time[1])

    def draw(self):
        self.screen.blit(self.bird, (self.x, self.y))

        if self.state == 'idle':
            self.stay_on_tree_timer -= 1

            if self.stay_on_tree_timer <= 0:
                self.state = 'pick_tree'
        
        if self.state == 'pick_tree':
            x, y, w, _ = choice(self.trees)

            self.target_x, self.target_y = x + w/2, y
            self.heading_x = self.target_x - self.x ; self.heading_y = self.target_y - self.y

            mag = sqrt(self.heading_x**2 + self.heading_y**2)
            if mag == 0 : self.state = 'pick_tree' ; return
            self.heading_x /= mag ; self.heading_y /= mag

            self.state = 'fly'
        
        if self.state == 'fly':
            if sqrt((self.target_x - self.x)**2 + (self.target_y - self.y)**2) > 1:
                self.x += self.heading_x ; self.y += self.heading_y
            else:
                self.x = self.target_x ; self.y = self.target_y

                self.stay_on_tree_timer = randint(self.wait_time[0], self.wait_time[1])
                self.state = 'idle'

class Scenery():
    def __init__(self, screen, trees=20, bushes=20):
        self.ground = Ground(screen)
        self.trees = Trees(screen, trees)

        self.bird = Birds(self.trees.get_collideables(), screen)

        self.bushes = Bushes(screen, bushes, collideables=self.trees.get_collideables())

    def draw(self):
        self.ground.draw()
        self.bushes.draw()
        self.trees.draw()
        self.bird.draw()

    def draw_collideables(self):
        for i in self.bushes.get_collideables() + self.trees.get_collideables():
            pygame.draw.rect(self.ground.screen, [255, 0, 0], i, 1)




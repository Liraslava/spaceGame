import pygame
from pygame.image import load
from pygame.math import Vector2
from pygame.transform import rotozoom
import random

def get_random_position(surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height())
    )

def load_sprite(name, with_alpha=True):
    path = r'C:\Users\User1\game_project223\my_project\space.png'.format(name)
    loded_sprite = load(path)
    if with_alpha:
        return loded_sprite.convert_alpha()
    else:
        return loded_sprite.convert()

def load_sprite1(name, with_alpha=True):
    path = r'C:\Users\User1\game_project223\my_project\spaceship.png'.format(name)
    loded_sprite1 = load(path)
    if with_alpha:
        return loded_sprite1.convert_alpha()
    else:
        return loded_sprite1.convert()

def load_sprite2(name, with_alpha=True):
    path = r'C:\Users\User1\game_project223\my_project\asteroid.png'.format(name)
    loded_sprite2 = load(path)
    if with_alpha:
        return loded_sprite2.convert_alpha()
    else:
        return loded_sprite2.convert()

UP = Vector2(0, -1)

def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)

class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius

class Spaceship(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.25

    def __init__(self, position):
        super(Spaceship, self).__init__(position, load_sprite1('spaceship'), Vector2(0))
        self.direction = Vector2(UP)

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION

    def slowdown(self):
        self.velocity -= self.direction * self.ACCELERATION

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)



class Asteroid(GameObject):
    def __init__(self, position):
        super(Asteroid, self).__init__(position, load_sprite2('asteroid'), (0,0))

class SpaceRock:
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.asteroids = [Asteroid((get_random_position(self.screen))) for _ in range(7)]
        self.background = load_sprite('space', False)
        self.spaceship = Spaceship((400, 300))

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption('Космические приключения')

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quit()

        is_key_processed = pygame.key.get_pressed()
        if is_key_processed[pygame.K_RIGHT]:
            self.spaceship.rotate(clockwise=True)
        elif is_key_processed[pygame.K_LEFT]:
            self.spaceship.rotate(clockwise=False)
        elif is_key_processed[pygame.K_UP]:
            self.spaceship.accelerate()
        elif is_key_processed[pygame.K_DOWN]:
            self.spaceship.slowdown()

    def _get_game_object(self):
        return[*self.asteroids, self.spaceship]

    def _process_game_logic(self):
        for game_object in self._get_game_object():
            game_object.move(self.screen)

        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    quit()

    def _draw(self):
        self.screen.blit(self.background, (0,0))
        for game_object in self._get_game_object():
            game_object.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)



if __name__ == '__main__':
    space_rocks = SpaceRock()
    space_rocks.main_loop()
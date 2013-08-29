# Imports, sorted alphabetically.

# Python packages
from math import cos, sin, atan2, radians
import random

# Third-party packages
# Nothing for now...

# Modules from this project
from entity import Entity
import globals as G
# import blocks as B
from inventory import Inventory
from model import PlayerModel
from utils import normalize, FACES


__all__ = (
    'Player',
)


class Player(Entity):
    local_player = True

    def __init__(self, position=(0,0,0), rotation=(-20, 0), flying=False,
                 game_mode=G.GAME_MODE, username="", local_player=True):
        super(Player, self).__init__(position, rotation, health=7,
                                     max_health=10, attack_power=2.0 / 3,
                                     attack_range=4)
        self.inventory = Inventory(27)
        self.quick_slots = Inventory(9)
        self.armor = Inventory(4)
        self.flying = flying
        self.game_mode = game_mode
        self.strafe = [0, 0]
        self.dy = 0
        self.current_density = 1 # Current density of the block we're colliding with
        self._position = position
        self.last_sector = None
        self.last_damage_block = 0, 100, 0 # dummy temp value
        self.username = username
        self.local_player = local_player

        # for debug
        #initial_items = [B.cake_block, B.torch_block]
        #for item in initial_items:
        #        self.inventory.add_item(item.id, item.max_stack_size)

        if not local_player:
            self.model = PlayerModel(position)
            self.momentum = (0,0,0)

    def add_item(self, item_id, quantity=1):
        if self.quick_slots.add_item(item_id, quantity=quantity):
            return True
        elif self.inventory.add_item(item_id, quantity=quantity):
            return True
        return False

    def change_health(self, change):
        self.health += change
        if self.health > self.max_health:
            self.health = self.max_health
    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
        if not self.local_player: self.model.update_position(value)

    def on_deactivate(self):
        self.strafe = [0, 0]

    def on_key_release(self, symbol, modifiers):
        if symbol == G.MOVE_FORWARD_KEY:
            self.strafe[0] += 1
        elif symbol == G.MOVE_BACKWARD_KEY:
            self.strafe[0] -= 1
        elif symbol == G.MOVE_LEFT_KEY:
            self.strafe[1] += 1
        elif symbol == G.MOVE_RIGHT_KEY:
            self.strafe[1] -= 1
        elif (symbol == G.JUMP_KEY
              or symbol == G.CROUCH_KEY) and self.flying:
            self.dy = 0

    def on_key_press(self, symbol, modifiers):
        if symbol == G.MOVE_FORWARD_KEY:
            self.strafe[0] -= 1
        elif symbol == G.MOVE_BACKWARD_KEY:
            self.strafe[0] += 1
        elif symbol == G.MOVE_LEFT_KEY:
            self.strafe[1] -= 1
        elif symbol == G.MOVE_RIGHT_KEY:
            self.strafe[1] += 1
        elif symbol == G.JUMP_KEY:
            if self.flying:
                self.dy = 0.045  # jump speed
            elif self.dy == 0:
                self.dy = 0.016  # jump speed
                G.CLIENT.send_jump()
        elif symbol == G.CROUCH_KEY:
            if self.flying:
                self.dy = -0.045  # inversed jump speed
        elif symbol == G.FLY_KEY and self.game_mode == G.CREATIVE_MODE:
            self.dy = 0
            self.flying = not self.flying

    def get_motion_vector(self, multiplier=1):
        if any(self.strafe):
            x, y = self.rotation
            y_r = radians(y)
            x_r = radians(x)
            strafe = atan2(*self.strafe)
            if self.flying:
                m = cos(y_r)
                dy = sin(y_r)
                if self.strafe[1]:
                    dy = 0.0
                    m = 1
                if self.strafe[0] > 0:
                    dy *= -1
                x_r += strafe
                dx = cos(x_r) * m
                dz = sin(x_r) * m
            else:
                dy = 0.0
                x_r += strafe
                dx = cos(x_r)
                dz = sin(x_r)
        else:
            dy = 0.0
            dx = 0.0
            dz = 0.0
        return dx*multiplier, dy*multiplier, dz*multiplier

    def get_sight_vector(self):
        x, y = self.rotation
        y_r = radians(y)
        x_r = radians(x)
        m = cos(y_r)
        dy = sin(y_r)
        x_r -= G.HALF_PI
        dx = cos(x_r) * m
        dz = sin(x_r) * m
        return dx, dy, dz

    def update(self, dt, parent):
        # walking
        if self.local_player:
            speed = 15 if self.flying else 5*self.current_density
            dx, dy, dz = self.get_motion_vector(multiplier=(dt * speed))
        else:
            dx, dy, dz = self.momentum
            dx, dy, dz = dx*dt, dy*dt, dz*dt

        # gravity
        if not self.flying:
            self.dy -= dt * 0.022  # g force, should be = jump_speed * 0.5 / max_jump_height
        self.dy = max(self.dy, -0.5)  # terminal velocity
        dy += self.dy

        # collisions
        x, y, z = self.position
        self.position = self.collide(parent, (x + dx, y + dy, z + dz), 2)

    def collide(self, parent, position, height):
        pad = 0.25
        p = list(position)
        np = normalize(position)
        self.current_density = 1 # Reset it, incase we don't hit any water
        for face in FACES:  # check all surrounding blocks
            for i in xrange(3):  # check each dimension independently
                if not face[i]:
                    continue
                d = (p[i] - np[i]) * face[i]
                if d < pad:
                    continue
                for dy in xrange(height):  # check each height
                    op = list(np)
                    op[1] -= dy
                    op[i] += face[i]
                    op = tuple(op)
                    # If there is no block or if the block is not a cube,
                    # we can walk there.
                    if op not in parent.world \
                            or parent.world[op].vertex_mode != G.VERTEX_CUBE:
                        continue
                    # if density <= 1 then we can walk through it. (water)
                    if parent.world[op].density < 1:
                        self.current_density = parent.world[op].density
                        continue
                    # if height <= 1 then we can walk on top of it. (carpet, half-blocks, etc...)
                    if parent.world[op].height < 0.5:
                        #current_height = parent.world[op].height
                        #x, y, z = self.position
                        #new_pos = (x, y + current_height, z)
                        #self.position = new_pos
                        continue

                    if parent.world[op].player_damage > 0:
                        if self.last_damage_block != np:
                            # this keeps a player from taking the same damage over and over...
                            self.change_health( - parent.world[op].player_damage)
                            parent.item_list.update_health()
                            self.last_damage_block = np
                            continue
                        else:
                            #do nothing
                            continue


                    p[i] -= (d - pad) * face[i]
                    if face == (0, -1, 0) or face == (0, 1, 0):
                        # jump damage
                        if self.game_mode == G.SURVIVAL_MODE:
                            damage = self.dy * -1000.0
                            damage = 3.0 * damage / 22.0
                            damage -= 2.0
                            if damage >= 0.0:
                                health_change = 0
                                if damage <= 0.839:
                                    health_change = 0
                                elif damage <= 1.146:
                                    health_change = -1
                                elif damage <= 1.44:
                                    health_change = -2
                                elif damage <= 2.26:
                                    health_change = -2
                                else:
                                    health_change = -3
                                if health_change != 0:
                                    self.change_health(health_change)
                                    parent.item_list.update_health()
                        self.dy = 0
                    break
        return tuple(p)

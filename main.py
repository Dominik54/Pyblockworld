import math

from pyblockworld import World, Window
from pyglet.window import key

TICKS_PER_SEC = 60

# Size of sectors used to ease block loading.
SECTOR_SIZE = 16

WALKING_SPEED = 10
FLYING_SPEED = 15

GRAVITY = 20.0
MAX_JUMP_HEIGHT = 2.0  # About the height of a block.
# To derive the formula for calculating jump speed, first solve
#    v_t = v_0 + a * t
# for the time at which you achieve maximum height, where a is the acceleration
# due to gravity and v_t = 0. This gives:
#    t = - v_0 / a
# Use t and the desired MAX_JUMP_HEIGHT to solve for v_0 (jump speed) in
#    s = s_0 + v_0 * t + (a * t^2) / 2
JUMP_SPEED = math.sqrt(2 * GRAVITY * MAX_JUMP_HEIGHT)
TERMINAL_VELOCITY = 50

PLAYER_HEIGHT = 2

'''
print("Block types", World.MATERIALS)

#
# BEISPIEL 1
#

# Eine Funktion, die beim Drücken der B-Taste aufgerufen werden soll
def b_key_pressed(world: World):
    print("B pressed. Player at", world.player_position())


# Erstellen einer neuen Welt
world = World()
# Die Funktion für die build-Taste (b) wird zugewiesen
world.build_key_pressed = b_key_pressed
# Die Welt wird gestartet
world.run()

'''


#   print("Block types", World.MATERIALS)


class BlockWorld:
    def set_block(self, x, y, z, block):
        pass

    def set_blocks(self, x1, y1, z1, x2, y2, z2):
        pass

    def player_position(self):
        pass


blockworld = BlockWorld()


class Wall:
    def __init__(self, bw=None, rotated=False, height=5):
        self.width = 6
        self.height = height
        self.rotated = rotated
        self.material_id = "default:stone"
        self._bw = bw

    def get_target_build_block_vector(self, world: World):
        vector = world.window.get_sight_vector()
        block, previous = world.window.model.hit_test(world.window.position, vector)
        print(f"this is block: {block}, this is previous: {previous}")
        return block, previous

    def build(self, world: World, y_initial=None, material="default:brick"):
        block, previous = self.get_target_build_block_vector(world)

        if block:
            x, y, z = block
            print(f"this is x: {x}, this is y: {y}, this is z: {z}")
            y_start = y_initial if y_initial is not None else y
            if not self.rotated:
                direction = (1, 0)  # Along x-axis
            else:
                #   world.setBlocks(x-1, y, z+1, x-1, y + self.height - 1, z + 7, material)
                direction = (0, 1)  # Along Z-Axis

            x_end = x + direction[0] * self.width
            y_end = y_start + self.height
            z_end = z + direction[1] * self.width

            world.setBlocks(x, y_start, z, x_end, y_end, z_end, material)
            return y_start

        else:
            print("No block found under crosshairs")


class WallWithDoor(Wall):
    def __init__(self, bw):
        super().__init__(bw)
        self.door_material_id = "default:wood"
        self.door_is_open = False

    def build(self, world: World, y_initial=None, material="default:brick"):
        super().build(world, y_initial, material)

    def trigger_door(self):
        if not self.door_is_open:
            self.door_is_open = True
        else:
            self.door_is_open = False


class WallWithWindow(Wall):
    def __init__(self, bw):
        super().__init__(bw)
        self.window_material_id = "air"

    def build(self, world: World, y_initial=None, material="default:brick"):
        pass


class Roof:
    def __init__(self):
        self.width = 6
        self.depth = 6
        self.roof_material_id = "default:brick"
        self.pos = ()
        self.__bw = BlockWorld
        

class House:
    def __init__(self, bw, pos):
        self.wallFront = Wall
        self.wallLeft = Wall
        self.wallRight = Wall
        self.wallBack = Wall
        self.pos = pos
        self.roof = Roof()


class CustomWorld(World):
    def __init__(self, name="Custom World"):
        super().__init__(name=name, create_window=False)
        self.window = CustomWindow(self)


class CustomWindow(Window):
    def __init__(self, world, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.world = world
        self.wall_with_window = WallWithWindow(blockworld)
        self.wall_with_door = WallWithDoor(blockworld)
        self.materials = ["air", "default:brick", "default:stone", "default:sand", "default:grass"]

    def get_position(self, world):
        vector = world.window.get_sight_vector()  # returns current line of sight vector where pl. are looking
        print(f"This is the vector: {vector}")
        block, previous = world.window.model.hit_test(world.window.position, vector)
        return block, previous

    def on_key_press(self, symbol, modifiers):
        """ Called when the player presses a key. See pyglet docs for key
        mappings.

        Parameters
        ----------
        symbol : int
            Number representing the key that was pressed.
        modifiers : int
            Number representing any modifying keys that were pressed.

        """
        if symbol == key.W:
            self.strafe[0] -= 1
        elif symbol == key.S:
            self.strafe[0] += 1
        elif symbol == key.A:
            self.strafe[1] -= 1
        elif symbol == key.D:
            self.strafe[1] += 1
        elif symbol == key.SPACE:
            if self.dy == 0:
                self.dy = JUMP_SPEED
        elif symbol == key.ESCAPE:
            self.set_exclusive_mouse(False)
        elif symbol == key.Y:
            self.position = (0, 0, 0)
            dx, dy, dz = self.get_motion_vector()
            self.dy = 0
        elif symbol == key.V:   # Builds one block, default being set to sand
            print("V key pressed")
            vector = self.world.window.get_sight_vector()
            block, previous = self.world.window.model.hit_test(self.world.window.position, vector)
            print(f"This is block: {block}; This is previous: {previous}")
            if block:
                x, y, z = block
                self.world.setBlock(x, y + 1, z, "default:sand")
        elif symbol == key.B:   # Builds three blocks of stone put on top of each other
            print("B key pressed")
            self.b_key_pressed(self.world)
        elif symbol == key.N:   # Builds three blocks of varying materials put on top of each other
            print("N key pressed")
            self.n_key_pressed(self.world)
        elif symbol == key.M:   # Builds two brick walls, one rotated by 90 degrees to the other
            print("M key pressed")
            self.m_key_pressed(self.world)
        elif symbol == key.G:   # Builds wall with door
            print("G key pressed")
            self.g_key_pressed(self.world)
        elif symbol == key.H:   # Builds the House
            print("H key pressed")
            self.h_key_pressed(self.world)
        elif symbol == key.I:   # Builds a Wall with a window
            print("J key pressed")
            self.j_key_pressed(self.world)
        elif symbol == key.K:   # Builds 4 walls, one with a window, one with a door
            print("K key pressed")
            self.k_key_pressed(self.world)
        elif symbol == key.R:   # Builds a roof
            print("R key pressed")
            self.r_key_pressed(self.world)
        elif symbol == key.O:    # Opens a door
            print("O key pressed")
            self.o_key_pressed(self.world)
        elif symbol == key.TAB:
            self.flying = not self.flying
        elif symbol in self.num_keys:
            index = (symbol - self.num_keys[0]) % len(self.inventory)
            self.block = self.inventory[index]
        else:
            self.unknown_key_pressed(symbol)

    def b_key_pressed(self, world: World, material="default:stone"):
        # Neue Blöcke können mit setBlock gesetzt werden.
        # Verfügbare Materialien stehen in World.MATERIALS und umfassen
        # air, default:brick, default:stone, default:sand, default:grass

        block, previous = self.get_position(world)

        if block:
            x, y, z = block

            # Einen Block platzieren
            #   world.setBlock(x+1, y, z, "default:brick")

            # Mehrere Blöcke auf einmal abseits des Spielers platzieren
            world.setBlocks(x, y+1, z, x, y + 3, z, material)
            print(f"block = {block} previous = {previous}")
        else:
            print("No block found under crosshairs")

    def n_key_pressed(self, world: World, material="default:brick"):

        block, previous = self.get_position(world)

        if block:
            x, y, z = block

            # Einen Block platzieren
            #   world.setBlock(x+1, y, z, "default:brick")

            # Mehrere Blöcke auf einmal abseits des Spielers platzieren
            world.setBlock(x, y + 1, z, material)
            world.setBlock(x, y + 2, z, "default:sand")
            world.setBlock(x, y + 3, z, "default:stone")

        else:
            print("No block found under crosshairs")

    def m_key_pressed(self, world: World, material="default:brick"):
        wall_not_rotated = Wall(bw=world)
        wall_rotated = Wall(bw=world, rotated=True)
        y_initial = wall_not_rotated.build(world=world, material="default:brick")
        wall_rotated.build(world=world, y_initial=y_initial, material="default:brick")

    def g_key_pressed(self, world: World, material="default:brick"):
        wall_with_door = WallWithDoor(bw=world)
        block, previous = self.get_position(world)

        if block:
            # Build the brick wall first
            y_initial = wall_with_door.build(world, material=material)

            # Calculate door position
            x, y, z = block
            door_height = 2  # Door height can be 2 blocks, for example
            door_y_start = y_initial + 1  # Position the door above ground level
            door_y_end = door_y_start + door_height

            # Determine where to place the door within the wall's width
            door_x = x + (wall_with_door.width // 2)  # Center the door along the wall's width

            # Place the door blocks by overwriting part of the wall with wooden material
            for dy in range(door_y_start, door_y_end):
                world.setBlock(door_x, dy, z, wall_with_door.door_material_id)

            print(
                f"Built a wall with a door at position: ({door_x}, {door_y_start}, {z}) to ({door_x}, {door_y_end}, {z})")
        else:
            print("No block found under crosshairs")

    def h_key_pressed(self, world: World, material="default:brick"):
        pass

    def j_key_pressed(self, world: World):
        pass

    def k_key_pressed(self, world: World):
        pass

    def r_key_pressed(self, world:World):
        pass

    def o_key_pressed(self, world:World):
        block, previous = self.get_position(world)
        if block:
            x, y, z = block
            WallWithDoor.trigger_door(self)


def main():
    world = CustomWorld()
    world.run()


if __name__ == "__main__":
    main()

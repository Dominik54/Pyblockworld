from pyblockworld import World, Window
from pyglet.window import key

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


class Wall:
    def __init__(self, pos=(), bw=None):
        self.width = 6
        self.height = 5
        self.pos = pos
        self.rotated = False
        self.material_id = "default:stone"
        self._bw = blockworld

    def build(self, world: World, material="default:brick"):
        vector = world.window.get_sight_vector()
        block, previous = world.window.model.hit_test(world.window.position, vector)

        if block:
            x, y, z = block

            # Einen Block platzieren
            #   world.setBlock(x+1, y, z, "default:brick")

            # Mehrere Blöcke auf einmal abseits des Spielers platzieren
            world.setBlocks(x, y, z, x + self.width, y + self.height, z, material)
        else:
            print("No block found under crosshairs")


class WallWithDoor(Wall):
    def __init__(self, pos, bw):
        super().__init__(pos, bw)
        self.door_material_id = "air"

    def build(self, world: World, material="default:brick"):
        pass


class WallWithWindow(Wall):
    def __init__(self, pos, bw):
        super().__init__(pos, bw)
        self.window_material_id = "air"

    def build(self, world: World, material="default:brick"):
        pass


class CustomWorld(Wall):
    def __init__(self):
        super().__init__(*args, **kwargs)


class CustomWindow(Window):
    def __init__(self, world, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.world = world
        self.wall_with_window = WallWithWindow(world.window.position, blockworld)
        self.wall_with_door = WallWithDoor(world.window.position, blockworld)
        self.materials = ["air", "default:brick", "default:stone", "default:sand", "default:grass"]

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
                self.dy = self.JUMP_SPEED
        elif symbol == key.ESCAPE:
            self.set_exclusive_mouse(False)
        elif symbol == key.Y:
            self.position = (0, 0, 0)
            dx, dy, dz = self.get_motion_vector()
            self.dy = 0
        elif symbol == key.V:
            print("V key pressed")
            vector = self.world.window.get_sight_vector()
            block, previous = self.world.window.model.hit_test(self.world.window.position, vector)
            if block:
                x, y, z = block
                self.world.setBlock(x, y + 1, z, "default:sand")
        elif symbol == key.B:
            print("B key pressed")
            CustomWindow.b_key_pressed(self.world)
        elif symbol == key.N:
            print("N key pressed")
            CustomWindow.n_key_pressed(self.world)
        elif symbol == key.M:
            print("M key pressed")
            CustomWindow.m_key_pressed(self, self.world)
        elif symbol == key.TAB:
            self.flying = not self.flying
        elif symbol in self.num_keys:
            index = (symbol - self.num_keys[0]) % len(self.inventory)
            self.block = self.inventory[index]
        else:
            self.unknown_key_pressed(symbol)

    @staticmethod
    def b_key_pressed(world: World, material="default:stone"):
        # Neue Blöcke können mit setBlock gesetzt werden.
        # Verfügbare Materialien stehen in World.MATERIALS und umfassen
        # air, default:brick, default:stone, default:sand, default:grass

        vector = world.window.get_sight_vector()

        block, previous = world.window.model.hit_test(world.window.position, vector)

        if block:
            x, y, z = block

            # Einen Block platzieren
            #   world.setBlock(x+1, y, z, "default:brick")

            # Mehrere Blöcke auf einmal abseits des Spielers platzieren
            world.setBlocks(x, y, z, x, y + 3, z, material)
        else:
            print("No block found under crosshairs")

    @staticmethod
    def n_key_pressed(world: World, material="default:brick"):

        vector = world.window.get_sight_vector()
        block, previous = world.window.model.hit_test(world.window.position, vector)

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

        vector = world.window.get_sight_vector()
        block, previous = world.window.model.hit_test(world.window.position, vector)

        if block:
            Wall.build(self, world, material)
        else:
            print("No block found under crosshairs")


class CustomWorld(World):
    def __init__(self, name="Custom World"):
        super().__init__(name=name, window_class=lambda *args, **kwargs: CustomWindow(self, *args, **kwargs))


def main():
    world = CustomWorld()
    world.run()


blockworld = BlockWorld

if __name__ == "__main__":
    main()

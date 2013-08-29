# Imports, sorted alphabetically.

# Python packages
import random

# Third-party packages
# Nothing for now...

# Modules from this project
import blocks as B
import globals as G


#
# Base
#

class SmallPlant(object):
    def __init__(self, block=None, grows_on=None):
        self.block = block
        self.grows_on = grows_on or (B.grass_block, B.dirt_block)

    def add_to_world(self, world, position, sync=False):
        world.add_block(position, self.block, sync=sync)


class Trunk(object):
    block = None
    height_range = 4, 8
    grows_on = ()

    def __init__(self, position, block=None, height_range=None):
        if block is not None:
            self.block = block
        if height_range is not None:
            self.height_range = height_range

        x, y, z = position

        self.height = random.randint(*self.height_range)
        self.blocks = {}
        for dy in range(self.height):
            self.blocks[(x, y + dy, z)] = self.block

##    @classmethod
#    def add_to_world(cls, world, position, sync=False):
#        trunk = cls(position)
#        for item in trunk.blocks.items():
#            world.add_block(*item, sync=sync)

class Tree(object):
    trunk_block = None
    leaf_block = None
    trunk_height_range = 4, 8

    def __init__(self, trunk_block=None, leaf_block=None, trunk_height_range=None, grows_on=None):
        self.trunk_block = trunk_block
        self.leaf_block = leaf_block
        self.trunk_height_range = trunk_height_range or (4, 8)
        self.grows_on = grows_on or (B.grass_block, B.dirt_block, B.snowgrass_block)

    def add_to_world(self, world, position, sync=False):
        trunk = Trunk(position, block=self.trunk_block,
                      height_range=self.trunk_height_range)

        for item in trunk.blocks.items():
            world.add_block(*item, force=False, sync=sync)

        x, y, z = position
        height = trunk.height
        treetop = y + height

        # Leaves generation
        d = height / 3 + 1
        for xl in range(x - d, x + d):
            dx = abs(xl - x)
            for yl in range(treetop - d, treetop + d):
                for zl in range(z - d, z + d):
                    # Don't replace existing blocks
                    if (xl, yl, zl) in world:
                        continue
                    # Avoids orphaned leaves
                    if not world.has_neighbors((xl, yl, zl),
                                               set((self.trunk_block,
                                                    self.leaf_block))):
                        continue
                    dz = abs(zl - z)
                    # The farther we are (horizontally) from the trunk,
                    # the least leaves we can find.
                    if random.uniform(0, dx + dz) > 0.6:
                        continue
                    world.add_block((xl, yl, zl), self.leaf_block, force=False,
                                    sync=sync)

#
# Small plants
#

# The _ is temporary to rename away the old names
# Please use the new ones, see _init()

class WaterMelon_(SmallPlant):
    def __init__(self):
        super(WaterMelon_, self).__init__(block=B.melon_block, grows_on=(B.grass_block, B.dirt_block, B.snowgrass_block))

class Pumpkin_(SmallPlant):
    def __init__(self):
        super(Pumpkin_, self).__init__(block=B.pumpkin_block, grows_on=(B.grass_block, B.dirt_block, B.snowgrass_block))

class YFlowers_(SmallPlant):
    def __init__(self):
        super(YFlowers_, self).__init__(block=B.yflowers_block)

class Potato_(SmallPlant):
    def __init__(self):
        super(Potato_, self).__init__(block=B.potato_block)

class Carrot_(SmallPlant):
    def __init__(self):
        super(Carrot_, self).__init__(block=B.carrot_block)

class Rose_(SmallPlant):
    def __init__(self):
        super(Rose_, self).__init__(block=B.rose_block)


class TallGrass_(SmallPlant):
    def __init__(self):
        super(TallGrass_, self).__init__(block=B.fern_block)

class TallGrass0_(SmallPlant):
    def __init__(self):
        super(TallGrass0_, self).__init__(block=B.wildgrass0_block, grows_on=(B.grass_block, B.dirt_block))

class TallGrass1_(SmallPlant):
    def __init__(self):
        super(TallGrass1_, self).__init__(block=B.wildgrass1_block, grows_on=(B.grass_block, B.dirt_block))

class TallGrass2_(SmallPlant):
    def __init__(self):
        super(TallGrass2_, self).__init__(block=B.wildgrass2_block, grows_on=(B.grass_block, B.dirt_block))

class TallGrass3_(SmallPlant):
    def __init__(self):
        super(TallGrass3_, self).__init__(block=B.wildgrass3_block, grows_on=(B.grass_block, B.dirt_block))

class TallGrass4_(SmallPlant):
    def __init__(self):
        super(TallGrass4_, self).__init__(block=B.wildgrass4_block, grows_on=(B.grass_block, B.dirt_block))

class TallGrass5_(SmallPlant):
    def __init__(self):
        super(TallGrass5_, self).__init__(block=B.wildgrass5_block, grows_on=(B.grass_block, B.dirt_block))

class TallGrass6_(SmallPlant):
    def __init__(self):
        super(TallGrass6_, self).__init__(block=B.wildgrass6_block, grows_on=(B.grass_block, B.dirt_block))

class TallGrass7_(SmallPlant):
    def __init__(self):
        super(TallGrass7_, self).__init__(block=B.wildgrass7_block, grows_on=(B.grass_block, B.dirt_block))

class DeadBush_(SmallPlant):
    def __init__(self):
        super(DeadBush_, self).__init__(block=B.deadbush_block, grows_on=(B.sand_block, B.sandstone_block))

class DesertGrass_(SmallPlant):
    def __init__(self):
        super(DesertGrass_, self).__init__(block=B.desertgrass_block, grows_on=(B.sand_block, B.sandstone_block))

#
# Tall plants
#

class Cactus_(Trunk):
    def __init__(self, position=(0,0,0)):
        self.block = B.cactus_block
        self.height_range = 1, 4
        self.grows_on = (B.sand_block, B.sandstone_block)
        super(Cactus_, self).__init__(position)

class TallCactus_(Trunk):
    def __init__(self, position=(0,0,0)):
        self.block = B.tallcactus_block
        self.height_range = 1, 10
        self.grows_on = (B.sand_block, B.sandstone_block)
        super(TallCactus_, self).__init__(position)

class Reed_(Trunk):
    def __init__(self, position=(0,0,0)):
        self.block = B.reed_block
        self.height_range = 1, 4
        self.grows_on = (B.sand_block, B.dirt_block)
        super(Reed_, self).__init__(position)

#
# Trees
#

class OakTree_(Tree):
    def __init__(self):
        super(OakTree_, self).__init__(trunk_block=B.oakwood_block, leaf_block=B.oakleaf_block)

class JungleTree_(Tree):
    def __init__(self):
        super(JungleTree_, self).__init__(trunk_block=B.junglewood_block, leaf_block=B.jungleleaf_block, trunk_height_range=(8, 12))

class BirchTree_(Tree):
    def __init__(self):
        super(BirchTree_, self).__init__(trunk_block=B.birchwood_block, leaf_block=B.birchleaf_block, trunk_height_range=(5, 7))

@G.initializer
def _init(M):
    M.water_melon = WaterMelon_()
    M.pumpkin = Pumpkin_()
    M.y_flowers = YFlowers_()
    M.potato = Potato_()
    M.carrot = Carrot_()
    M.rose = Rose_()
    M.tall_grass = TallGrass_()
    M.tall_grass0 = TallGrass0_()
    M.tall_grass1 = TallGrass1_()
    M.tall_grass2 = TallGrass2_()
    M.tall_grass3 = TallGrass3_()
    M.tall_grass4 = TallGrass4_()
    M.tall_grass5 = TallGrass5_()
    M.tall_grass6 = TallGrass6_()
    M.tall_grass7 = TallGrass7_()
    M.dead_bush = DeadBush_()
    M.desert_grass= DesertGrass_()

    M.cactus = Cactus_()
    M.tall_cactus = TallCactus_()
    M.reed = Reed_()
    M.oak_tree = OakTree_()
    M.jungle_tree = JungleTree_()
    M.birch_tree = BirchTree_()

    M.SMALL_PLANTS = set((
        M.water_melon,
        M.pumpkin,      
        M.y_flowers,
        M.potato,
        M.carrot,
        M.rose,
        M.tall_grass,
        M.tall_grass0,
        M.tall_grass1,
        M.tall_grass2,
        M.tall_grass3,
        M.tall_grass4,
        M.tall_grass5,
        M.tall_grass6,
        M.tall_grass7,
        M.dead_bush,
        M.desert_grass,
    ))

    M.TALL_PLANTS = set((
        M.cactus,
        M.tall_cactus,
        M.reed,
    ))
    
    M.PLANTS = M.SMALL_PLANTS | M.TALL_PLANTS
    
    M.TREES = set((
        M.oak_tree,
        M.jungle_tree,
        M.birch_tree,
    ))

    M.VEGETATION = M.PLANTS | M.TREES

    M.TREE_BLOCKS = set(tree.trunk_block for tree in M.TREES)
    M.LEAF_BLOCKS = set(tree.leaf_block for tree in M.TREES)
    M.PLANT_BLOCKS = set(plant.block for plant in M.PLANTS)

    M.VEGETATION_BLOCKS = M.PLANT_BLOCKS | M.TREE_BLOCKS | M.LEAF_BLOCKS


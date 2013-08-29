# Imports, sorted alphabetically.

# Python packages
# Nothing for now...

# Third-party packages
# Nothing for now...

# Modules from this project
import blocks as B
import globals as G


# From MinecraftWiki
# Items are objects which do not exist outside of the player's inventory and hands
# i.e., they cannot be placed in the game world.
# Some items simply place blocks or entities into the game world when used.
# Type
# * Materials: iron ingot, gold ingot, etc.
# * Food: found or crafted by the player and eaten to regain hunger points
# * Potions
# * Tools
# * Informative items: map, compass and clock
# * Weapons
# * Armor

def get_item(item_or_block_id):
    """
    Get the Block or Item with the specified id, which must either be an instance
    of BlockID, or a string format BlockID knows how to parse.
    """
    if not isinstance(item_or_block_id, B.BlockID):
        item_or_block_id = B.BlockID(str(item_or_block_id))
    if item_or_block_id.main >= G.ITEM_ID_MIN:
        return G.ITEMS_DIR[item_or_block_id]
    else:
        return G.BLOCKS_DIR[item_or_block_id]


class Item(object):
    id = None
    max_stack_size = 0
    amount_label_color = 255, 255, 255, 255
    icon_name = None
    name = "Item"
    group = None

    # How long can this item burn (-1 for non-fuel items)
    burning_time = -1
    # How long does it take to smelt this item (-1 for unsmeltable items)
    smelting_time = -1

    def __init__(self):
        self.id = B.BlockID(self.id, 0, self.icon_name)
        G.ITEMS_DIR[self.id] = self

    def on_right_click(self, world, player):
        pass

    def __repr__(self):
        return self.name

class ItemStack(object):
    def __init__(self, type = 0, amount = 1, durability = -1):
        if amount < 1:
            amount = 1
        self.type = B.BlockID(type, 0, get_item(type).icon_name)
        self.amount = amount
        if durability == -1:
            self.durability = -1 if not hasattr(self.get_object(), 'durability') else self.get_object().durability
        else:
            self.durability = durability
        self.max_durability = get_item(type).durability if hasattr(get_item(type), 'durability') else -1
        self.max_stack_size = get_item(type).max_stack_size

    # for debugging
    def __repr__(self):
        return '{ Item stack with type = ' + str(get_item(self.type)) + ' }'

    def change_amount(self, change=0):
        overflow = 0
        if change != 0:
            self.amount += change
            if self.amount < 0:
                self.amount = 0
            elif self.amount > self.max_stack_size:
                overflow = self.amount - self.max_stack_size
                self.amount -= overflow

        return overflow

    # compatible with blocks
    @property
    def id(self):
        return self.type

    # compatible with blocks
    @property
    def name(self):
        return self.get_object().name

    def get_object(self):
        return get_item(self.id)

class CoalItem(Item):
    id = 263
    icon_name = "coal"
    max_stack_size = 64
    name = "Coal"
    burning_time = 80

class LadderItem(Item):
    id = 999
    max_stack_size = 64
    name = "Ladder"

class DiamondItem(Item):
    id = 264
    icon_name = "diamond"
    max_stack_size = 64
    name = "Diamond"

class IronIngotItem(Item):
    id = 265
    icon_name = "ingotIron"
    max_stack_size = 64
    name = "Iron Ingot"

class GoldIngotItem(Item):
    id = 266
    icon_name = "ingotGold"
    max_stack_size = 64
    name = "Gold Ingot"

class StickItem(Item):
    id = 280
    max_stack_size = 64
    name = "Stick"
    burning_time = 5
    icon_name = "stick"

class BreadItem(Item):
    id = 297
    icon_name = "bread"
    max_stack_size = 64
    name = "Bread"
    regenerated_health = 3

class FlintItem(Item):
    id = 318
    icon_name = "flint"
    max_stack_size = 64
    name = "Flint"

class YellowDyeItem(Item):
    id = 351
    max_stack_size = 64
    name = "Dandelion Yellow Dye"
    icon_name = "dyePowder_yellow"

class CactusGreenDyeItem(Item):
    id = 351,2
    max_stack_size = 64
    name = "Cactus Green Dye"
    icon_name = "dyePowder_green"

class RedDyeItem(Item):
    id = 351,1
    max_stack_size = 64
    name = "Red Dye"
    icon_name = "dyePowder_red"

class BoneMeal(Item):
    id = 351,15
    max_stack_size = 64
    name = "Bone Meal"
    icon_name = "dyePowder_white"

    def on_right_click(self, world, player):
        block, previous = world.hit_test(player.position, player.get_sight_vector(), player.attack_range)
        if hasattr(world[block], 'fertilize'):
            return world[block].fertilize()
        else:
            return False

class SugarItem(Item):
    id = 353
    icon_name = "sugar"
    max_stack_size = 64
    name = "Sugar"

class SeedItem(Item):
    block_type = None
    soil_type = None

    def on_right_click(self, world, player):
        block, previous = world.hit_test(player.position, player.get_sight_vector(), player.attack_range)
        if previous:
            if world[block].id == self.soil_type.id: # plant
                world.add_block(previous, self.block_type)
                return True # remove from inventory

class WheatSeedItem(SeedItem):
    id = 295
    icon_name = "seeds"
    max_stack_size = 64
    name = "Seed"

    def __init__(self):
	self.block_type = B.wheat_crop_block
        self.soil_type = B.farm_block
        super(WheatSeedItem, self).__init__()

class PotatoItem(SeedItem):
    id = 392
    icon_name = "potato"
    max_stack_size = 64
    name = "Potato"
    regenerated_health = 1

    def __init__(self):
        block_type = B.potato_block
        self.soil_type = B.farm_block
        super(PotatoItem, self).__init__()

# class CookedPotatoItem(Item):

class CarrotItem(SeedItem):
    id = 391
    icon_name = "carrots"
    max_stack_size = 64
    name = "Carrot"
    regenerated_health = 1

    def __init__(self):
        self.block_type = B.carrot_block
        self.soil_type = B.farm_block
        super(CarrotItem, self).__init__()

class WheatItem(Item):
    id = 296
    icon_name = "wheat"
    max_stack_size = 64
    name = "Wheat"

class PaperItem(Item):
    id = 339
    icon_name = "paper"
    max_stack_size = 64
    name = "Paper"

class Tool(Item):
    material = None
    multiplier = 0
    tool_type = None

    def __init__(self):
        super(Tool, self).__init__()
        self.multiplier = 2 * (self.material + 1)

class WoodAxe(Tool):
    material = G.WOODEN_TOOL
    tool_type = G.AXE
    max_stack_size = 1
    id = 271
    durability = 20
    name = "Wooden Axe"
    icon_name = "hatchetWood"

class StoneAxe(Tool):
    material = G.STONE_TOOL
    tool_type = G.AXE
    max_stack_size = 1
    id = 275
    durability = 40
    name = "Stone Axe"
    icon_name = "hatchetStone"

class IronAxe(Tool):
    material = G.IRON_TOOL
    tool_type = G.AXE
    max_stack_size = 1
    id = 258
    durability = 60
    name = "Iron Axe"
    icon_name = "hatchetIron"

class DiamondAxe(Tool):
    material = G.DIAMOND_TOOL
    tool_type = G.AXE
    max_stack_size = 1
    id = 279
    durability = 100
    name = "Diamond Axe"
    icon_name = "hatchetDiamond"

class GoldenAxe(Tool):
    material = G.GOLDEN_TOOL
    tool_type = G.AXE
    max_stack_size = 1
    id = 286
    durability = 50
    name = "Golden Axe"
    icon_name = "hatchetGold"

class WoodPickaxe(Tool):
    material = G.WOODEN_TOOL
    tool_type = G.PICKAXE
    max_stack_size = 1
    id = 270
    icon_name = 'pickaxeWood'
    durability = 10
    name = "Wooden Pickaxe"

class StonePickaxe(Tool):
    material = G.STONE_TOOL
    tool_type = G.PICKAXE
    max_stack_size = 1
    id = 274
    icon_name = 'pickaxeStone'
    durability = 30
    name = "Stone Pickaxe"

class IronPickaxe(Tool):
    material = G.IRON_TOOL
    tool_type = G.PICKAXE
    max_stack_size = 1
    id = 257
    icon_name = 'pickaxeIron'
    durability = 40
    name = "Iron Pickaxe"

class DiamondPickaxe(Tool):
    material = G.DIAMOND_TOOL
    tool_type = G.PICKAXE
    max_stack_size = 1
    id = 278
    icon_name = 'pickaxeDiamond'
    durability = 150
    name = "Diamond Pickaxe"

class GoldenPickaxe(Tool):
    material = G.GOLDEN_TOOL
    tool_type = G.PICKAXE
    max_stack_size = 1
    id = 285
    durability = 30
    name = "Golden Pickaxe"
    icon_name = "pickaxeGold"

class WoodShovel(Tool):
    material = G.WOODEN_TOOL
    tool_type = G.SHOVEL
    max_stack_size = 1
    id = 269
    durability = 10
    name = "Wooden Shovel"
    icon_name = "shovelWood"

class StoneShovel(Tool):
    material = G.STONE_TOOL
    tool_type = G.SHOVEL
    max_stack_size = 1
    id = 273
    durability = 30
    name = "Stone Shovel"
    icon_name = "shovelStone"

class IronShovel(Tool):
    material = G.IRON_TOOL
    tool_type = G.SHOVEL
    max_stack_size = 1
    id = 256
    durability = 70
    name = "Iron Shovel"
    icon_name = "shovelIron"

class DiamondShovel(Tool):
    material = G.DIAMOND_TOOL
    tool_type = G.SHOVEL
    max_stack_size = 1
    id = 277
    durability = 100
    name = "Diamond Shovel"
    icon_name = "shovelDiamond"

class GoldenShovel(Tool):
    material = G.GOLDEN_TOOL
    tool_type = G.SHOVEL
    max_stack_size = 1
    id = 284
    durability = 30
    name = "Golden Shovel"
    icon_name = "shovelGold"

class Hoe(Tool):
    def __init__(self):
        super(Hoe, self).__init__()

    def on_right_click(self, world, player):
        block, previous = world.hit_test(player.position, player.get_sight_vector(), player.attack_range)
        if previous:
            if world[block].id == B.dirt_block.id or world[block].id == B.grass_block.id:
                world.add_block(block, B.farm_block)

class WoodHoe(Hoe):
    material = G.WOODEN_TOOL
    tool_type = G.HOE
    max_stack_size = 1
    id = 290
    durability = 60
    name = "Wooden Hoe"
    icon_name = "hoeWood"

class StoneHoe(Hoe):
    material = G.STONE_TOOL
    tool_type = G.HOE
    max_stack_size = 1
    id = 291
    durability = 40
    name = "Stone Hoe"
    icon_name = "hoeStone"

class IronHoe(Hoe):
    material = G.IRON_TOOL
    tool_type = G.HOE
    max_stack_size = 1
    id = 292
    durability = 40
    name = "Iron Hoe"
    icon_name = "hoeIron"

class DiamondHoe(Hoe):
    material = G.DIAMOND_TOOL
    tool_type = G.HOE
    max_stack_size = 1
    id = 293
    durability = 100
    name = "Diamond Hoe"
    icon_name = "hoeDiamond"

class GoldenHoe(Hoe):
    material = G.GOLDEN_TOOL
    tool_type = G.HOE
    max_stack_size = 1
    id = 294
    durability = 100
    name = "Golden Hoe"
    icon_name = "hoeGold"

class Armor(Item):
    material = None
    defense_point = 0
    armor_type = None
    max_stack_size = 1

    def __init__(self):
        super(Armor, self).__init__()

class IronHelmet(Armor):
    material = G.IRON_TOOL
    defense_point = 1
    armor_type = G.HELMET
    id = 306
    name = "Iron Helmet"
    icon_name = "helmetIron"

class IronChestplate(Armor):
    material = G.IRON_TOOL
    defense_point = 3
    armor_type = G.CHESTPLATE
    id = 307
    name = "Iron Chestplate"
    icon_name = "chestplateIron"

class IronLeggings(Armor):
    material = G.IRON_TOOL
    defense_point = 2.5
    armor_type = G.LEGGINGS
    id = 308
    name = "Iron Leggings"
    icon_name = "leggingsIron"

class IronBoots(Armor):
    material = G.IRON_TOOL
    defense_point = 1
    armor_type = G.BOOTS
    id = 309
    name = "Iron Boots"
    icon_name = "bootsIron"

##Emerald Armor .. Pretty much re-textured Iron armor (from Tekkit)

#class EmeraldHelmet(Armor):
    #material = globals.IRON_TOOL
    #defense_point = 1
    #armor_type = globals.HELMET
    #id = 306.1
    #name = "Emerald Helmet"

#class EmeraldChestplate(Armor):
    #material = globals.IRON_TOOL
    #defense_point = 3
    #armor_type = globals.CHESTPLATE
    #id = 307.1
    #name = "Emerald Chestplate"

#class EmeraldLeggings(Armor):
    #material = globals.IRON_TOOL
    #defense_point = 2.5
    #armor_type = globals.LEGGINGS
    #id = 308.1
    #name = "Emerald Leggings"

#class EmeraldBoots(Armor):
    #material = globals.IRON_TOOL
    #defense_point = 1
    #armor_type = globals.BOOTS
    #id = 309.1
    #name = "Emerald Boots"

@G.initializer
def _init(M):
    M.coal_item = CoalItem()
    M.diamond_item = DiamondItem()
    M.stick_item = StickItem()
    M.iron_ingot_item = IronIngotItem()
    M.gold_ingot_item = GoldIngotItem()
    M.flint_item = FlintItem()
    M.wood_axe = WoodAxe()
    M.stone_axe = StoneAxe()
    M.iron_axe = IronAxe()
    M.diamond_axe = DiamondAxe()
    M.golden_axe = GoldenAxe()
    M.wood_pickaxe = WoodPickaxe()
    M.stone_pickaxe = StonePickaxe()
    M.iron_pickaxe = IronPickaxe()
    M.diamond_pickaxe = DiamondPickaxe()
    M.golden_pickaxe = GoldenPickaxe()
    M.wood_shovel = WoodShovel()
    M.stone_shovel = StoneShovel()
    M.iron_shovel = IronShovel()
    M.diamond_shovel = DiamondShovel()
    M.golden_shovel = GoldenShovel()
    M.wood_hoe = WoodHoe()
    M.stone_hoe = StoneHoe()
    M.iron_hoe = IronHoe()
    M.diamond_hoe = DiamondHoe()
    M.golden_hoe = GoldenHoe()
    M.iron_helmet = IronHelmet()
    M.iron_chestplate = IronChestplate()
    M.iron_leggings = IronLeggings()
    M.iron_boots = IronBoots()
    #M.emerald_helmet = EmeraldHelmet()
    #M.emerald_chestplace = EmeraldChestplate()
    #M.emerald_leggings = EmeraldLeggings()
    #M.emerald_boots = EmeraldBoots()
    M.yellowdye_item = YellowDyeItem()
    M.ladder_item = LadderItem()
    M.ladder_item = LadderItem()
    M.reddye_item = RedDyeItem()
    M.sugar_item = SugarItem()
    M.paper_item = PaperItem()
    M.wheat_seed_item = WheatSeedItem()
    M.wheat_item = WheatItem()
    M.bread_item = BreadItem()
    M.potato_item = PotatoItem()
    M.carrot_item = CarrotItem()
    M.bone_meal_item = BoneMeal()


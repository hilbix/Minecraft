# Imports, sorted alphabetically.

# Python packages
# Nothing for now...

# Third-party packages
# Nothing for now...

# Modules from this project
import blocks as B
import globals as G
import items as I


__all__ = (
    'Recipe', 'Recipes', 'SmeltingRecipe', 'SmeltingRecipes',
)


class Recipe(object):
    # ingre is a list that contains the ids of the ingredients
    # e.g. [[2, 2], [1, 1]]
    def __init__(self, ingre, output):
        # what blocks are needed to craft this block/item
        self.ingre = ingre
        self.output = output
        self.shapeless = False

    def __repr__(self):
        return 'Ingredients: ' + str(self.ingre) + '; Output: ' + str(self.output)

class Recipes(object):
    def __init__(self):
        self.nr_recipes = 0
        self.recipes = []

    def remove_empty_line_col(self, ingre_list):
        # remove empty lines
        if len(ingre_list) == 0:
            return

        for i in (0, -1):
            line = ingre_list[i]
            if len(line) == 0:
                continue
            isempty = True
            for id in line:
                if id: isempty = False
            if isempty:
                ingre_list.pop(i)

        #remove empty column
        for i in (0, -1):
            isempty = True
            for line in ingre_list:
                if len(line) == 0:
                    continue
                if line[i]: isempty = False
            if isempty:
                for line in ingre_list:
                    if len(line) == 0:
                        continue
                    line.pop(i)

    def parse_recipe(self, shape, ingre):
        ingre_list = []

        for line in shape:
            sub_ingre = []

            # line length should not be greater than 3
            if len(line) > 3:
                print('add_recipe(): line length should be <= 3!')
                return

            for c in line:
                if c == ' ':
                    sub_ingre.append(B.air_block.id)
                else:
                    sub_ingre.append(ingre[c].id)
            ingre_list.append(sub_ingre)

        self.remove_empty_line_col(ingre_list)

        return ingre_list

    def add_recipe(self, shape, ingre, output):
        self.recipes.append(Recipe(self.parse_recipe(shape, ingre), output))
        self.nr_recipes += 1

    def add_shapeless_recipe(self, ingre, output):
        ingre_list = [x.id for x in ingre if x.id]
        ingre_list.sort()
        r = Recipe(ingre_list, output)
        r.shapeless = True
        self.recipes.append(r)

    def craft(self, input_blocks):
        id_list = []
        shapeless_id_list = []
        for line in input_blocks:
            id_list.append([b.id for b in
                            line])    # removed b.id != 0: it may make the
                            # shape different
            shapeless_id_list.extend([b.id for b in line if b.id])
        shapeless_id_list.sort()

        self.remove_empty_line_col(id_list)
        for r in self.recipes:
            if r.shapeless:
                if r.ingre == shapeless_id_list:
                    return r.output
            else:
                if r.ingre == id_list:
                    return r.output

        return None

    def dump(self):
        for recipe in self.recipes:
            print recipe

class SmeltingRecipe(object):
    def __init__(self, ingre, output):
        # what blocks are needed to craft this block/item
        self.ingre = ingre
        self.output = output


class SmeltingRecipes(object):
    def __init__(self):
        self.nr_recipes = 0
        self.recipes = []

    def add_recipe(self, ingre, output):
        self.recipes.append(SmeltingRecipe(ingre, output))
        self.nr_recipes += 1

    def smelt(self, ingre):
        for r in self.recipes:
            if r.ingre == ingre:
                return r.output

        return None


@G.initializer
def _init(M):
    G.recipes = Recipes()
    G.smelting_recipes = SmeltingRecipes()

    IS = I.ItemStack
    AR = G.recipes.add_recipe
    LR = G.recipes.add_shapeless_recipe
    MR = G.smelting_recipes.add_recipe

    # stone items

    AR(["##", "##"],          {'#': B.stone_block},  IS(B.stonebrick_block.id,     amount=4))
    AR(["###", "# #", "###"], {'#': B.cobble_block}, IS(B.furnace_block.id,        amount=1))
    AR(["##", "##"],          {'#': B.quartz_block}, IS(B.quartzbrick_block.id,    amount=4))
    AR(["#", "#"],            {'#': B.quartz_block}, IS(B.quartzcolumn_block.id,   amount=2))
    AR(["#", "#", "#"],       {'#': B.quartz_block}, IS(B.quartzcolumn_block.id,   amount=3))
    AR(["   ", "   ", "###"], {'#': B.quartz_block}, IS(B.quartzchiseled_block.id, amount=3))
    
    #9 ores to blocks
    
    AR(["###", "###", "###"], {'#': I.iron_ingot_item}, IS(B.iron_block.id,    amount=1))
    AR(["###", "###", "###"], {'#': I.gold_ingot_item}, IS(B.gold_block.id,    amount=1))
    AR(["###", "###", "###"], {'#': I.diamond_item},    IS(B.diamond_block.id, amount=1))

    # block back to 9 ores

    LR((B.diamond_block,), IS(I.diamond_item.id,    amount=9))
    LR((B.iron_block,),    IS(I.iron_ingot_item.id, amount=9))
    LR((B.gold_block,),    IS(I.gold_ingot_item.id, amount=9))

    # wood items

    LR((B.birchwood_block,),  IS(B.birchwoodplank_block.id,  amount=4))
    LR((B.junglewood_block,), IS(B.junglewoodplank_block.id, amount=4))
    LR((B.oakwood_block,),    IS(B.oakwoodplank_block.id,    amount=4))

    AR(["#", "#"],            {'#': B.oakwoodplank_block},    IS(I.stick_item.id,  amount=4))
    AR(["#", "#"],            {'#': B.junglewoodplank_block}, IS(I.stick_item.id,  amount=4))
    AR(["#", "#"],            {'#': B.oakwoodplank_block},    IS(I.stick_item.id,  amount=4))
    AR(["#", "#"],            {'#': B.oakwoodplank_block},    IS(I.stick_item.id,  amount=4))
    AR(["###", "# #", "###"], {'#': B.birchwoodplank_block},  IS(B.chest_block.id, amount=1))
    AR(["###", "# #", "###"], {'#': B.oakwoodplank_block},    IS(B.chest_block.id, amount=1))
    AR(["###", "# #", "###"], {'#': B.junglewoodplank_block}, IS(B.chest_block.id, amount=1))
    AR(["##", "##"],          {'#': B.birchwoodplank_block},  IS(B.craft_block.id, amount=1))
    AR(["##", "##"],          {'#': B.oakwoodplank_block},    IS(B.craft_block.id, amount=1))
    AR(["##", "##"],          {'#': B.junglewoodplank_block}, IS(B.craft_block.id, amount=1))
    AR(["# #", "###", "# #"], {'#': I.stick_item},            IS(I.ladder_item.id, amount=4))

    for material, toolset in [(I.diamond_item,    [I.diamond_pickaxe, I.diamond_axe, I.diamond_shovel, I.diamond_hoe]),
                              (B.cobble_block,    [I.stone_pickaxe,   I.stone_axe,   I.stone_shovel,   I.stone_hoe]),
                              (I.iron_ingot_item, [I.iron_pickaxe,    I.iron_axe,    I.iron_shovel,    I.iron_hoe]),
                              (I.gold_ingot_item, [I.golden_pickaxe,  I.golden_axe,  I.golden_shovel,  I.golden_hoe])]:

        AR(["###", " @ ", " @ "], {'#': material, '@': I.stick_item}, IS(toolset[0].id,  amount=1))
        AR(["## ", "#@ ", " @ "], {'#': material, '@': I.stick_item}, IS(toolset[1].id,  amount=1))
        AR([" # ", " @ ", " @ "], {'#': material, '@': I.stick_item}, IS(toolset[2].id,  amount=1))
        AR(["## ", " @ ", " @ "], {'#': material, '@': I.stick_item}, IS(toolset[-1].id, amount=1))
    
    # armors

    for material, armors in [(I.iron_ingot_item, [I.iron_helmet, I.iron_chestplate, I.iron_leggings, I.iron_boots])]:

        AR(["###", "# #"],        {'#': material}, IS(armors[0].id,  amount=1))
        AR(["# #", "###", "###"], {'#': material}, IS(armors[1].id,  amount=1))
        AR(["###", "# #", "# #"], {'#': material}, IS(armors[2].id,  amount=1))
        AR(["# #", "# #"],        {'#': material}, IS(armors[-1].id, amount=1))
    
    # wood items
    
    for wood in (B.birchwoodplank_block, B.junglewoodplank_block, B.oakwoodplank_block):

        AR(["#", "#"],            {'#': wood},                    IS(I.stick_item.id,   amount=4))
        AR(["###", "# #", "###"], {'#': wood},                    IS(B.chest_block.id,  amount=1))
        AR(["##", "##"],          {'#': wood},                    IS(B.craft_block.id,  amount=1))
        AR(["###", " @ ", " @ "], {'#': wood, '@': I.stick_item}, IS(I.wood_pickaxe.id, amount=1))
        AR(["## ", "#@ ", " @ "], {'#': wood, '@': I.stick_item}, IS(I.wood_axe.id,     amount=1))
        AR([" # ", " @ ", " @ "], {'#': wood, '@': I.stick_item}, IS(I.wood_shovel.id,  amount=1))
    
    # sand items
    
    AR(["##", "##"], {'#': B.sand_block}, IS(B.sandstone_block.id, amount=1))
    
    # plants items

    AR(["#"],                {'#': B.yflowers_block}, IS(I.yellowdye_item.id, amount=2))
    AR(["#"],                {'#': B.rose_block},     IS(I.reddye_item.id,    amount=2))
    AR(["#"],                {'#': B.reed_block},     IS(I.sugar_item.id,     amount=1))
    AR(["   ","   ", "###"], {'#': B.reed_block},     IS(I.paper_item.id,     amount=4))
    AR(["   ","   ", "###"], {'#': I.wheat_item},     IS(I.bread_item.id,     amount=1))
    
    # combined items

    AR(["#", "@"], {'#': I.coal_item, '@': I.stick_item}, IS(B.torch_block.id, amount=4))
    
    # smelting items

    MR(B.ironore_block, IS(I.iron_ingot_item.id, amount=1))
    MR(B.cobble_block,  IS(B.stone_block.id,     amount=1))


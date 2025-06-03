from enum import Enum

class Name(Enum):
    # UI
    MAKE_STATUE = "Make Statue"
    DISCOVER_KNOWLEDGE = "Discover"

    # ATRIBUTES
    CHAOS = "Chaos"
    CREATIVITY = "Creativity"
    HEALTH = "Health"
    MAGIC = "Magic"
    COURAGE = "Courage"

    # RESOURCES
    LOG = "Log"
    WATER = "Water"
    DIRT = "Dirt"
    CLAY = "Clay"
    STONE = "Stone"
    LIMESTONE = "Limestone"
    FLINT = "Flint"
    MALACHITE = "Malachite"
    LUMBER = "Lumber"
    CHARCOAL = "Charcoal"
    PIT = "Pit"
    HEMP = "Hemp"
    OLDOWAN = "Oldowan"
    BAST_FIBER = "Bast fiber"
    METEORIC_IRON = "Meteoric iron"
    STONE_ANVIL = "Stone anvil"
    LIMESTONE_DUST = "Limestone dust"
    MALACHITE_DUST = "Malachite dust"
    FIRE = "Fire"
    THREAD = "Thread"
    WHEEL = "Wheel"
    SPINDLE = "Spindle"
    BOWL = "Bowl"
    POTTER_WHEEL = "Potter wheel"
    BRICK_MOLD = "Brick mold"
    RAW_BRICK = "Raw brick"
    FIRED_BRICK = "Fired brick"
    RAW_POTTERY = "Raw pottery"
    FIRED_POTTERY = "Fired pottery"
    LIME = "Lime"
    FABRIC = "Fabric"
    ROPE = "Rope"
    BELLOWS = "Bellows"
    CLOTHES = "Clothes"
    SAND = "Sand"
    MORTAR = "Mortar"
    HOUSE = "House"
    MEGALITH = "Megalith"
    COPPER_CHARCOAL_MIX = "Copper-charcoal mix"
    COPPER = "Copper"
    OBSERVATORY_1 = "Observatory 1"

    # WORKS
    GATHERER = "Gatherer"
    CROP_COLECTOR = "Crop colector"
    FLINT_KNAPPER = "Flint knapper"
    ARCHEOASTRONOMER = "Archeoastronomer"
    TREE_FELLER = "Tree feller"
    WOODWORKER__LUMBER = "Woodworker (Lumber)"
    WOODWORKER__BOWL = "Woodworker (Bowl)"
    WOODWORKER__WHEEL = "Woodworker (Wheel)"
    WOODWORKER__SPINDLE = "Woodworker (Spindle)"
    WOODWORKER__BRICK_MOLD = "Woodworker (Brick mold)"
    WOODWORKER__POTTER_WHEEL = "Woodworker (Potter wheel)"
    FIREKEEPER = "Firekeeper"
    DIGGER = "Digger"
    RETTER = "Retter"
    SURFACE_MINER = "Surface miner"
    CHARCOAL_BURNER = "Charcoal burner"
    SPINNER = "Spinner "
    ANVIL_MAKER = "Anvil maker"
    CRUSHER__LIMESTONE = "Crusher (Limestone)"
    CRUSHER__MALACHITE = "Crusher (Malachite)"
    BRICKMAKER = "Brickmaker"
    CLAY_FIRER__BRICK = "Clay firer (Brick)"
    CLAY_FIRER__POTTERY = "Clay firer (Pottery)"
    CALCINER = "Calciner"
    WEAVER = "Weaver"
    ROPE_MAKER = "Rope-maker"
    POTTER = "Potter"
    TAILOR__BELLOWS = "Tailor (Bellows)"
    TAILOR__CLOTHES = "Tailor (Clothes)"
    CRUSHER__STONE = "Crusher (Stone)"
    MORTAR_MIXER = "Mortar mixer"
    COPPER_SMELTER = "Copper smelter"
    COPPER_WASHER = "Copper washer"

    # MULTIWORKS
    CHARCOAL_PILE = "Charcoal pile"
    BUILDING = "Building"
    MEGALITH_DIGGING = "Megalith digging"
    OBSERVATORY_BUILDING_1 = "Observatory building 1"
    ASTRONOMICAL_OBSERVING = "Astronomical observing"

    # KNOWLEDGE
    CURIOSITY = "Curiosity"
    PLANT_IDENTIFICATION = "Plant identification"
    SHARP_IDEA = "Sharp idea"
    STAR_OBSERVATION = "Star observation"
    FOREST_SKILLS = "Forest skills"
    PYROTECHNOLOGY = "Pyrotechnology"
    EARTHLY_DESIRES = "Earthly desires"
    ABSTRACT_THOUGHT = "Abstract thought"
    ROT_AND_ROLL = "Rot & Roll"
    COOLER_ROCKS = "Cooler rocks!"
    BLACKEST_WOOD = "Blackest wood"
    REVOLUTION_REVOLUTION = "Revolution revolution"
    ATTENTION_YARNING = "Attention: Yarning"
    TO_BITES_AND_DUST = "To bites & dust"
    BRICK_BY_BRICK = "Brick by brick"
    TRIAL_BY_FIRE = "Trial-by-fire"
    FANCY_TANGLING = "Fancy tangling"
    NEVER_LOSE_ROPE = "Never lose rope"
    ARSONISTS_DREAM = "Arsonist's dream"
    POTTERY_RPM = "Pottery RPM"
    RAG_TO_RICHES = "Rag to riches"
    STICKY_GOOP_TECH = "Sticky goop tech"
    ARCHEO_ARCHITECT = "Archeo architect"
    MONUMENTAL_AMBITION = "Monumental ambition"
    CALCOLITHIC_MODE = "Calcolithic mode"
    THE_BEGGINING = "The Beggining"
    BRONZE_AGE_BEGGINS = "Bronze Age beggins"
#
#
#
#
#
#
#
#
#
#



resource = """
Log
Water
Dirt
Clay
Stone
Limestone
Flint
Malachite
Lumber
Charcoal
Pit
Hemp
Oldowan
Bast fiber
Meteoric iron
Stone anvil
Limestone dust
Malachite dust
Fire
Thread
Wheel
Spindle	Bowl
Potter wheel
Brick mold
Raw brick
Fired brick
Raw pottery
Fired pottery
Lime
Fabric
Rope
Bellows
Clothes
Sand
Mortar
Megalith
Copper-charcoal mix
Copper
Observatory 1
"""



knowledge = """
Curiosity
Plant identification
Sharp idea
Star observation
Forest skills
Pyrotechnology
Earthly desires
Abstract thought
Rot & Roll
Cooler rocks!
Blackest wood
Revolution revolution
Attention: Yarning
To bites & dust
Brick by brick
Trial-by-fire
Fancy tangling
Never lose rope
Arsonist's dream
Pottery RPM
Rag to riches
Sticky goop tech
Archeo architect
Monumental ambition
Calcolithic mode
The Beggining
Bronze Age beggins
"""



works = """
Gatherer
Crop colector
Flint knapper
Archeoastronomer
Tree feller
Woodworker (Lumber)
Woodworker (Bowl)
Firekeeper
Digger
Retter
Surface miner
Charcoal burner
Woodworker (Wheel)
Woodworker (Spindle)
Spinner 
Anvil maker
Crusher (Limestone)
Crusher (Malachite)
Woodworker (Brick mold)
Brickmaker
Clay firer (Brick)
Calciner
Weaver
Rope-maker
Woodworker (Potter wheel)
Potter
Clay firer (Pottery)
Tailor (Bellows)
Tailor (Clothes)
Crusher (Stone)
Mortar mixer
Copper smelter
Copper washer

Charcoal piling
Building
Megalith digging
Observatory building 1
Astronomical observing
"""


# for i in knowledge.split('\n'):
#     print(i.upper().replace(" ", "_").replace("(", "_").replace(")", "") )#+ ' = "' + i + '"')

text = """Crop colector
Flint knapper
Archeoastronomer
Tree feller;Woodworker (Lumber);Woodworker (Bowl)
Firekeeper
Digger
~
Retter
Surface miner
Charcoal burner
Woodworker (Wheel)
Woodworker (Spindle);Yarn spinner
Anvil maker;Crusher (Limestone);Crusher (Malachite)
Woodworker (Brick mold);Brickmaker;Clay firer (Brick)
Calciner
Weaver
Rope-maker
Charcoal pile builder
Woodworker (Potter wheel)
Potter;Clay firer (Pottery)
Tailor (Bellows);Tailor (Clothes)
Crusher (Stone)
Mortar mixer
Builder
Megalith digger
Copper smelter;Copper washer
Observatory building 1;Astronomical Observatory
"""


b = []
for row in text.split("\n"):
    b = []
    for i in row.split(';'):
        a = "Name." + i.upper().replace(" (", "__").replace(")", "").replace(" ", "_").replace("-","_")
        b.append(a)

    print(", ".join(b))
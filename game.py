from names import Name

"""
Objective: to define what is the full game multiwork that is updated through game loop* or player input*.
The game is organized as many dictionaries for quick hash search and light processing, as python OOP is not as optimized.
"""


def init_golems(material: Name, weakness: dict[str: float]={}, golems: int=5) -> dict:
    return {"material": material, # mud/clay,   water/charcoal?,   sandstone/quartzite,   stone,   copper,    granite/flint
            "weakness": weakness,   # Pensando em colocar algo como "golem upgrades" ou "architecture" 
            # "upgrades": upgrades,
            
            "birth dates": {0: golems},      # e ser um elemento mais complexo que contenha informações do golem.
            "death dates": {},      # Eu preciso também implementar o sistema de fraquezas e eventos.
            "statues": 0,           # o material dos golems vai estar intimamente associado 
            "statues due dates" : {}, # current_day + dev_time: number # {100: 10}
            "working idle": golems,
            "working busy": 0,
            "broken": 0
            }




# CHAOS:      element of surprise
# CREATIVITY: to progress in the game
# HEALTH:     pensando em mudar esse nome
# MAGIC:      to keep golems alive and balance progression
# COURAGE:    to gain land
def init_attributes() -> dict:                                                                    # dict[day that it ends: Name of the event]
    return {# Name.CHAOS: {"level": float, "random events": dict[Name: callable], "current events": dict[int: Name]},  # fica pra depois da matéria
            
            Name.CREATIVITY: {"points": 0, "all time points": 0},

            Name.HEALTH: {"level": 0, "samples": []},  # list[int or float]

            Name.MAGIC: {"capacity": 125, "flux": 30.0, "contained": 25},

            # Name.COURAGE: {"points": int},  # fica pra depois da matéria
            }




def init_event() -> dict:  # implementar depois da matéria?
    return {"ages possible": list[str],
            "chance": float,
            "start function": callable,
            "duration": int,
            "end function": callable}




def init_resource(is_tool: bool=False, breaking_chance: float=0.0, damage: int=0, protection: int=0, housing: int=0) -> dict: # Material, Tool, Equipment / Gear / Protection, Machine, Vehicle
    return {"unlocked": True,
            "quantity": 0,

            "is tool": is_tool,
            "breaking chance": breaking_chance,
            "in use": 0,
            "damage": damage,  # any tool can be used as a weapon, this is how good it is as a weapon  # will not be used as of now because of courage not being planned to be implemented yet
            "protection": protection,
            "housing": housing
            }




# for specialization: father work    think i'm gonna scrap that idea
def init_work(unlocked: bool=False, resources_cost: dict[Name: int]={}, resources_product: dict[Name: int]={}, flux_cost: int=0, flux_product: int=0, tools: list[Name]=[], energy_cost: int=0, energy_product: int=0) -> dict:
    return {"unlocked": unlocked,
            "golems working": 0,
            "in multiworks": {},

            "resources cost": resources_cost,
            "resources product": resources_product, # CONSTANT -> dict[Name: int]     |     LOOT -> dict["iterations": int, Name: float] Obs: the float sum is 1
            "flux cost": flux_cost,
            "flux product": flux_product,           # always with the function that slows down the flux production by the closer you are to the capacity
            "tools": tools,
            "energy cost": energy_cost,
            "energy product": energy_product,
            # "enough": {"resources": bool, "flux": bool, "tools": bool, "energy": bool}
            }




# for multiwork: workers, land taken
def init_multiwork(worker_type: Name=None, workers_needed: int=0, land_needed: int=0, building_cost: dict[Name: int]={}, resources_cost: dict[Name: int]={}, resources_product: dict[Name: int]={}, flux_cost: int=0, flux_product: int=0, tools: dict[Name: int]={}, energy_cost: int=0, energy_product: int=0) -> dict:
    return {"unlocked": False,
            "quantity": 0,
            "land needed": land_needed,             # only occupied while the multiwork is built, deocuppied when multiwork is destroyed
            "building cost": building_cost,         # consumed only at creation

            "worker type": worker_type,             # ainda to pensando qq eu faço com isso aqui, será q eu faço uma lista?
            "workers needed": workers_needed,       # number of workers needed to activate production

            "resources cost": resources_cost,       # consumed daily
            "resources product": resources_product, # CONSTANT -> dict[Name: int]     |     LOOT -> dict["iterations": int, Name: float] Obs: the float sum is 1
            "flux cost": flux_cost,
            "flux product": flux_product,           # always with the function that slows down the flux production by the closer you are to the capacity
            "tools": tools,
            "energy usage": energy_cost,
            "energy product": energy_product,
            # "enough": {"resources": bool, "flux": bool, "tools": bool, "energy": bool}
            }




def init_knowledge(unlocked: bool=False, learned: bool=False, dependencies: list[Name]=[], work_unlocked: list[Name]=[], multiwork_unlocked: list[Name]=[], effect: callable=None, creativity_cost: int=0, flux_cost: int=0, resources_cost: dict[Name: int]={}) -> dict:
    return {"unlocked": unlocked,
            "learned": learned,
            "dependencies": dependencies,
            "work unlocked": work_unlocked,             # maybe change to be "unlocked": {"work" or "multiworks": Name} with a single key dictionary
            "multiwork unlocked": multiwork_unlocked,
            "effect": effect,  # something that happens when you learn | for ages, there will be an "change_age()" effect, etc
            "creativity cost": creativity_cost,
            "flux cost": flux_cost,
            "resources cost": resources_cost,
            }








def init_game() -> dict:
    return {"new game": True,
            "ascension state": True,
            "language": "en",
            
            "metadata": {"ascension points": 0,
                         "golem upgrades": None, # add later, dict
                         "golems unlocked": None # add later, dict
                         },

            "data": {"age": 0,
                     
                     "current day": 0,
                     
                     "golems": init_golems(material=Name.DIRT, 
                                           weakness={"erosion":     1e-4,
                                                     "wild beast":  1e-4,
                                                     "rusting":     1e-4,
                                                     "freezing":    1e-4,
                                                     "burning":     1e-4
                                                     }, 
                                            golems=5
                                            ),

                     "land": {"busy": 0, "idle": 16},  # x4 toda era 16 * 4**"age"      age 6: 4**6

                     "energy": {"usage": {}, "production": {}},  # units producing: {nome de estrutura/trabalho: unidades ativas * watts}
                     
                     "attributes": init_attributes(),

                     "resources": {
                         Name.LOG: init_resource(),
                         Name.WATER: init_resource(),
                         Name.DIRT: init_resource(),
                         Name.CLAY: init_resource(),
                         Name.STONE: init_resource(),
                         Name.LIMESTONE: init_resource(),
                         Name.FLINT: init_resource(),
                         Name.MALACHITE: init_resource(),
                         Name.LUMBER: init_resource(),
                         Name.CHARCOAL: init_resource(),
                         Name.PIT: init_resource(is_tool=True, breaking_chance=0.25),
                         Name.HEMP: init_resource(),
                         Name.OLDOWAN: init_resource(is_tool=True, breaking_chance=0.2),
                         Name.BAST_FIBER: init_resource(),
                         Name.METEORIC_IRON: init_resource(),
                         Name.STONE_ANVIL: init_resource(is_tool=True, breaking_chance=0.15),
                         Name.LIMESTONE_DUST: init_resource(),
                         Name.MALACHITE_DUST: init_resource(),
                         Name.FIRE: init_resource(),
                         Name.THREAD: init_resource(),
                         Name.WHEEL: init_resource(is_tool=True, breaking_chance=0.12),
                         Name.SPINDLE: init_resource(is_tool=True, breaking_chance=0.1),
                         Name.BOWL: init_resource(is_tool=True, breaking_chance=0.1),
                         Name.POTTER_WHEEL: init_resource(is_tool=True, breaking_chance=0.04),
                         Name.BRICK_MOLD: init_resource(is_tool=True, breaking_chance=0.1),
                         Name.RAW_BRICK: init_resource(),
                         Name.FIRED_BRICK: init_resource(),
                         Name.RAW_POTTERY: init_resource(),
                         Name.FIRED_POTTERY: init_resource(is_tool=True, breaking_chance=0.15),
                         Name.LIME: init_resource(),
                         Name.FABRIC: init_resource(),
                         Name.ROPE: init_resource(is_tool=True, breaking_chance=0.1),
                         Name.BELLOWS: init_resource(is_tool=True, breaking_chance=0.07),
                         Name.CLOTHES: init_resource(),
                         Name.SAND: init_resource(),
                         Name.MORTAR: init_resource(),
                         Name.MEGALITH: init_resource(),
                         Name.COPPER_CHARCOAL_MIX: init_resource(),
                         Name.COPPER: init_resource(),
                         Name.OBSERVATORY_1: init_resource(is_tool=True, breaking_chance=0),
                     },

                     "priorities": {Name.GATHERER: "works"}, # works and multiworks

                     "works": {
                         Name.GATHERER: init_work(
                            unlocked=True,
                            resources_product={
                                "iterations": 2,
                                Name.WATER: 0.2,
                                Name.DIRT: 0.2,
                                Name.LOG: 0.15,
                                Name.CLAY: 0.15,
                                Name.STONE: 0.15,
                                Name.LIMESTONE: 0.075,
                                Name.FLINT: 0.075
                            },
                         ),

                         Name.CROP_COLECTOR: init_work(
                            resources_product={Name.HEMP: 5},
                         ),

                         Name.FLINT_KNAPPER: init_work(
                            resources_cost={Name.FLINT: 2, Name.STONE: 3},
                            resources_product={Name.OLDOWAN: 1},
                         ),

                         Name.ARCHEOASTRONOMER: init_work(
                            resources_product={
                                "iterations": 1,
                                Name.METEORIC_IRON: 0.01,
                                "nothing": 0.99},
                            flux_product=0.1,
                         ),

                         Name.TREE_FELLER: init_work(
                            resources_product={Name.LOG: 1},
                            tools=[Name.OLDOWAN]
                         ),

                         Name.WOODWORKER__LUMBER: init_work(
                            resources_cost={Name.LOG: 2},
                            resources_product={Name.LUMBER: 2},
                            tools=[Name.OLDOWAN]
                         ),

                         Name.WOODWORKER__BOWL: init_work(
                            resources_cost={Name.LUMBER: 3},
                            resources_product={Name.BOWL: 1},
                            tools=[Name.OLDOWAN]
                         ),

                         Name.FIREKEEPER: init_work(
                            resources_cost={Name.LOG:10},
                            resources_product={Name.FIRE:1},
                            tools=[Name.OLDOWAN]
                         ),

                         Name.DIGGER: init_work(
                            resources_product={
                                "iterations": 2,
                                Name.DIRT:0.62,
                                Name.CLAY:0.33,
                                Name.PIT:0.05
                            },
                            tools=[Name.OLDOWAN]
                         ),

                         Name.RETTER: init_work(
                            resources_cost={Name.HEMP:3,Name.WATER:5},
                            resources_product={Name.BAST_FIBER:2},
                            tools=[Name.BOWL]
                         ),

                         Name.SURFACE_MINER: init_work(
                            resources_product={
                                "iterations":2,
                                Name.STONE:0.4,
                                Name.LIMESTONE:0.25,
                                Name.FLINT:0.25,
                                Name.MALACHITE:0.1
                            },
                            tools=[Name.OLDOWAN]
                         ),

                         Name.CHARCOAL_BURNER: init_work(
                            resources_cost={Name.FIRE:1, Name.LOG:3},
                            resources_product={Name.CHARCOAL:2},
                            tools=[Name.PIT]
                         ),

                         Name.WOODWORKER__WHEEL: init_work(
                            resources_cost={Name.LUMBER:5},
                            resources_product={Name.WHEEL:1},
                            tools=[Name.OLDOWAN]
                         ),

                         Name.WOODWORKER__SPINDLE: init_work(
                            resources_cost={Name.LUMBER:3},
                            resources_product={Name.SPINDLE:1},
                            tools=[Name.OLDOWAN]
                         ),

                         Name.SPINNER: init_work(
                            resources_cost={Name.BAST_FIBER:4},
                            resources_product={Name.THREAD:1},
                            tools=[Name.SPINDLE]
                         ),

                         Name.ANVIL_MAKER: init_work(
                            resources_cost={Name.FLINT:5, Name.STONE:10},
                            resources_product={Name.STONE_ANVIL:1},
                            tools=[Name.OLDOWAN]
                         ),

                         Name.CRUSHER__LIMESTONE: init_work(
                            resources_cost={Name.LIMESTONE:1},
                            resources_product={Name.LIMESTONE_DUST:1},
                            tools=[Name.STONE_ANVIL]
                         ),

                         Name.CRUSHER__MALACHITE: init_work(
                            resources_cost={Name.MALACHITE:1},
                            resources_product={Name.MALACHITE_DUST:1},
                            tools=[Name.STONE_ANVIL]
                         ),

                         Name.WOODWORKER__BRICK_MOLD: init_work(
                            resources_cost={Name.LUMBER:5},
                            resources_product={Name.BRICK_MOLD:1},
                            tools=[Name.OLDOWAN]
                         ),

                         Name.BRICKMAKER: init_work(
                            resources_cost={Name.CLAY:3},
                            resources_product={Name.RAW_BRICK:1},
                            tools=[Name.BRICK_MOLD]
                         ),

                         Name.CLAY_FIRER__BRICK: init_work(
                            resources_cost={Name.RAW_BRICK:1, Name.CHARCOAL:6, Name.FIRE:1},
                            resources_product={Name.FIRED_BRICK:1},
                            tools=[Name.PIT]
                         ),

                         Name.CALCINER: init_work(
                            resources_cost={Name.LIMESTONE_DUST:2, Name.FIRE:2},
                            resources_product={Name.LIME:2},
                            tools=[Name.PIT]
                         ),

                         Name.WEAVER: init_work(
                            resources_cost={Name.THREAD:8},
                            resources_product={Name.FABRIC:1},
                         ),

                         Name.ROPE_MAKER: init_work(
                            resources_cost={Name.THREAD:12},
                            resources_product={Name.ROPE:1},
                         ),

                         Name.WOODWORKER__POTTER_WHEEL: init_work(
                            resources_cost={Name.WHEEL:5, Name.LUMBER:20},
                            resources_product={Name.POTTER_WHEEL:1},
                            tools=[Name.OLDOWAN]
                         ),

                         Name.POTTER: init_work(
                            resources_cost={},
                            resources_product={},
                            tools=[Name.POTTER_WHEEL]
                         ),

                         Name.CLAY_FIRER__POTTERY: init_work(
                            resources_cost={Name.RAW_POTTERY:1, Name.CHARCOAL:6, Name.FIRE:1},
                            resources_product={Name.FIRED_POTTERY:1},
                            tools=[Name.PIT]
                         ),

                         Name.TAILOR__BELLOWS: init_work(
                            resources_cost={Name.FABRIC:8, Name.LUMBER:10, },
                            resources_product={Name.BELLOWS:1, },
                            tools=[Name.OLDOWAN]
                         ),

                         Name.TAILOR__CLOTHES: init_work(
                            resources_cost={Name.FABRIC:6, },
                            resources_product={Name.CLOTHES:1, },
                            tools=[Name.OLDOWAN]
                         ),

                         Name.CRUSHER__STONE: init_work(
                            resources_cost={Name.STONE:2, },
                            resources_product={Name.SAND:1, },
                            tools=[Name.STONE_ANVIL]
                         ),

                         Name.MORTAR_MIXER: init_work(
                            resources_cost={Name.SAND:5, Name.LIME:5, Name.WATER:5, },
                            resources_product={Name.MORTAR:2},
                            tools=[Name.FIRED_POTTERY]
                         ),

                         Name.COPPER_SMELTER: init_work(
                            resources_cost={Name.MALACHITE_DUST:3, Name.FIRE:1, Name.CHARCOAL:10, Name.DIRT:10, },
                            resources_product={Name.COPPER_CHARCOAL_MIX:1, },
                            tools=[Name.PIT, Name.BELLOWS]
                         ),

                         Name.COPPER_WASHER: init_work(
                            resources_cost={Name.COPPER_CHARCOAL_MIX:1, Name.WATER:5, },
                            resources_product={Name.COPPER:1},
                            tools=[Name.BOWL]
                         ),
                     },

                     "multiworks": {
                         Name.CHARCOAL_PILE: init_multiwork(
                             worker_type=Name.CHARCOAL_BURNER,
                             workers_needed=3,
                             resources_cost={Name.LOG: 15, Name.LUMBER: 4, Name.ROPE: 1, Name.FIRE: 1, Name.DIRT: 10, Name.CLAY: 5},
                             resources_product={Name.CHARCOAL: 15},
                         ),

                         Name.BUILDING: init_multiwork(
                             worker_type=Name.MORTAR_MIXER,
                             workers_needed=2,
                             resources_cost={Name.LUMBER: 4, Name.FIRED_BRICK: 4, Name.MORTAR:4},
                             resources_product={"iterations": 1, Name.HOUSE: 0.34, "nothing": 0.66},
                             tools={Name.OLDOWAN: 2}
                         ),

                         Name.MEGALITH_DIGGING: init_multiwork(
                             worker_type=Name.DIGGER,
                             workers_needed=3,
                             resources_product={
                                 "iterations": 6,
                                 Name.DIRT: 0.5,
                                 Name.CLAY: 0.35,
                                 Name.PIT: 0.1,
                                 Name.MEGALITH: 0.05
                             },
                             tools={Name.OLDOWAN: 3, Name.ROPE: 3, Name.WHEEL: 10}
                         ),

                         Name.OBSERVATORY_BUILDING_1: init_multiwork(
                             worker_type=Name.BRICKMAKER,
                             workers_needed=3,
                             resources_cost={Name.MEGALITH: 1, Name.STONE: 5, Name.LIMESTONE: 5, Name.LIME: 5},
                             resources_product={"iterations": 1, Name.OBSERVATORY_1: 0.03, "nothing": 0.97},
                             tools={Name.OLDOWAN: 3, Name.ROPE: 3, Name.WHEEL: 4}
                         ),

                         Name.ASTRONOMICAL_OBSERVING: init_multiwork(
                             worker_type=Name.ARCHEOASTRONOMER,
                             workers_needed=5,
                             flux_product=5,
                             tools={Name.OBSERVATORY_1}
                         ),
                     },

                     "knowledge": {
                         Name.CURIOSITY: init_knowledge(
                             unlocked=True,
                             learned=True,
                             work_unlocked=[Name.GATHERER]
                         ), 
 
                         Name.PLANT_IDENTIFICATION: init_knowledge(
                             dependencies=[Name.CURIOSITY],
                             work_unlocked=[Name.CROP_COLECTOR],
                             resources_cost={Name.LOG:10, Name.WATER:10}
                         ), 
 
                         Name.SHARP_IDEA: init_knowledge(
                             dependencies=[Name.CURIOSITY],
                             work_unlocked=[Name.FLINT_KNAPPER],
                             resources_cost={Name.STONE:10, Name.FLINT:10}
                         ), 
 
                         Name.STAR_OBSERVATION: init_knowledge(
                             dependencies=[Name.CURIOSITY],
                             work_unlocked=[Name.ARCHEOASTRONOMER],
                             flux_cost=5
                         ), 
 
                         Name.FOREST_SKILLS: init_knowledge(
                             dependencies=[Name.SHARP_IDEA],
                             work_unlocked=[Name.TREE_FELLER, Name.WOODWORKER__LUMBER, Name.WOODWORKER__BOWL],
                             resources_cost={Name.OLDOWAN:5, Name.LOG:20}
                         ), 
 
                         Name.PYROTECHNOLOGY: init_knowledge(
                             dependencies=[Name.SHARP_IDEA],
                             work_unlocked=[Name.FIREKEEPER],
                             resources_cost={Name.OLDOWAN:5, Name.LOG:30}
                         ), 
 
                         Name.EARTHLY_DESIRES: init_knowledge(
                             dependencies=[Name.SHARP_IDEA],
                             work_unlocked=[Name.DIGGER],
                             resources_cost={Name.OLDOWAN:5}
                         ), 
 
                         Name.ABSTRACT_THOUGHT: init_knowledge(
                             dependencies=[Name.STAR_OBSERVATION],
                             flux_cost=5
                         ), 
 
                         Name.ROT_AND_ROLL: init_knowledge(
                             dependencies=[Name.PLANT_IDENTIFICATION, Name.FOREST_SKILLS],
                             work_unlocked=[Name.RETTER],
                             resources_cost={Name.BOWL:5, Name.HEMP:50, Name.WATER:50}
                         ), 
 
                         Name.COOLER_ROCKS: init_knowledge(
                             dependencies=[Name.EARTHLY_DESIRES],
                             work_unlocked=[Name.SURFACE_MINER],
                             resources_cost={Name.OLDOWAN:5, Name.DIRT:20, Name.CLAY:10, Name.STONE:10, Name.LIMESTONE:10, Name.FLINT:5}
                         ), 
 
                         Name.BLACKEST_WOOD: init_knowledge(
                             dependencies=[Name.PYROTECHNOLOGY, Name.EARTHLY_DESIRES],
                             work_unlocked=[Name.CHARCOAL_BURNER],
                             resources_cost={Name.FIRE:5, Name.PIT:5, Name.LOG:20}
                         ), 
 
                         Name.REVOLUTION_REVOLUTION: init_knowledge(
                             dependencies=[Name.FOREST_SKILLS, Name.ABSTRACT_THOUGHT],
                             work_unlocked=[Name.WOODWORKER__WHEEL],
                             resources_cost={Name.LUMBER:20}
                         ), 
 
                         Name.ATTENTION_YARNING: init_knowledge(
                             dependencies=[Name.ROT_AND_ROLL],
                             work_unlocked=[Name.WOODWORKER__SPINDLE, Name.SPINNER],
                             resources_cost={Name.LUMBER:20, Name.BAST_FIBER:20}
                         ), 
 
                         Name.TO_BITES_AND_DUST: init_knowledge(
                             dependencies=[Name.COOLER_ROCKS],
                             work_unlocked=[Name.ANVIL_MAKER, Name.CRUSHER__LIMESTONE, Name.CRUSHER__MALACHITE],
                             resources_cost={Name.OLDOWAN:5, Name.STONE:20, Name.LIMESTONE:20, Name.MALACHITE:5}
                         ), 
 
                         Name.BRICK_BY_BRICK: init_knowledge(
                             dependencies=[Name.FOREST_SKILLS, Name.BLACKEST_WOOD],
                             work_unlocked=[Name.WOODWORKER__BRICK_MOLD, Name.BRICKMAKER, Name.CLAY_FIRER__BRICK],
                             resources_cost={Name.LUMBER:40, Name.CLAY:50, Name.FIRE:5, Name.CHARCOAL:10, Name.PIT:5}
                         ), 
 
                         Name.TRIAL_BY_FIRE: init_knowledge(
                             dependencies=[Name.PYROTECHNOLOGY, Name.TO_BITES_AND_DUST],
                             work_unlocked=[Name.CALCINER],
                             resources_cost={Name.FIRE:5, Name.LIMESTONE_DUST:20}
                         ), 
 
                         Name.FANCY_TANGLING: init_knowledge(
                             dependencies=[Name.ATTENTION_YARNING],
                             work_unlocked=[Name.WEAVER],
                             resources_cost={Name.THREAD:24}
                         ), 
 
                         Name.NEVER_LOSE_ROPE: init_knowledge(
                             dependencies=[Name.ATTENTION_YARNING],
                             work_unlocked=[Name.ROPE_MAKER],
                             resources_cost={Name.THREAD:36}
                         ), 
 
                         Name.ARSONISTS_DREAM: init_knowledge(
                             dependencies=[Name.BLACKEST_WOOD, Name.NEVER_LOSE_ROPE],
                             multiwork_unlocked=[Name.CHARCOAL_PILE],
                             resources_cost={Name.LOG:50, Name.LUMBER:20, Name.FIRE:5, Name.ROPE:5, Name.DIRT:80, Name.CLAY:30}
                         ), 
 
                         Name.POTTERY_RPM: init_knowledge(
                             dependencies=[Name.REVOLUTION_REVOLUTION, Name.BRICK_BY_BRICK],
                             work_unlocked=[Name.WOODWORKER__POTTER_WHEEL, Name.POTTER, Name.CLAY_FIRER__POTTERY],
                             resources_cost={Name.WHEEL:10, Name.LUMBER:20, Name.CLAY:20, Name.FIRE:5, Name.PIT:5}
                         ), 
 
                         Name.RAG_TO_RICHES: init_knowledge(
                             dependencies=[Name.FANCY_TANGLING],
                             work_unlocked=[Name.TAILOR__BELLOWS, Name.TAILOR__CLOTHES],
                             resources_cost={Name.FABRIC:10, Name.THREAD:15}
                         ), 
 
                         Name.STICKY_GOOP_TECH: init_knowledge(
                             dependencies=[Name.TRIAL_BY_FIRE, Name.POTTERY_RPM],
                             work_unlocked=[Name.CRUSHER__STONE, Name.MORTAR_MIXER],
                             resources_cost={Name.STONE:30, Name.LIME:10, Name.WATER:100, Name.FIRED_POTTERY:5}
                         ), 
 
                         Name.ARCHEO_ARCHITECT: init_knowledge(
                             dependencies=[Name.BRICK_BY_BRICK, Name.STICKY_GOOP_TECH],
                             multiwork_unlocked=[Name.BUILDING],
                             resources_cost={Name.FIRED_BRICK:15, Name.MORTAR:20}
                         ), 
 
                         Name.MONUMENTAL_AMBITION: init_knowledge(
                             dependencies=[Name.COOLER_ROCKS, Name.REVOLUTION_REVOLUTION, Name.NEVER_LOSE_ROPE],
                             multiwork_unlocked=[Name.MEGALITH_DIGGING],
                             resources_cost={Name.OLDOWAN:20, Name.WHEEL:40, Name.ROPE:10}
                         ), 
 
                         Name.CALCOLITHIC_MODE: init_knowledge(
                             dependencies=[Name.TO_BITES_AND_DUST, Name.ARSONISTS_DREAM, Name.RAG_TO_RICHES],
                             work_unlocked=[Name.COPPER_SMELTER, Name.COPPER_WASHER],
                             resources_cost={Name.FIRE:10, Name.PIT:10, Name.CHARCOAL:50, Name.BELLOWS:5, Name.BOWL:10, Name.WATER:100, Name.MALACHITE_DUST:30}
                         ), 
 
                         Name.THE_BEGGINING: init_knowledge(
                             dependencies=[Name.ARCHEO_ARCHITECT, Name.MONUMENTAL_AMBITION],
                             multiwork_unlocked=[Name.OBSERVATORY_BUILDING_1, Name.ASTRONOMICAL_OBSERVING],
                             resources_cost={Name.MEGALITH:5, Name.STONE:25, Name.LIMESTONE:25, Name.LIME:25}
                         ), 
 
                         Name.BRONZE_AGE_BEGGINS: init_knowledge(
                             dependencies=[Name.CALCOLITHIC_MODE, Name.THE_BEGGINING],
                             resources_cost={Name.OBSERVATORY_1:1, Name.COPPER:30}
                         ),
                     },
                    },
            }

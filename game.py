from names import Name

"""
Objective: to define what is the full game structure that is updated through game loop* or player input*.
The game is organized as many dictionaries for quick hash search and light processing, as python OOP is not as optimized.
"""


def init_golems(material: Name, weakness: dict[str: float]={}, golems: int=5) -> dict:
    return {"material": material,
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




def init_attributes() -> dict:
    return {Name.CHAOS: {"chaos level": int, "random events": dict[str: float]},
            Name.CREATIVITY: {"points": 0, # to progress in the game
                              "all time points": 0
                              },
            Name.HEALTH: {},
            Name.MAGIC: {"capacity": 1000, # to keep golems alive and balance progression
                         "flux": 1000.0,
                         "contained": 0
                         },
            Name.COURAGE: {"courage points": int}, # to gain land
            }




def init_resource(expiration_time: int) -> dict: # Material, Tool, Equipment / Gear / Protection, Machine, Vehicle
    return {"unlocked": False,
            "expiration dates": {}, # key = current day + expiration time + rand? | value = quantity produced in that day
            "expiration time": expiration_time,
            "quantity": 0,
            "in use": 0, # only used by tool and machine, also only used for computation purposes, no use for the player
            }




# for specialization: father work    think i'm gonna scrap that idea
def init_work(unlocked: bool=False, resources_cost: dict[Name: int]={}, resources_product: dict[Name: int]={}, flux_cost: int=0, flux_product: int=0, tools: list[Name]=[]) -> dict:
    return {"unlocked": unlocked,
            "golems working": 0,
            "in structures": {},
            "resources cost": resources_cost,
            "resources product": resources_product, # CONSTANT -> dict[Name: int]     |     LOOT -> dict["iterations": int, Name: float] Obs: the float sum is 1
            "flux cost": flux_cost,
            "flux product": flux_product,           # always with the function that slows down the flux production by the closer you are to the capacity
            "tools": tools # resource needed to activate production that is not consumed (like a catalyst)
            }




# for structure: workers, land taken
def init_structure(worker_type: Name=None, workers_needed: int=0, land_needed: int=0, building_cost: dict[Name: int]={}, resources_cost: dict[Name: int]={}, resources_product: dict[Name: int]={}, flux_cost: int=0, flux_product: int=0, tools: dict[Name: int]={}) -> dict:
    return {"unlocked": False,
            "quantity": 0,
            "worker type": worker_type,             # ainda to pensando qq eu faço com isso aqui
            "workers needed": workers_needed,       # number of workers needed to activate production
            "land needed": land_needed,             # only occuped while the structure is built, deocuppied when structure is destroyed
            "building cost": building_cost,         # consumed only at creation
            "resources cost": resources_cost,       # consumed daily
            "resources product": resources_product, # CONSTANT -> dict[Name: int]     |     LOOT -> dict["iterations": int, Name: float] Obs: the float sum is 1
            "flux cost": flux_cost,
            "flux product": flux_product,           # always with the function that slows down the flux production by the closer you are to the capacity
            "tools": tools # resource needed to activate production that is not consumed (like a catalyst)
            }




def init_knowledge(dependencies: list[Name]=[], work_unlocked: list[Name]=[], structure_unlocked: list[Name]=[], creativity_cost: int=0, flux_cost: int=0, resources_cost: dict[Name: int]={}) -> dict:
    return {"unlocked": False,
            "learned": False,
            "dependencies": dependencies,
            "work unlocked": work_unlocked,             # maybe change to be "unlocked": {"work" or "structures": Name} with a single key dictionary
            "structure unlocked": structure_unlocked,
            "creativity cost": creativity_cost,
            "flux cost": flux_cost,
            "resources cost": resources_cost,
            }




def init_game() -> dict:
    return {"ascension state": True,
            "language": "en",
            
            "metadata": {"ascension points": 0,
                         "golem upgrades": None, # add later, dict
                         "golems unlocked": None # add later, dict
                         },

            "data": {"current day": 0,
                     "golems": init_golems(material=Name.MUD, 
                                           weakness={"erosion": 1/700,
                                                     "wild beast": 1/300,
                                                     "rusting": 1/1000,
                                                     "freezing": 1/1000,
                                                     "burning": 1/10000
                                                     }, 
                                            golems=5
                                            ),

                     "land": {"busy": 0, "idle": 10},
                     "attributes": init_attributes(),

                     "resources": {Name.MUD: init_resource(100),
                                   Name.WOOD: init_resource(100),
                                   Name.WATER: init_resource(100),
                                   Name.STONE: init_resource(100),
                                   Name.SANDSTONE: init_resource(100),
                                   Name.GRANITE: init_resource(100),
                                   Name.LIMESTONE: init_resource(100),
                                   Name.TIN: init_resource(100),
                                   Name.COPPER: init_resource(100),
                                   
                                   Name.FLINT: init_resource(200),
                                   Name.MEAT: init_resource(30),
                                   Name.HIDE: init_resource(100),
                                   Name.CLAY: init_resource(200),
                                   Name.CHARCOAL: init_resource(300),
                                   Name.STONE_TOOLS: init_resource(150),
                                   Name.POTTERY: init_resource(200),
                                   Name.LOG: init_resource(300),
                                   Name.ROPE: init_resource(250),
                                   Name.DRIED_MEAT: init_resource(200),
                                   Name.PRIMITIVE_FURNACE: init_resource(500),
                                   Name.ASH: init_resource(400),
                                   Name.WOODEN_SPEAR: init_resource(150),
                                   Name.BOW: init_resource(150),

                                   Name.BRONZE: init_resource(200),
                                   },

                     "priorities": {Name.GATHERER: "works"}, # works and structures

                     "works": {Name.GATHERER: init_work(
                                    unlocked=True,
                                    resources_product={
                                        "iterations": 1, 
                                        Name.MUD: 0.2,       
                                        Name.WOOD: 0.2,      
                                        Name.WATER: 0.2, 
                                        Name.STONE: 0.09,     
                                        # Name.SANDSTONE: 0.09, 
                                        # Name.GRANITE: 0.09, 
                                        Name.LIMESTONE: 0.09, 
                                        Name.CLAY: 0.09, # aham
                                        Name.FLINT: 0.09, # ehem
                                        Name.TIN: 0.01,       
                                        Name.COPPER:0.03
                                    }
                                ),
                                
                                Name.LUMBERJACK: init_work(
                                    resources_cost={Name.STONE_TOOLS: 1},
                                    resources_product={Name.LOG: 2}
                                ),

                                Name.HUNTER: init_work(
                                    resources_cost={Name.WOODEN_SPEAR: 1},
                                    resources_product={Name.MEAT: 2, Name.HIDE: 1}
                                ),

                                Name.FLINT_KNAPPER: init_work(
                                    resources_cost={Name.FLINT: 2},
                                    resources_product={Name.STONE_TOOLS: 1}
                                ),

                                Name.POTTERY_MAKER: init_work(
                                    resources_cost={Name.CLAY: 3},
                                    resources_product={Name.POTTERY: 1}
                                ),

                                Name.CHARCOAL_MAKER: init_work(
                                    resources_cost={Name.LOG: 4},
                                    resources_product={Name.CHARCOAL: 2, Name.ASH: 1}
                                ),

                                Name.MINER: init_work(
                                    resources_cost={Name.STONE_TOOLS: 1},
                                    resources_product={"iterations": 1,
                                                       Name.COPPER: 0.7,
                                                       Name.TIN: 0.3}
                                ),

                                Name.TOOL_MAKER: init_work(
                                    resources_cost={Name.WOOD: 2, Name.STONE: 2},
                                    resources_product={Name.STONE_TOOLS: 2}
                                ),

                                Name.SPEAR_MAKER: init_work(
                                    resources_cost={Name.WOOD: 3, Name.FLINT: 1},
                                    resources_product={Name.WOODEN_SPEAR: 1}
                                ),

                                Name.BOWYER: init_work(
                                    resources_cost={Name.WOOD: 4, Name.ROPE: 2},
                                    resources_product={Name.BOW: 1}
                                ),

                                Name.ROPE_MAKER: init_work(
                                    resources_cost={Name.HIDE: 2},
                                    resources_product={Name.ROPE: 2}
                                ),

                                Name.MEAT_DRIER: init_work(
                                    resources_cost={Name.MEAT: 2, Name.ASH: 1},
                                    resources_product={Name.DRIED_MEAT: 2}
                                ),

                                Name.BUILDER: init_work(
                                    resources_cost={Name.POTTERY: 10, Name.STONE: 10},
                                    resources_product={Name.PRIMITIVE_FURNACE: 1}
                                ),

                                Name.FURNACE_OPERATOR: init_work(
                                    resources_cost={Name.CHARCOAL: 5, Name.COPPER: 4, Name.TIN: 2, Name.PRIMITIVE_FURNACE: 1},
                                    resources_product={Name.BRONZE: 1}
                                ),
                               },

                     "structures": {},

                     "knowledge": {
                        Name.WOOD_CUTTING: init_knowledge(
                            dependencies=[],
                            work_unlocked=[Name.LUMBERJACK],
                            creativity_cost=5
                        ),

                        Name.FLINT_PROCESSING: init_knowledge(
                            dependencies=[],
                            work_unlocked=[Name.FLINT_KNAPPER],
                            creativity_cost=5
                        ),

                        Name.PRIMITIVE_WEAPONS: init_knowledge(
                            dependencies=[Name.FLINT_PROCESSING, Name.WOOD_CUTTING],
                            work_unlocked=[Name.SPEAR_MAKER],
                            creativity_cost=8
                        ),

                        Name.BASIC_HUNTING: init_knowledge(
                            dependencies=[Name.PRIMITIVE_WEAPONS],
                            work_unlocked=[Name.HUNTER],
                            creativity_cost=10
                        ),

                        Name.LEATHER_WORKING: init_knowledge(
                            dependencies=[Name.BASIC_HUNTING],
                            work_unlocked=[Name.ROPE_MAKER],
                            creativity_cost=8
                        ),

                        Name.BOW_MAKING: init_knowledge(
                            dependencies=[Name.LEATHER_WORKING, Name.WOOD_CUTTING],
                            work_unlocked=[Name.BOWYER],
                            creativity_cost=12
                        ),

                        Name.FIRE_CONTROL: init_knowledge(
                            dependencies=[Name.WOOD_CUTTING],
                            work_unlocked=[Name.CHARCOAL_MAKER],
                            creativity_cost=10
                        ),

                        Name.DRYING_TECHNIQUES: init_knowledge(
                            dependencies=[Name.FIRE_CONTROL, Name.BASIC_HUNTING],
                            work_unlocked=[Name.MEAT_DRIER],
                            creativity_cost=8
                        ),

                        Name.CLAY_WORKING: init_knowledge(
                            dependencies=[],
                            work_unlocked=[Name.POTTERY_MAKER],
                            creativity_cost=6
                        ),

                        Name.BASIC_MINING: init_knowledge(
                            dependencies=[Name.FLINT_PROCESSING],
                            work_unlocked=[Name.MINER],
                            creativity_cost=10
                        ),

                        Name.BASIC_TOOL_MAKING: init_knowledge(
                            dependencies=[Name.FLINT_PROCESSING, Name.WOOD_CUTTING],
                            work_unlocked=[Name.TOOL_MAKER],
                            creativity_cost=10
                        ),

                        Name.FOOD_PRESERVATION: init_knowledge(
                            dependencies=[Name.DRYING_TECHNIQUES, Name.CLAY_WORKING],
                            work_unlocked=[],
                            creativity_cost=10,
                            resources_cost={Name.POTTERY: 10, Name.DRIED_MEAT: 10}
                        ),

                        Name.KILN_CONSTRUCTION: init_knowledge(
                            dependencies=[Name.CLAY_WORKING, Name.FIRE_CONTROL],
                            work_unlocked=[Name.BUILDER],
                            creativity_cost=15,
                            resources_cost={Name.CLAY: 30, Name.STONE: 30}
                        ),

                        Name.SMELTING_PREPARATIONS: init_knowledge(
                            dependencies=[Name.BASIC_MINING, Name.FIRE_CONTROL],
                            work_unlocked=[],
                            creativity_cost=15,
                            resources_cost={Name.CHARCOAL: 25, Name.COPPER: 15, Name.TIN: 10}
                        ),

                        Name.FURNACE_BUILDING: init_knowledge(
                            dependencies=[Name.KILN_CONSTRUCTION, Name.SMELTING_PREPARATIONS],
                            work_unlocked=[Name.FURNACE_OPERATOR],
                            creativity_cost=20,
                            resources_cost={Name.STONE: 40, Name.CLAY: 20, Name.CHARCOAL: 20}
                        ),

                        Name.BRONZE_SMELTING: init_knowledge(
                            dependencies=[Name.FURNACE_BUILDING],
                            work_unlocked=[],
                            creativity_cost=25,
                            resources_cost={Name.COPPER: 20, Name.TIN: 10, Name.CHARCOAL: 20}
                        )
                    },
                     },
            }




game = init_game()

resources = game["data"]["resources"]

unlocked_resources = {key: value["unlocked"] for key, value in game["data"]["resources"].items()}

print(unlocked_resources)
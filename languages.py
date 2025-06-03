from names import Name

"""
The "languages" dictionary is ready to be imported to any other code.
Each key is the language abreviation, and contains the constant Name of the items that will be called by whenever your mouse is over an item.
The Name key then contains:
    "name": the translated item title for that language, 
    "description": the translated description to that item using local markdown format and
    "category": str in ["atribute", "resources", "works", "structures", "knowledge"] so that the code knows where to access the info the text refers to.

Name: {"name": str, 
       "description": str, 
       "category": str
       },
"""

languages = {
    "en": {Name.CHAOS: {"name": "Chaos", 
                        "description": str, 
                        "category": "atribute"
                        },
           Name.CREATIVITY: {"name": "Creativity", 
                             "description": str, 
                             "category": "atribute"
                             },
           Name.HEALTH: {"name": "Health", 
                         "description": str, 
                         "category": "atribute"
                         },
           Name.MAGIC: {"name": "Magic", 
                        "description": str, 
                        "category": "atribute"
                        },
           Name.COURAGE: {"name": "Courage", 
                          "description": str, 
                          "category": "atribute"
                          },
           },

    "pt": {Name.CHAOS: {"name": "Caos", 
                        "description": str, 
                        "category": "atribute"
                        },
           Name.CREATIVITY: {"name": "Criatividade", 
                             "description": str, 
                             "category": "atribute"
                             },
           Name.HEALTH: {"name": "Saúde", 
                         "description": str, 
                         "category": "atribute"
                         },
           Name.MAGIC: {"name": "Magia", 
                        "description": str, 
                        "category": "atribute"
                        },
           Name.COURAGE: {"name": "Coragem", 
                          "description": str, 
                          "category": "atribute"
                          },
           },
}
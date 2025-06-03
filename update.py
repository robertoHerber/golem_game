import random
from names import Name
from game import init_game

"""
Objective: to define every way in which the game is updated. 
Becuse of the idle nature of the game, most of the updating doesn't depend on user input.
"""

"""
Dicionários:
.items() torna o dicionário iterável
.values() torna os valores do dicionário iteráveis mas faz uma cópia. EVITE usar a menos que você realmente precise da lista de valores.
no caso, iterando um dict[dict], é possível usar hash em cada value (ex.: value["unlocked"])
se eu atribuir um dicionário incluso em outro e atualizar ele, ele modifica o original
    Ex.: dict2 = dict1[dict2]
         dict1["key"] = x
         # x será atualizado no dict1
reatribuição continua sendo nececssária se eu fizer um .copy() em um dicionário
eu posso usar esse sistema de atribuição dos dicionários pra fazer coisas interessantes
eu posso iterar as chaves de um dicionario só usando o dicionário no for
"""


############### ideia pra calcular coragem: armas * coragem_multiplier / população 
############### ideia pra saúde: médias exponenciailmente ponderadas da longevidade?
############### trocar todos os ratio por possible e refazer os cálculos todos (menos o learn knowledge pq tá funcionando)




# def update_chaos(game: dict) -> None:
#     pass




def update_creativity(game: dict) -> None:
    creativity = game["data"]["attributes"][Name.CREATIVITY]

    chance = 1 / (10 + (1 * creativity["all time points"]))
    point = 1 if random.random() < chance else 0
    creativity["points"] += point
    creativity["all time points"] += point




# INCLOMRPELEMTO
def update_health(game: dict) -> None:   # incompleto
    health = game["data"]["attributes"][Name.HEALTH]
    samples = health["samples"]
    resources = game["data"]["resources"]

    # Calcular sample de saúde
    protection = 10

    # Calcular EWMA
    alpha = 0.1

    if not samples:
        return []

    result = [ema]
    for x in samples[1:]:
        ema = (1 - alpha) * ema + alpha * x
        result.append(ema)

    return result[-1]

    pass




def flux_function(game: dict, x: int) -> int:  # melhorar isso daqui
    magic = game["data"]["attributes"][Name.MAGIC]
    flux = magic["flux"]
    cap  = magic["capacity"]

    if flux == 0:
        return 0
    
    # Função mesmo
    num = x
    den = 100 * flux / cap
    return num / den




# def update_courage(game: dict) -> None:
#     pass




def remove_worker(game: dict) -> None:  # nem sei se essa função funciona
    golems = game["data"]["golems"]
    works = game["data"]["works"]

    if golems["working idle"] == 0:
        golems_working = {}
        for key in works:
            golems_working[works[key]["golems working"]] = key

        work_to_remove = golems_working[max(list(golems_working.values()))]

        works[work_to_remove]["golems working"] -= 1
        golems["working busy"] -= 1

    elif golems["working idle"] > 1:
        golems["working idle"] -= 1




def update_unlocked_resources(game: dict) -> None:
    resources = game["data"]["resources"]

    for value in resources.values():
        if value["unlocked"] == False and value["quantity"] != 0:
            value["unlocked"] = True
    return




def simulate_random_choices(data: dict, multiplier: int) -> dict:
    iterations = data["iterations"] * multiplier
    items = {key: value for key, value in data.items() if key != "iterations"}
    
    # Criar uma lista de itens e suas probabilidades
    choices, probabilities = zip(*items.items())
    
    # Realizar as escolhas aleatórias
    results = {}
    for _ in range(iterations):
        chosen_item = random.choices(choices, probabilities)[0]
        results[chosen_item] = results.get(chosen_item, 0) + 1

    results = {key: value for key, value in results.items() if key != "nothing"}
    
    return results




def compute_golems(game: dict) -> None:
    health = game["data"]["attributes"][Name.HEALTH]
    magic = game["data"]["attributes"][Name.MAGIC]
    current_day = game["data"]["current day"]
    golems = game["data"]["golems"]


    # statues -> working
    statues_due = golems["statues due dates"].get(current_day, 0)
    if statues_due > 0:
        golems["statues"] -= statues_due
        golems["working idle"] += statues_due
        golems["birth dates"][current_day] = statues_due
        
        del golems["statues due dates"][current_day]


    # Dano
    broken = {}
    dead = {}

    for weakness, probability in golems["weakness"].items():
        broken[weakness] = 0
        dead[weakness] = 0

        chance = probability / health["level"] if health["level"] > 0 else probability

        # PENSAR POSSIBILIDADE DO BINOMIO DE NEWTON
        # Talvez o numpy tenha alguma função que cria um array de números aleatórios entre 0 e 1 e então avalie de maneira vetorizada quantos são menores que a probabilidade
        # working -> broken
        total_workers = int(golems["working idle"] + golems["working busy"])
        for _ in range(total_workers):
            broken[weakness] += 1 if random.random() < chance else 0
        # broken -> dead
        for _ in range(golems["broken"]):
            dead[weakness] += 1 if random.random() < chance else 0

    # working -> broken
    day_broken = sum(list(broken.values()))  # golems que quebraram nesse dia
    golems["broken"] += day_broken
    # remove_workers(game, day_broken)

    # broken -> dead
    day_dead = sum(list(dead.values()))
    golems["broken"] -= day_dead
    golems["death dates"][current_day] = day_dead

    cFpg = 10  # contained flux per golem
    magic["flux"] -= cFpg * day_dead
    magic["contained"] -= cFpg * day_dead




def compute_production(game: dict) -> None:
    magic = game["data"]["attributes"][Name.MAGIC]
    energy = game["data"]["energy"]
    resources = game["data"]["resources"]
    priorities = game["data"]["priorities"]
    works = game["data"]["works"]
    multiworks = game["data"]["multiworks"]


    # Zerar ferramentas um uso
    for name in resources:
        if resources[name]["is tool"]:
            resources[name]["in use"] = 0


    # Processar prioridades
    for name, category in priorities.items():
        if category == "works":
            unit = works[name]

            # Constantes
            resources_cost = unit["resources cost"].copy()
            resources_product = unit["resources product"].copy()
            in_multiworks = sum(list(unit["in multiworks"].values()))  # sum de uma lista vazia é zero
            active_units = unit["golems working"] - in_multiworks


            # Máximo possível usando a parte inteira da divisão (//)
            resources_possible =  [resources[key]["quantity"] // resources_cost[key] for key in resources_cost]        if resources_cost else [active_units]
            flux_possible =       (magic["flux"] - magic["contained"]) // unit["flux cost"]                            if unit["flux cost"] > 0 else active_units
            tools_possible =      [resources[tool]["quantity"] - resources[tool]["in use"] for tool in unit["tools"]]  if unit["tools"] else [active_units]

            total_energy =        sum([value for value in energy["production"].values()])
            other_energy_usage =  sum([energy["usage"][key] for key in energy["usage"]       if key != name])
            energy_possible =     total_energy - other_energy_usage // unit["energy cost"]  if unit["energy cost"] > 0 else active_units


            # Ajuste de unidades ativas
            active_units = min([active_units] + resources_possible + [flux_possible] + tools_possible + [energy_possible])
            active_units = max(0, active_units)  # Prevenção contra valores negativos
            if active_units == 0:
                continue


            # Calcular produção
            iterations = resources_product.get("iterations")
            if iterations == None:
                for key in resources_product:
                    resources_product[key] *= active_units
            elif type(iterations) == int:
                resources_product = simulate_random_choices(resources_product, active_units)
            flux_product = flux_function(game, unit["flux product"] * active_units)


            # Atribuição (atualizar valores no dicionário original)
            for tool in unit["tools"]:  # Faz as ferramentas quebrarem aleatoriamente
                resources[tool]["in use"] += active_units
                for _ in range(active_units):
                    chance = resources[tool]["breaking chance"]
                    resources[tool]["quantity"] -= 1 if random.random() < chance else 0

            for key in resources_cost:
                resources[key]["quantity"] -= resources_cost[key] * active_units
            for key in resources_product:
                resources[key]["quantity"] += resources_product[key]

            magic["flux"] -= unit["flux cost"] * active_units
            magic["flux"] += flux_product
            if magic["flux"] > magic["capacity"]:  # Evita produzir fluxo infinito
                magic["flux"] = magic["capacity"]

            energy["usage"][name] = unit["energy cost"] * active_units
            energy["production"][name] = unit["energy product"] * active_units



        elif category == "multiworks":
            unit = multiworks[name]

            # Constantes
            worker_type = works[unit["worker type"]]
            resources_cost = unit["resources cost"].copy()
            resources_product = unit["resources product"].copy()
            resources_quantity = {key: resources[key]["quantity"] for key in resources_cost}  # valores reais dos recursos que serão consumidos
            active_units = unit["quantity"]


            # Máximo possível usando a parte inteira da divisão (//)
            in_other_multiworks = sum([worker_type["in multiworks"][key] for key in worker_type["in multiworks"]   if key != name])    
            workers_possible =    (worker_type["golems working"] - in_other_multiworks) // unit["workers needed"]  
            resources_possible =  [resources_quantity[key] // resources_cost[key] for key in resources_cost]       if resources_cost else [active_units]
            flux_possible =       (magic["flux"] - magic["contained"]) // unit["flux cost"]                        if unit["flux cost"] > 0 else active_units

            tools_possible = [
                (resources[tool]["quantity"] - resources[tool]["in use"]) // unit["tools"][tool] 
                for tool in unit["tools"]
                ] if unit["tools"] else [active_units]
            
            total_energy =        sum([value for value in energy["production"].values()])
            other_energy_usage =  sum([energy["usage"][key] for key in energy["usage"]       if key != name])
            energy_possible =     total_energy - other_energy_usage // unit["energy cost"]  if unit["energy cost"] > 0 else active_units


            # Ajuste de unidades ativas
            active_units = min([active_units, workers_possible] + resources_possible + [flux_possible] + tools_possible + [energy_possible])
            active_units = max(0, active_units)  # Prevenção contra valores negativos
            if active_units == 0:
                continue


            # Calcular produção
            iterations = resources_product.get("iterations")
            if iterations == None:
                for key in resources_product:
                    resources_product[key] *= active_units
            elif type(iterations) == int:
                resources_product = simulate_random_choices(resources_product, active_units)

            flux_product = flux_function(game, unit["flux product"] * active_units)


            # Atribuição (atualizar valores no dicionário original)
            worker_type["in multiworks"][name] = unit["workers needed"] * active_units

            for tool in unit["tools"]:  # Faz as ferramentas quebrarem aleatoriamente
                resources[tool]["in use"] += active_units
                for _ in range(active_units):
                    chance = resources[tool]["breaking chance"]
                    for _ in range(unit["tools"][tool]):  # Tem mais de uma ferramenta por estrutura
                        resources[tool]["quantity"] -= 1 if random.random() < chance else 0

            for key in resources_cost:
                resources[key]["quantity"] -= resources_cost[key] * active_units
            for key in resources_product:
                resources[key]["quantity"] += resources_product[key]

            magic["flux"] -= unit["flux cost"] * active_units
            magic["flux"] += flux_product
            if magic["flux"] > magic["capacity"]:  # Evita produzir fluxo infinito
                magic["flux"] = magic["capacity"]

            energy["usage"][name] = unit["energy cost"] * active_units
            energy["production"][name] = unit["energy product"] * active_units




# PLAYER INPUT


# desbloquear conhecimento
def unlock_knowledge(game: dict) -> None:
    creativity = game["data"]["attributes"][Name.CREATIVITY]
    knowledge = game["data"]["knowledge"]

    knowledge_learned = []
    for key in knowledge:
        if knowledge[key]["learned"]:
            knowledge_learned.append(key)

    knowledge_possible = []
    for key in knowledge:
        trues = []
        for dependence in knowledge[key]["dependencies"]:
            trues.append(dependence in knowledge_learned)
        if False not in trues and not knowledge[key]["unlocked"]:
            knowledge_possible.append(key)

    unlocking_cost = 1  # Balancear
    if (creativity["points"] >= unlocking_cost) and knowledge_possible:
        unlocked = random.choice(knowledge_possible)
        knowledge[unlocked]["unlocked"] = True
    
        creativity["points"] -= unlocking_cost




# aprender conhecimento
def learn_knowledge(game: dict, name: Name) -> None:
    knowledge = game["data"]["knowledge"][name]
    resources = game["data"]["resources"]
    creativity = game["data"]["attributes"][Name.CREATIVITY]
    magic = game["data"]["attributes"][Name.MAGIC]
    works = game["data"]["works"]
    multiworks = game["data"]["multiworks"]

    # cost / real > 1
    if not knowledge["learned"]:
        creativity_ratio =  creativity["points"] - knowledge["creativity cost"]
        flux_ratio       =  magic["flux"] - magic["contained"] - knowledge["flux cost"]
        resources_ratio  =  [resources[key]["quantity"] - value for key, value in knowledge["resources cost"].items()]

        min_ratio = min([creativity_ratio, flux_ratio] + resources_ratio)
        if min_ratio >= 0:
            creativity["points"] -= knowledge["creativity cost"]
            magic["flux"] -= knowledge["flux cost"]

            for key, value in knowledge["resources cost"].items():
                resources[key]["quantity"] -= value
                    
            knowledge["learned"] = True

            for name in knowledge["work unlocked"]:
                works[name]["unlocked"] = True
                game["data"]["priorities"][name] = "works"

            for name in knowledge["multiwork unlocked"]:
                multiworks[name]["unlocked"] = True
                game["data"]["priorities"][name] = "multiworks"




# fazer estatua
def make_statue(game: dict, quantity: int=1) -> None:
    magic = game["data"]["attributes"][Name.MAGIC]
    golems = game["data"]["golems"]
    current_day = game["data"]["current day"]
    material = game["data"]["resources"][golems["material"]]

    # Constantes
    Fpg  = 10       # Flux per golem
    cFpg = 5      # Contained Flux per golem
    mpg  = 50      # Materials per golem
    time = 365     # Days until full development
    pct  = 10/100  # Percentage of noise on time
    noise = int(time * pct)

    # Máximo possível usando a parte inteira da divisão (//)
    flux_possible =      (magic["flux"] - magic["contained"]) // (Fpg + cFpg)
    material_possible =  (material["quantity"] // mpg)

    # Ajuste da quantidade
    quantity = min(quantity, flux_possible, material_possible)
    quantity = max(0, quantity)  # Prevenção contra valores negativos
    if quantity == 0:
        return
    
    # Atribuição no game["data"]
    golems["statues"] +=     quantity
    magic["flux"] -=         quantity * Fpg
    magic["contained"] +=    quantity * cFpg
    material["quantity"] -=  quantity * mpg

    due_date = current_day + time + random.randint(0, noise)
    golems["statues due dates"][due_date] = golems["statues due dates"].get(due_date, 0) + quantity




# empregar golem
def employ_golem(game: dict, name: Name, quantity: int=1) -> None:
    work = game["data"]["works"][name]
    golems = game["data"]["golems"]

    if golems["working idle"] >= quantity:
        work["golems working"] += quantity
        golems["working idle"] -= quantity
        golems["working busy"] += quantity




# desempregar golem
def unemploy_golem(game: dict, name: Name, quantity: int=1) -> None:
    work = game["data"]["works"][name]
    golems = game["data"]["golems"]

    if work["golems working"] >= quantity:
        work["golems working"] -= quantity
        golems["working idle"] += quantity
        golems["working busy"] -= quantity




# construir estrutura
def build_multiwork(game: dict, name: Name, quantity: int=1) -> None:
    multiwork = game["data"]["multiworks"][name]
    resources = game["data"]["resources"]
    land = game["data"]["land"]

    # Máximo possível usando a parte inteira da divisão (//)
    land_possible =       land["idle"] // multiwork["land needed"]
    resources_possible =  [resources[key]["quantity"] // multiwork["building cost"][key] for key in multiwork["building cost"]]

    # Ajuste da quantidade
    quantity = min([quantity, land_possible], resources_possible)
    quantity = max(0, quantity)  # Prevenção contra valores negativos
    if quantity == 0:
        return

    # Atribuição
    for key, value in multiwork["building cost"].items():
        resources[key]["quantity"] -= value * quantity
    
    land["idle"] -= multiwork["land needed"] * quantity
    land["busy"] += multiwork["land needed"] * quantity
    multiwork["quantity"] += quantity




# quebrar estrutura
def break_multiwork(game: dict, name: Name, quantity: int=1) -> None:
    multiwork = game["data"]["multiworks"][name]
    resources = game["data"]["resources"]
    land = game["data"]["land"]

    quantity = min(quantity, multiwork["quantity"])
    quantity = max(0, quantity)
    if quantity == 0:
        return
    
    total_land = multiwork["land needed"] * quantity
    land["idle"] += total_land
    land["busy"] -= total_land

    multiwork["quantity"] += quantity
    for key, value in multiwork["building cost"].items():
        leftove_percent = 1/3
        resource_leftover = int(value * quantity * leftove_percent)
        resources[key]["quantity"] += resource_leftover








def update_game(game: dict) -> None:
    game["data"]["current day"] += 1

    # compute_energy(game)

    # update_chaos(game)
    update_creativity(game)
    update_health(game)
    # update_courage(game)

    update_unlocked_resources(game)
    compute_golems(game)
    compute_production(game)
    return

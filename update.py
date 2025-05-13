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
.values() torna os valores do dicionário iteráveis mas faz uma cópia
no caso, iterando um dict[dict], é possível usar hash em cada value (ex.: value["unlocked"])
se eu atribuir um dicionário incluso em outro e atualizar ele, ele modifica o original
    Ex.: dict2 = dict1[dict2]
         dict1["key"] = x
         # x será atualizado no dict1
reatribuição continua sendo nececssária se eu fizer um .copy() em um dicionário
eu posso usar esse sistema de atribuição dos dicionários pra fazer coisas interessantes
eu posso iterar as chaves de um dicionario só usando o dicionário no for
"""


def update_creativity(game: dict) -> None:
    creativity = game["data"]["attributes"][Name.CREATIVITY]

    chance = 1 / (10 + (1 * creativity["all time points"]))
    point = 1 if random.random() < chance else 0
    creativity["points"] += point
    creativity["all time points"] += point




def update_unlocked_resources(game: dict) -> None:
    resources = game["data"]["resources"]

    for value in resources.values():
        if value["unlocked"] == False and value["quantity"] != 0:
            value["unlocked"] = True
    return




def flux_function(game: dict, x: int) -> int:
    magic = game["data"]["attributes"][Name.MAGIC]
    # y = 10 * x / (100 * magic["flux"] / magic["capacity"])
    # return y
    flux = magic["flux"]
    cap  = magic["capacity"]
    if flux == 0 or cap == 0:
        return 0
    den = 100 * flux / cap
    return 10 * x / den




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
    
    return results




def remove_workers(game: dict, golems_to_remove: int) -> None:
    golems = game["data"]["golems"]
    priorities = game["data"]["priorities"]
    works = game["data"]["works"]

    if golems["working idle"] < golems_to_remove:
        busy_golems_to_remove = golems_to_remove - golems["working idle"]
        golems["working idle"] = 0
        golems["working busy"] -= busy_golems_to_remove
        
        for category, name in reversed(list(priorities.items())):
            if busy_golems_to_remove == 0:
                break
            if category == "work":
                if works[name]["golems working"] < busy_golems_to_remove:
                    works[name]["golems working"] = 0
                    busy_golems_to_remove -= works[name]["golems working"]
                else:
                    works[name]["golems working"] -= busy_golems_to_remove
                    busy_golems_to_remove = 0
    else: 
        golems["working idle"] -= golems_to_remove




# def função pra remover recursos do expiration dates (game, Name, quantity)




def compute_golems(game: dict) -> None:
    magic = game["data"]["attributes"][Name.MAGIC]
    current_day = game["data"]["current day"]
    golems = game["data"]["golems"]
    resources = game["data"]["resources"]
    works = game["data"]["works"]


    # Estatuas
    statues_flux_consumption = 10
    statues_materials_consumption = 10

    statues_flux = golems["statues"] * statues_flux_consumption
    statues_materials = golems["statues"] * statues_materials_consumption

    flux_ratio = magic["flux"] / statues_flux if statues_flux > 0 else 1
    # material_ratio = resources.get(golems["material"], 0) / statues_materials if statues_materials > 0 else 1
    material_ratio = resources[golems["material"]]["quantity"] / statues_materials if statues_materials > 0 else 1

    if min([flux_ratio, material_ratio]) < 1:
        statues_flux = int(magic["flux"] / statues_flux_consumption) if statues_flux_consumption > 0 else 0
        statues_materials = int(resources[golems["material"]]["quantity"] / statues_materials_consumption) if statues_materials_consumption > 0 else 0

        true_statues = min([statues_flux, statues_materials])

        statues_flux = true_statues * statues_flux_consumption
        statues_materials = true_statues * statues_materials_consumption

    magic["flux"] -= statues_flux
    resources[golems["material"]]["quantity"] -= statues_materials


    # Consumo comum de fluxo
    common_flux_consumption = 5
    golems_flux = (golems["working idle"] + golems["working busy"] + golems["broken"]) * common_flux_consumption
    flux_ratio = magic["flux"] / golems_flux if golems_flux > 0 else 1

    if (flux_ratio) < 1:
        true_golems = int(magic["flux"] / common_flux_consumption)
        golems_flux = true_golems * common_flux_consumption

    magic["flux"] -= golems_flux


    # Desenvolver (statues -> working)
    statues_due = golems["statues due dates"].get(current_day, 0)
    if statues_due:
        golems["statues"] -= statues_due
        golems["working idle"] += statues_due
        golems["birth dates"][current_day] = statues_due
        if statues_due != 0:
            del golems["statues due dates"][current_day]


    # Dano físico
    broken = {}
    broken_to_death = {}

    for weakness, chance in golems["weakness"].items():
        broken[weakness] = 0
        broken_to_death[weakness] = 0
        # PENSAR POSSIBILIDADE DO BINOMIO DE NEWTON
        # working -> broken
        total_workers = int(golems["working idle"] + golems["working busy"])
        for i in range(total_workers):
            broken[weakness] += 1 if random.random() < chance else 0
        # broken -> dead
        for i in range(golems["broken"]):
            broken_to_death[weakness] += 1 if random.random() < chance else 0

    # working -> broken
    day_broken = sum(list(broken.values()))  # golems que quebraram nesse dia
    golems["broken"] += day_broken
    remove_workers(game, day_broken)

    # broken -> dead
    day_broken_to_death = sum(list(broken_to_death.values()))
    golems["death dates"][current_day] = day_broken_to_death
    golems["broken"] -= day_broken_to_death


    # Sem fluxo (flux < contained)
    contained_flux_per_golem = 10
    magic["contained"] = (golems["working idle"] + golems["working busy"] + golems["broken"] + golems["statues"]) * contained_flux_per_golem
    
    falta = magic["contained"] - magic["flux"]
    defluxed = (falta // contained_flux_per_golem) if falta > 0 else 0
    golem_stages = [golems["statues"], golems["broken"]]
    
    if defluxed > -float("inf"):
        for i in golem_stages:
            if defluxed == 0 or golem_stages[-1] == 0:
                break

            deduct = min(i, defluxed)


            if i == golems["statues"]:  # Remover "statues due dates"
                defluxed_statues = deduct

                keys_to_delete = []  # Lista para armazenar as chaves a serem removidas

                for date, n_statues in golems["statues due dates"].items():
                    deduct_statues = min(n_statues, defluxed_statues)
                    defluxed_statues -= deduct_statues
                    golems["statues due dates"][date] -= deduct_statues  # Atualiza o valor no dicionário

                    if golems["statues due dates"][date] == 0:
                        keys_to_delete.append(date)  # Marca a chave para remoção

                    if defluxed_statues == 0:
                        break
                    
                # Remove as chaves marcadas
                for date in keys_to_delete:
                    del golems["statues due dates"][date]


            i -= deduct
            golems["death dates"][current_day] = golems["death dates"].get(current_day, 0) + deduct
            defluxed -= deduct

        statues_dev_time = 365
        due_date = current_day + statues_dev_time
        golems["statues"] += defluxed
        golems["statues due dates"][due_date] = golems["statues due dates"].get(due_date, 0) + defluxed
        remove_workers(game, defluxed)




def compute_expiration(game: dict) -> None:
    resources = game["data"]["resources"]
    current_day = game["data"]["current day"]

    for key in resources:
        resources[key]
        resources[key]["quantity"] -= resources[key]["expiration dates"].get(current_day, 0)
        if resources[key]["expiration dates"].get(current_day, 0) != 0:
            del resources[key]["expiration dates"][current_day]




def compute_production(game: dict) -> None:
    current_day = game["data"]["current day"]
    magic = game["data"]["attributes"][Name.MAGIC]
    resources = game["data"]["resources"]
    priorities = game["data"]["priorities"]
    works = game["data"]["works"]
    structures = game["data"]["structures"]

    # Atualizar resetar ferramentas
    for key in resources:
        if resources[key]["in use"] > 0:
            resources[key]["unlocked"] = 0

    # Processar prioridades
    for name, category in priorities.items():
        if category == "works":
            unit = works[name]
            resources_cost = unit["resources cost"].copy()
            resources_quantity = {key: resources[key]["quantity"] for key in resources_cost}
            # golems_in_structures = sum([value for value in unit["in structures"].values()])
            # golems_in_structures = golems_in_structures if type(golems_in_structures) == int else 0 
            active_units = unit["golems working"] # - golems_in_structures

            # Calcular custo total para a quantidade de trabalhadores atual
            for key in resources_cost:
                resources_cost[key] *= active_units
            
            # Verificar se a produção é possível
            resources_ratios =  [resources_quantity[key] - resources_cost[key] for key in resources_cost] if resources_cost else [1]

            flux_cost =   unit["flux cost"] * active_units
            flux_ratio =  magic["flux"] - flux_cost

            tools_available =   tools_available = [resources[tool]["quantity"] - resources[tool]["in use"] for tool in unit["tools"]]
            tools_available =   min(tools_available) if tools_available else active_units
            tools_per_worker =  tools_available - active_units
            
            min_ratio = min(resources_ratios + [flux_ratio, tools_per_worker])

            
            if min_ratio > 0:
                # Ajustar unidades ativas com base nos recursos disponíveis
                resources_cost = unit["resources cost"].copy()
                resources_cost_possible = [int(quantity / cost) for quantity, cost in zip(resources_quantity.values(), resources_cost.values())]
                flux_possible = int(magic["flux"] / unit["flux cost"]) if unit["flux cost"] > 0 else float("inf")

                active_units = min(resources_cost_possible + [flux_possible, tools_available])

                # Recalcular custos com base nas unidades ajustadas
                for key in resources_cost:
                    resources_cost[key] *= active_units
                flux_cost = unit["flux cost"] * active_units
            elif min_ratio < 0:
                continue
            

            # Calcular produção
            resources_product = unit["resources product"].copy()
            iterations = resources_product.get("iterations")
            if iterations == None:
                for key in resources_product:
                    resources_product[key] *= active_units
            elif type(iterations) == int:
                resources_product = simulate_random_choices(resources_product, active_units)

            flux_product = flux_function(game, unit["flux product"] * active_units)

            # Atribuir valores no dicionário original
            for tool in unit["tools"]:
                resources[tool]["in use"] += active_units

            for key in resources_cost: # consumir os recursos com a data de expiração mais próxima
                resources[key]["quantity"] -= resources_cost[key]
                for expiration in resources[key]["expiration dates"]:
                    expiring = resources[key]["expiration dates"][expiration]
                    deduct = min(expiring, resources_cost[key])
                    resources_cost[key] -= deduct
                    expiring -= deduct
                    if resources_cost[key] == 0:
                        break

            for key in resources_product: # nessa parte precisa acrescentar items no ["resources"][Name]["expiration dates"]
                expiration_time = resources[key]["expiration time"]
                pcent = 10/100
                expiration = current_day + expiration_time + random.randint(int(-expiration_time*pcent), int(expiration_time*pcent))
                resources[key]["quantity"] += resources_product[key]
                resources[key]["expiration dates"][expiration] = resources[key]["expiration dates"].get(expiration, 0) + resources_product[key]

            magic["flux"] -= flux_cost
            magic["flux"] += flux_product



        elif category == "structures":
            unit = structures[name]
            # atualizar / corrigir os valores em ["works"][Name]["in structures"] (capar em "golems working" e -= x % "workers needed")
            # deixa pra fazer depois da pré-produção
            resources_cost = 0




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
    structures = game["data"]["structures"]

    # cost / real > 1
    if not knowledge["learned"]:
        creativity_ratio =  creativity["points"] - knowledge["creativity cost"]
        flux_ratio = magic["flux"] - knowledge["flux cost"]
        resources_ratio = [resources[key]["quantity"] - value for key, value in knowledge["resources cost"].items()]

        min_ratio = min([creativity_ratio, flux_ratio] + resources_ratio)
        if min_ratio > 0:
            creativity["points"] -= knowledge["creativity cost"]
            magic["flux"] -= knowledge["flux cost"]

            for key, value in knowledge["resources cost"].items():
                resources[key]["quantity"] -= value
                debit = value
                for i in resources[key]["expiration dates"].values():
                    deduct = min(i, debit)
                    debit -= deduct
                    i -= deduct
                    if debit == 0:
                        break 
                    
            knowledge["learned"] = True
            for name in knowledge["work unlocked"]:
                works[name]["unlocked"] = True
                game["data"]["priorities"][name] = "works"
            for name in knowledge["structure unlocked"]:
                structures[name]["unlocked"] = True
                game["data"]["priorities"][name] = "structures"




# fazer estatua
def make_statue(game: dict, quantity: int=1) -> None:
    golems = game["data"]["golems"]
    current_day = game["data"]["current day"]

    statues_dev_time = 365
    due_date = current_day + statues_dev_time
    golems["statues"] += quantity
    golems["statues due dates"][due_date] = golems["statues due dates"].get(due_date, 0) + quantity




# empregar golem
def employ_golem(game: dict, name: Name, quantity: int=1) -> None:
    work = game["data"]["works"][name]
    golems = game["data"]["golems"]

    if golems["working idle"] >= quantity:
        work["golems working"] += quantity
        golems["working idle"]   -= quantity
        golems["working busy"]   += quantity




# desempregar golem
def unemploy_golem(game: dict, name: Name, quantity: int=1) -> None:
    work = game["data"]["works"][name]
    golems = game["data"]["golems"]

    if work["golems working"] >= quantity:
        work["golems working"]   -= quantity
        golems["working idle"]   += quantity
        golems["working busy"]   -= quantity




# construir estrutura
def build_structure(game: dict, name: Name, quantity: int=1) -> None:
    structure = game["data"]["structures"][name]
    resources = game["data"]["resources"]
    land = game["data"]["land"]

    total_land = structure["land needed"] * quantity
    resources_ratio = [value * quantity / resources[key]["quantity"] for key, value in structure["building cost"].items()]
    land_ratio = total_land / land["idle"]

    if min(resources_ratio + [land_ratio]) <= 1:
        for key, value in structure["building cost"].items():
            resources[key]["quantity"] -= value * quantity
            debit = value * quantity
            for i in resources[key]["expiration dates"].values():
                deduct = min(i, debit)
                debit -= deduct
                i -= deduct
                if debit == 0:
                    break 
        
        land["idle"] -= total_land
        land["busy"] += total_land
        structure["quantity"] += quantity




# quebrar estrutura
def break_structure(game: dict, name: Name, quantity: int=1) -> None:
    structure = game["data"]["structures"][name]
    resources = game["data"]["resources"]
    land = game["data"]["land"]
    current_day = game["data"]["current day"]

    if structure["quantity"] >= quantity:
        total_land = structure["land needed"] * quantity
        land["idle"] += total_land
        land["busy"] -= total_land

        structure["quantity"] += quantity
        for key, value in structure["building cost"].items():
            leftove_percent = 1/3
            resource_leftover = int(value * quantity * leftove_percent)
            expiration_time = resources[key]["expiration time"]
            percent = 10/100
            expiration = current_day + expiration_time + random.randint(-expiration_time*percent, expiration_time*percent)
            resources[key]["quantity"] += resource_leftover
            resources[key]["expiration dates"][expiration] = resources[key]["expiration dates"].get(expiration, 0) + resource_leftover








def update_game(game: dict) -> None:
    game["data"]["current day"] += 1
    update_creativity(game)
    update_unlocked_resources(game)
    # compute_golems(game)
    # compute_expiration(game)
    compute_production(game)
    return

# FLux tá muito bugado
# "Sem fluxo" tá zoando tudo
# compute golems ta zoando tudo

# game = init_game()
# for _ in range(10*365):
#     compute_production(game)
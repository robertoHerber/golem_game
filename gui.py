import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
# import pickle
# import sys
from names import Name
# from languages import languages
from game import init_game
from update import update_game, unlock_knowledge, learn_knowledge, make_statue, employ_golem, unemploy_golem, build_structure, break_structure


def show(dim, screen, game: dict, mpos, scroll_i=0, scroll_r=0, scroll_w=0, scroll_k=0):
    # Colunas
    column_width = dim[0] / 4

    info_column = pygame.Rect((column_width * 0), 0, column_width, dim[1])
    info_collision = info_column.collidepoint(mpos)
    pygame.draw.rect(screen, (63, 63, 63), info_column)

    resource_column = pygame.Rect((column_width * 1), 0, column_width, dim[1])
    resource_collision = resource_column.collidepoint(mpos)
    pygame.draw.rect(screen, (31, 31, 31), resource_column)

    work_column = pygame.Rect((column_width * 2), 0, column_width, dim[1])
    work_collision = work_column.collidepoint(mpos)
    pygame.draw.rect(screen, (63, 63, 63), work_column)

    knowledge_column = pygame.Rect((column_width * 3), 0, column_width, dim[1])
    knowledge_collision = knowledge_column.collidepoint(mpos)
    pygame.draw.rect(screen, (31, 31, 31), knowledge_column)

    if info_collision:
        column = "info"
    elif resource_collision:
        column = "resource"
    elif work_collision:
        column = "work"
    elif knowledge_collision:
        column = "knowledge"

    # Dados do jogo
    resources = game["data"]["resources"]
    works = game["data"]["works"]
    knowledge = game["data"]["knowledge"]
    current_day = game["data"]["current day"]
    golems = game["data"]["golems"]
    land = game["data"]["land"]
    attributes = game["data"]["attributes"]

    first_column_titles = ["Day", 
                           "Golems",
                           "Working Golems",
                           "Broken Golems",
                        #    "Statues",
                           "Land",
                        #    "Chaos",
                           "Creativity",
                        #    "Health",
                           "Magic",
                        #    "Courage",
                           Name.MAKE_STATUE,
                           Name.DISCOVER_KNOWLEDGE
                           ]
    first_column_infos = [f"{current_day % 365} (Year {current_day // 365})", 
                          str(golems["working busy"] + golems["working idle"] + golems["broken"]),
                          f"{golems["working busy"]}/{golems["working busy"] + golems["working idle"]}",
                          str(golems["broken"]),
                        #   str(golems["statues"]),
                          f"{land["busy"]}/{land["busy"] + land["idle"]}",
                        #   " ",
                          str(attributes[Name.CREATIVITY]["points"]),
                        #   " ",
                          f"{attributes[Name.MAGIC]["contained"]}/{attributes[Name.MAGIC]["flux"]}/{attributes[Name.MAGIC]["capacity"]}",
                        #   " ",
                          " ",
                          " "
                          ]

    unlocked_resources = [key for key in resources if resources[key]["unlocked"]]
    unlocked_works = game["data"]["priorities"]
    unlocked_knowledge = [key for key in knowledge if knowledge[key]["unlocked"]]

    # Formatação
    padding = 9
    row_width = column_width - 2*padding
    row_height = dim[1] / 20

    font_size = int(dim[1]/36)
    font = pygame.font.Font(None, size=font_size)

    # Dados nas colunas
    rect_collisions = []

    # Primeira coluna
    for n in range(len(first_column_titles)):
        title = first_column_titles[n] if type(first_column_titles[n]) == str else first_column_titles[n].value
        info = first_column_infos[n]

        # Retângulo
        left = 0*column_width + padding
        top = padding + n*(row_height + padding) + scroll_i

        row = pygame.Rect(left, top, row_width, row_height)
        row_collision = row.collidepoint(mpos)
        rect_collisions.append(row_collision)
        pygame.draw.rect(screen, (127*(1+row_collision), 127*(1+row_collision), 127*(1+row_collision)), row)

        # Texto
        # Nome do recurso
        text = font.render(title, True, (255, 255, 255))

        text_left = left + padding
        text_top = top + (row_height - font_size)/2  # Isso aqui centraliza o texto no retângulo 
        screen.blit(text, (text_left, text_top))

        # Quantidade
        text = font.render(info, True, (255, 255, 255))

        text_left += (row_width/2)
        screen.blit(text, (text_left, text_top))


    # Recursos
    for n, name in enumerate(unlocked_resources):
        # Retângulo
        left = 1*column_width + padding
        top = padding + n*(row_height + padding) + scroll_r

        resource_row = pygame.Rect(left, top, row_width, row_height)
        row_collision = resource_row.collidepoint(mpos)
        rect_collisions.append(row_collision)
        pygame.draw.rect(screen, (127*(1+row_collision), 127, 127), resource_row)

        # Texto
        # Nome do recurso
        text = font.render(name.value, True, (255, 255, 255))

        text_left = left + padding
        text_top = top + (row_height - font_size)/2  # Isso aqui centraliza o texto no retângulo 
        screen.blit(text, (text_left, text_top))

        # Quantidade
        text = font.render(str(resources[name]["quantity"]), True, (255, 255, 255))

        text_left += (row_width/2)
        screen.blit(text, (text_left, text_top))


    # Trabalho
    for n, name in enumerate(unlocked_works):
        # Retângulo
        left = 2*column_width + padding
        top = padding + n*(row_height + padding) + scroll_w

        work_row = pygame.Rect(left, top, row_width, row_height)
        row_collision = work_row.collidepoint(mpos)
        rect_collisions.append(row_collision)
        pygame.draw.rect(screen, (127, 127*(1+row_collision), 127), work_row)

        # Texto
        # Nome do recurso
        text = font.render(name.value, True, (255, 255, 255))

        text_left = left + padding
        text_top = top + (row_height - font_size)/2  # Isso aqui centraliza o texto no retângulo 
        screen.blit(text, (text_left, text_top))

        # Quantidade
        text = font.render(str(works[name]["golems working"]), True, (255, 255, 255))

        text_left += (row_width/2)
        screen.blit(text, (text_left, text_top))


    # Conhecimento
    for n, name in enumerate(unlocked_knowledge):
        # Retângulo
        left = 3*column_width + padding
        top = padding + n*(row_height + padding) + scroll_k

        knowledge_row = pygame.Rect(left, top, row_width, row_height)
        row_collision = knowledge_row.collidepoint(mpos)
        rect_collisions.append(row_collision)
        pygame.draw.rect(screen, (127, 127, 127*(1+row_collision)), knowledge_row)

        # Texto
        # Nome do recurso
        text = font.render(name.value, True, (255, 255, 255))

        text_left = left + padding
        text_top = top + (row_height - font_size)/2  # Isso aqui centraliza o texto no retângulo 
        screen.blit(text, (text_left, text_top))

        # Quantidade
        text = font.render("learned: " + str(knowledge[name]["learned"]), True, (255, 255, 255))

        text_left += (row_width/2)
        screen.blit(text, (text_left, text_top))

    
    all_rect = first_column_titles + unlocked_resources + list(unlocked_works.keys()) + unlocked_knowledge
    if True in rect_collisions:
        mouse_over = all_rect[rect_collisions.index(True)]
    else:
        mouse_over = None
        
    return mouse_over, column




def find_category(game: dict, name: Name) -> str:
    possibilities = ["resources", "works", "structures", "knowledge"]

    for i in possibilities:
        if name in list(game["data"][i].keys()):
            return i

    return None




pygame.init()

dim = (1280, 720)
dim = (1280, 720)
dim = (1920, 1080)
screen = pygame.display.set_mode(dim)
pygame.display.set_caption("Golems Ascendancy")

running = True
clock = pygame.time.Clock()
delta_time = 0.1
time_accumulator = 0

font = pygame.font.Font(None, size=30)

game = init_game()

scroll_i = 0
scroll_r = 0
scroll_w = 0
scroll_k = 0
scroll_lenght = 50



# Loop
while running:
    # Clean everything from last frame
    screen.fill((63, 63, 63))
    # Mouse position
    mpos = pygame.mouse.get_pos()
    
    mouse_over, column = show(dim, screen, game, mpos, scroll_i, scroll_r, scroll_w, scroll_k)

    # text = font.render(column, True, (255, 255, 255))
    # screen.blit(text, (0, 40))

    # if mouse_over != None:
    #     text_to_blit = mouse_over.value if type(mouse_over) != str else mouse_over
    #     text = font.render(text_to_blit, True, (255, 255, 255))
    #     screen.blit(text, (0, 0))

    # isso aqui é pra não deixar você scrollar pra cima
    # scroll_i = 0 if scroll_i > 0 else scroll_i
    # scroll_r = 0 if scroll_r > 0 else scroll_r
    # scroll_w = 0 if scroll_w > 0 else scroll_w
    # scroll_k = 0 if scroll_k > 0 else scroll_k

    # Event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event.button)

            if event.button == 1:
                category = find_category(game, mouse_over)
                if category == "works":
                    employ_golem(game, mouse_over)
                elif category == "structure":
                    build_structure(game, mouse_over)
                elif category == "knowledge":
                    learn_knowledge(game, mouse_over)
                elif mouse_over == Name.MAKE_STATUE:
                    make_statue(game)
                elif mouse_over == Name.DISCOVER_KNOWLEDGE:
                    unlock_knowledge(game)

            elif event.button == 3:
                category = find_category(game, mouse_over)
                if category == "works":
                    unemploy_golem(game, mouse_over)
                elif category == "structure":
                    break_structure(game, mouse_over)

            elif event.button == 4:
                if column == "info":
                    scroll_i += scroll_lenght
                if column == "resource":
                    scroll_r += scroll_lenght
                if column == "work":
                    scroll_w += scroll_lenght
                if column == "knowledge":
                    scroll_k += scroll_lenght

            elif event.button == 5:
                if column == "info":
                    scroll_i -= scroll_lenght
                if column == "resource":
                    scroll_r -= scroll_lenght
                if column == "work":
                    scroll_w -= scroll_lenght
                if column == "knowledge":
                    scroll_k -= scroll_lenght


    # 1 - left click
    # 2 - middle click
    # 3 - right click
    # 4 - scroll up
    # 5 - scroll down

    day_duration = 1.0/1
    if time_accumulator >= day_duration:
        time_accumulator -= day_duration
        update_game(game)

    # Framerate
    pygame.display.flip()
    delta_time = clock.tick(60) / 1000
    time_accumulator += delta_time
    delta_time = max(0.001, min(0.1, delta_time))
pygame.quit()




# 4 colunas
#   current day & golems & land & attibutes
#   resources
#   works
#   knowledge

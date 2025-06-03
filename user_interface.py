import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
import random
import pickle
import sys
from names import Name
from languages import languages
from game import init_game
from update import update_game, unlock_knowledge, learn_knowledge, make_statue, employ_golem, unemploy_golem, build_multiwork, break_multiwork




def show(dim, screen, game: dict, mpos, scroll_i=0, scroll_r=0, scroll_w=0, scroll_k=0):
    background = pygame.image.load("assets/stone screen.png").convert_alpha()
    pygame.transform.scale(background, dim)
    screen.blit(background, (0, 0))

    frame(dim, screen, 0, 0, dim[0], dim[1], border="card")


    # Colunas
    column_width = dim[0] / 4

    info_column = pygame.Rect((column_width * 0), 0, column_width, dim[1])
    info_collision = info_column.collidepoint(mpos)
    # pygame.draw.rect(screen, (63, 63, 63), info_column)

    resource_column = pygame.Rect((column_width * 1), 0, column_width, dim[1])
    resource_collision = resource_column.collidepoint(mpos)
    # pygame.draw.rect(screen, (31, 31, 31), resource_column)

    work_column = pygame.Rect((column_width * 2), 0, column_width, dim[1])
    work_collision = work_column.collidepoint(mpos)
    # pygame.draw.rect(screen, (63, 63, 63), work_column)

    knowledge_column = pygame.Rect((column_width * 3), 0, column_width, dim[1])
    knowledge_collision = knowledge_column.collidepoint(mpos)
    # pygame.draw.rect(screen, (31, 31, 31), knowledge_column)

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
                           "Statues",
                           "",
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
                          f"{golems['working busy']}/{golems['working busy'] + golems['working idle']}",
                          str(golems["broken"]),
                          str(golems["statues"]),
                          str(golems["statues due dates"]),
                          f"{land['busy']}/{land['busy'] + land['idle']}",
                        #   " ",
                          str(attributes[Name.CREATIVITY]["points"]),
                        #   " ",
                          f"{attributes[Name.MAGIC]['contained']}/{attributes[Name.MAGIC]['flux']}/{attributes[Name.MAGIC]['capacity']}",
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
    font = pygame.font.Font("assets/computer modern.ttf", size=font_size)

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

        row = pygame.Surface((row_width, row_height), pygame.SRCALPHA)
        row.fill((64*row_collision, 64*row_collision, 64*row_collision, 128))
        screen.blit(row, (left, top))
        frame(dim, screen, left, top, row_width, row_height, border="card")


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

        row = pygame.Rect(left, top, row_width, row_height)
        row_collision = row.collidepoint(mpos)
        rect_collisions.append(row_collision)

        row = pygame.Surface((row_width, row_height), pygame.SRCALPHA)
        row.fill((64*row_collision, 64*row_collision, 64*row_collision, 128))
        screen.blit(row, (left, top))
        frame(dim, screen, left, top, row_width, row_height, border="card")

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

        row = pygame.Rect(left, top, row_width, row_height)
        row_collision = row.collidepoint(mpos)
        rect_collisions.append(row_collision)

        row = pygame.Surface((row_width, row_height), pygame.SRCALPHA)
        row.fill((64*row_collision, 64*row_collision, 64*row_collision, 128))
        screen.blit(row, (left, top))
        frame(dim, screen, left, top, row_width, row_height, border="card")

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

        row = pygame.Rect(left, top, row_width, row_height)
        row_collision = row.collidepoint(mpos)
        rect_collisions.append(row_collision)

        row = pygame.Surface((row_width, row_height), pygame.SRCALPHA)
        row.fill((64*row_collision, 64*row_collision, 64*row_collision, 128))
        screen.blit(row, (left, top))
        frame(dim, screen, left, top, row_width, row_height, border="card")

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




def frame(dim, width:int, height:int, border: str="card"):
    # Surface image
    border = "assets/" + border

    top_border =    pygame.image.load(border + " top.png").convert_alpha()
    right_border =  pygame.image.load(border + " right.png").convert_alpha()
    bottom_border = pygame.image.load(border + " bottom.png").convert_alpha()
    left_border =   pygame.image.load(border + " left.png").convert_alpha()

    # Scale
    factor = dim[0] / 1920
    top_border =    pygame.transform.scale_by(top_border, factor)
    right_border =  pygame.transform.scale_by(right_border, factor)
    bottom_border = pygame.transform.scale_by(bottom_border, factor)
    left_border =   pygame.transform.scale_by(left_border, factor)

    # Lenght
    border_lenght = top_border.get_width()

    # Thickness
    top_thickness =    top_border.get_height()
    right_thickness =  right_border.get_width()
    bottom_thickness = bottom_border.get_height()
    left_thickness =   left_border.get_width()

    # Min size
    width =  max(width,  right_thickness + left_thickness)
    height = max(height, top_thickness +   bottom_thickness)

    # Crop
    top_crop =    pygame.Surface((width - right_thickness,  top_thickness))
    right_crop =  pygame.Surface((right_thickness,          height - bottom_thickness))
    bottom_crop = pygame.Surface((width - left_thickness,   bottom_thickness))
    left_crop =   pygame.Surface((left_thickness,           height - top_thickness))

    # Cropping surface // chop
    top_crop.blit(top_border,        (0, 0))
    right_crop.blit(right_border,    (0, 0))
    bottom_crop.blit(bottom_border,  (-border_lenght + width - left_thickness,  0))
    left_crop.blit(left_border,      (0,  -border_lenght + height - top_thickness))

    top_crop.set_colorkey((0, 0, 0, 0))
    right_crop.set_colorkey((0, 0, 0, 0))
    bottom_crop.set_colorkey((0, 0, 0, 0))
    left_crop.set_colorkey((0, 0, 0, 0))

    frame_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    frame_surface.fill((0,0,0,0))

    # Draw on screen
    frame_surface.blit(top_crop,    (0,                            0))
    frame_surface.blit(right_crop,  (0 + width - right_thickness,  0))
    frame_surface.blit(bottom_crop, (0 + left_thickness,           0 + height - bottom_thickness))
    frame_surface.blit(left_crop,   (0,                            0 + top_thickness))

    return frame_surface




def show_3(dim, screen, game: dict, mpos, window, scroll_i=0, scroll_r=0, scroll_w=0, scroll_k=0):
    """
    Ordem:
    0. Seção principal (varia dependendo da(s) janela(s) abertas)
    1. Seção de recursos
    2. Cabeçalho
    3. Seletor de janelas

    Filosofo é uma função separada
    """

    # Importação de dados do game
    resources = game["data"]["resources"]
    works = game["data"]["works"]
    multiworks = game["data"]["multiworks"]
    knowledge = game["data"]["knowledge"]

    age = game["data"]["age"]
    current_day = game["data"]["current day"]
    golems = game["data"]["golems"]
    attributes = game["data"]["attributes"]



    # -1. Definição de seções da tela
    main =     pygame.Rect(dim[0] / 5,  dim[1] / 5,     dim[0] * 3 / 5,     dim[1] * 4 / 5)
    resource = pygame.Rect(0,           dim[1] / 5,     dim[0] / 5,         dim[1] * 4 / 5)
    header =   pygame.Rect(0,           0,              dim[0],             dim[1] / 5)

    main_col = main.collidepoint(mpos)
    resource_col = resource.collidepoint(mpos)
    header_col = header.collidepoint(mpos)

    # Determinar a seção que o mouse está
    mouse_over = None
    section = None

    if main_col:
        section = "work"
    elif resource_col:
        section = "resource"
    elif header_col:
        section = "header"



    # Dados do jogo
    unlocked_resources = [key for key in resources if resources[key]["unlocked"]]
    unlocked_works     = game["data"]["priorities"]
    unlocked_knowledge = [key for key in knowledge if knowledge[key]["unlocked"]]



    # Formatação
    font_size = int(dim[1]/36)
    font = pygame.font.Font("assets/computer modern.ttf", size=font_size)



    # 0. Seção principal
    if window == "production":
        background = pygame.image.load("assets/main.png").convert_alpha()
        background = pygame.transform.scale(background, dim)
        screen.blit(background, (0, 0))

        work_columns = 2     # x
        padding_fraction = 1/10   # f

        work_border = 12 * dim[0]/2560

        card_width = (main.width - work_border) / (work_columns + work_columns*padding_fraction + padding_fraction)
        card_height = card_width * 1/1.6
        padding = card_width * padding_fraction

        card_border = frame(dim, card_width, card_height, border="card")

        # Recursos
        for n, name in enumerate(unlocked_works):

            # Carta de recurso
            column = n % work_columns
            row = n // work_columns

            left = main.left + padding + column * (card_width + padding)
            top =  main.top  + padding + row *   (card_height + padding) + scroll_r

            card_rect = pygame.Rect(left, top, card_width, card_height)
            card_collision = card_rect.collidepoint(mpos)
            if card_collision:
                mouse_over = name

            card_alpha = pygame.Surface((card_width, card_height), pygame.SRCALPHA)
            card_alpha.fill((64*card_collision, 64*card_collision, 64*card_collision, 128))
            screen.blit(card_alpha, (left, top))
            screen.blit(card_border, (left, top))


            # Imagem
            reducer = card_height * 0.05
            img = pygame.image.load("assets/missing.png").convert_alpha()
            img = pygame.transform.scale(img, (card_height - 2*reducer, card_height - 2*reducer))
            screen.blit(img, (left+reducer, top+reducer))


            # Texto
            # Quantidade
            text = font.render(str(works[name]["golems working"]), True, (255, 255, 255))

            text_left = left + card_width - text.get_width() - card_width / 20
            centerer = (card_height - text.get_width()) / 2

            screen.blit(text, (text_left, top + centerer))

    elif window == "knowledge":
        background = pygame.image.load("assets/knowledge.png").convert_alpha()
        background = pygame.transform.scale(background, dim)
        screen.blit(background, (0, 0))

        knowledge_columns = 2     # x
        padding_fraction = 1/10   # f

        knowledge_border = 12 * dim[0]/2560

        card_width = (main.width - knowledge_border) / (knowledge_columns + knowledge_columns*padding_fraction + padding_fraction)
        card_height = card_width * 1/1.6
        padding = card_width * padding_fraction

        card_border = frame(dim, card_width, card_height, border="card")

        # Recursos
        for n, name in enumerate(unlocked_knowledge):

            # Carta de recurso
            column = n % knowledge_columns
            row = n // knowledge_columns

            left = main.left + padding + column * (card_width + padding)
            top =  main.top  + padding + row *   (card_height + padding) + scroll_r

            card_rect = pygame.Rect(left, top, card_width, card_height)
            card_collision = card_rect.collidepoint(mpos)
            if card_collision:
                mouse_over = name

            card_alpha = pygame.Surface((card_width, card_height), pygame.SRCALPHA)
            card_alpha.fill((64*card_collision, 64*card_collision, 64*card_collision, 128))
            screen.blit(card_alpha, (left, top))
            screen.blit(card_border, (left, top))


            # Imagem
            reducer = card_height * 0.05
            img = pygame.image.load("assets/missing.png").convert_alpha()
            img = pygame.transform.scale(img, (card_height - 2*reducer, card_height - 2*reducer))
            screen.blit(img, (left+reducer, top+reducer))


            # Texto
            # Quantidade
            text = font.render(str(knowledge[name]["learned"]), True, (255, 255, 255))

            text_left = left + card_width - text.get_width() - card_width / 20
            centerer = (card_height - text.get_width()) / 2

            screen.blit(text, (text_left, top + centerer))



    # 1. Recursos
    background = pygame.image.load("assets/resources.png").convert_alpha()
    background = pygame.transform.scale(background, dim)
    screen.blit(background, (0, 0))

    resource_columns = 5     # x
    padding_fraction = 1/5   # f

    resource_border = 12 * dim[0]/2560

    card_width = (resource.width - resource_border) / (resource_columns + resource_columns*padding_fraction + padding_fraction)
    card_height = card_width * 1.3
    padding = card_width * padding_fraction

    card_border = frame(dim, card_width, card_height, border="card")

    # Recursos
    for n, name in enumerate(unlocked_resources):

        # Carta de recurso
        column = n % resource_columns
        row = n // resource_columns

        left = resource.left + padding + column * (card_width + padding)
        top =  resource.top  + padding + row *   (card_height + padding) + scroll_r

        card_rect = pygame.Rect(left, top, card_width, card_height)
        card_collision = card_rect.collidepoint(mpos)
        if card_collision:
            mouse_over = name

        card_alpha = pygame.Surface((card_width, card_height), pygame.SRCALPHA)
        card_alpha.fill((64*card_collision, 64*card_collision, 64*card_collision, 128))
        screen.blit(card_alpha, (left, top))
        screen.blit(card_border, (left, top))


        # Imagem
        reducer = card_width * 0.05
        img = pygame.image.load("assets/missing.png").convert_alpha()
        img = pygame.transform.scale(img, (card_width - 2*reducer, card_width - 2*reducer))
        screen.blit(img, (left+reducer, top+reducer))


        # Texto
        # Quantidade
        text = font.render(str(resources[name]["quantity"]), True, (255, 255, 255))

        centerer = (card_width - text.get_width()) / 2
        text_top = top + (card_height)/1.5

        screen.blit(text, (left + centerer, text_top))




    # 3. Cabeçalho
    background = pygame.image.load("assets/header.png").convert_alpha()
    background = pygame.transform.scale(background, dim)
    screen.blit(background, (0, 0))


    # Verificar se o mouse está sobre algum retângulo    
    # all_rect = first_column_titles + unlocked_resources + list(unlocked_works.keys()) + unlocked_knowledge
    # if True in rect_collisions:
    #     mouse_over = all_rect[rect_collisions.index(True)]
    # else:
    #     mouse_over = None
        
    return mouse_over, section




def find_category(game: dict, name: Name) -> str:
    possibilities = ["resources", "works", "multiworks", "knowledge"]

    for i in possibilities:
        if name in list(game["data"][i].keys()):
            return i

    return None




def write(dim, screen, game:dict, mouse_over):
    # Coluna do philosopher
    section_left = dim[0] * 4 / 5
    section_top = dim[1] / 5
    section_width = dim[0] / 5

    # pygame.draw.rect(screen, (0,0,0), pygame.Rect(section_left, section_top, section_width, dim[1]))

    scale = dim[0] / (1.6*2560) 
    philosopher = pygame.image.load("assets/philosopher.png").convert_alpha()
    philosopher = pygame.transform.scale_by(philosopher, scale)

    centerer = (section_width - philosopher.get_width()) / 2
    screen.blit(philosopher, (section_left + centerer, section_top))

    font_size = int(dim[1]/18)
    font = pygame.font.Font("assets/computer modern.ttf", size=font_size)

    if mouse_over != None:
        text_to_blit = mouse_over.value if type(mouse_over) != str else mouse_over
        text = font.render(text_to_blit, True, (255, 255, 255))
    else: 
        text = font.render("None", True, (255, 255, 255))

    centerer = (section_width - text.get_width()) / 2
    screen.blit(text, (section_left + centerer, section_top*2))








# Initialize pygame

pygame.init()

# dim = (1280, 720)
dim = (1*1920, 1*1080)
# dim = (2560, 1440)  # 2k
screen = pygame.display.set_mode(dim)
pygame.display.set_caption("Megolemania / Golems Ascendancy")

running = True
clock = pygame.time.Clock()
delta_time = 0.1
time_accumulator = 0

font = pygame.font.Font(None, size=30)

game = init_game()
#load game
window = "production"
scroll_i = 0
scroll_r = 0
scroll_w = 0
scroll_k = 0
scroll_lenght = 50



# Loop
while running:
    # Clean everything from last frame
    screen.fill((0,0,0))
    # Mouse position
    mpos = pygame.mouse.get_pos()
    
    # Show
    #mouse_over, column = show(dim, screen, game, mpos, scroll_i, scroll_r, scroll_w, scroll_k)
    mouse_over, column = show_3(dim, screen, game, mpos, window, scroll_i, scroll_r, scroll_w, scroll_k)
    write(dim, screen, game, mouse_over)

    # Checar colisão do mouse
    text = font.render(column, True, (255, 255, 255))
    screen.blit(text, (0, 40))


    # Não deixar você scrollar pra cima
    # scroll_i = 0 if scroll_i > 0 else scroll_i
    # scroll_r = 0 if scroll_r > 0 else scroll_r
    # scroll_w = 0 if scroll_w > 0 else scroll_w
    # scroll_k = 0 if scroll_k > 0 else scroll_k

    # Event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                window = "production"
            if event.key == pygame.K_2:
                window = "knowledge"

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                category = find_category(game, mouse_over)
                if category == "works":
                    employ_golem(game, mouse_over)
                elif category == "multiwork":
                    build_multiwork(game, mouse_over)
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
                elif category == "multiwork":
                    break_multiwork(game, mouse_over)

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

    # fazer a função de autosave e colocar pra salvar antes de QUIT, também colocar pra procurar o save antes de dar init_game()


    # Duração do dia
    # default 2
    days_per_second = 2
    days_per_second = min(days_per_second, 60)
    day_duration = 1.0 / days_per_second
    if time_accumulator >= day_duration:
        time_accumulator -= day_duration
        update_game(game)

    # Framerate
    pygame.display.flip()
    delta_time = clock.tick(60) / 1000
    time_accumulator += delta_time
    delta_time = max(0.001, min(0.1, delta_time))
pygame.quit()

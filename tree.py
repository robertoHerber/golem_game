import pygame
import sys
from collections import deque

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

# Node settings
NODE_WIDTH = 120
NODE_HEIGHT = 60
HORIZONTAL_SPACING = 80
VERTICAL_SPACING = 100

def draw_knowledge_tree(screen, knowledge_data, font):
    # Calculate node positions using BFS for tree layout
    nodes = {}
    levels = {}
    
    # Find root nodes (nodes with no dependencies)
    roots = [name for name, data in knowledge_data.items() if not data['dependencies']]
    
    # Assign levels using BFS
    queue = deque()
    for root in roots:
        queue.append((root, 0))
        levels[root] = 0
    
    while queue:
        current, level = queue.popleft()
        for name, data in knowledge_data.items():
            if current in data['dependencies']:
                if name not in levels or levels[name] < level + 1:
                    levels[name] = level + 1
                    queue.append((name, level + 1))
    
    # Group nodes by level
    level_groups = {}
    for node, level in levels.items():
        if level not in level_groups:
            level_groups[level] = []
        level_groups[level].append(node)
    
    # Calculate positions
    max_level = max(level_groups.keys()) if level_groups else 0
    screen_width = screen.get_width()
    
    for level in sorted(level_groups.keys()):
        nodes_in_level = level_groups[level]
        total_width = len(nodes_in_level) * NODE_WIDTH + (len(nodes_in_level) - 1) * HORIZONTAL_SPACING
        start_x = (screen_width - total_width) // 2
        y = 50 + level * (NODE_HEIGHT + VERTICAL_SPACING)
        
        for i, node in enumerate(nodes_in_level):
            x = start_x + i * (NODE_WIDTH + HORIZONTAL_SPACING)
            nodes[node] = (x, y, NODE_WIDTH, NODE_HEIGHT)
    
    # Draw connections first (so they're behind nodes)
    for name, data in knowledge_data.items():
        if name in nodes:
            x1 = nodes[name][0] + NODE_WIDTH // 2
            y1 = nodes[name][1]
            
            for dep in data['dependencies']:
                if dep in nodes:
                    x2 = nodes[dep][0] + NODE_WIDTH // 2
                    y2 = nodes[dep][1] + NODE_HEIGHT
                    pygame.draw.line(screen, BLACK, (x1, y1), (x2, y2), 2)
    
    # Draw nodes
    for name, rect in nodes.items():
        x, y, w, h = rect
        pygame.draw.rect(screen, GRAY, (x, y, w, h))
        pygame.draw.rect(screen, BLACK, (x, y, w, h), 2)
        
        # Draw name (split if too long)
        name_parts = name.split('_')
        for i, part in enumerate(name_parts):
            text = font.render(part, True, BLACK)
            text_rect = text.get_rect(center=(x + w // 2, y + h // 2 - (len(name_parts) - 1) * 10 + i * 20))
            screen.blit(text, text_rect)
    
    return nodes

def main():
    # Screen setup
    width, height = 1200, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Knowledge Tree Visualization")
    
    # Font setup
    font = pygame.font.SysFont('Arial', 14)
    
    # Prepare knowledge data (convert from your format)
    knowledge_data = {
        "WOOD_CUTTING": {
            "dependencies": [],
            "work_unlocked": ["LUMBERJACK"]
        },
        "FLINT_PROCESSING": {
            "dependencies": [],
            "work_unlocked": ["FLINT_KNAPPER"]
        },
        "PRIMITIVE_WEAPONS": {
            "dependencies": ["FLINT_PROCESSING", "WOOD_CUTTING"],
            "work_unlocked": ["SPEAR_MAKER"]
        },
        "BASIC_HUNTING": {
            "dependencies": ["PRIMITIVE_WEAPONS"],
            "work_unlocked": ["HUNTER"]
        },
        "LEATHER_WORKING": {
            "dependencies": ["BASIC_HUNTING"],
            "work_unlocked": ["ROPE_MAKER"]
        },
        "BOW_MAKING": {
            "dependencies": ["LEATHER_WORKING", "WOOD_CUTTING"],
            "work_unlocked": ["BOWYER"]
        },
        "FIRE_CONTROL": {
            "dependencies": ["WOOD_CUTTING"],
            "work_unlocked": ["CHARCOAL_MAKER"]
        },
        "DRYING_TECHNIQUES": {
            "dependencies": ["FIRE_CONTROL", "BASIC_HUNTING"],
            "work_unlocked": ["MEAT_DRIER"]
        },
        "CLAY_WORKING": {
            "dependencies": [],
            "work_unlocked": ["POTTERY_MAKER"]
        },
        "BASIC_MINING": {
            "dependencies": ["FLINT_PROCESSING"],
            "work_unlocked": ["MINER"]
        },
        "BASIC_TOOL_MAKING": {
            "dependencies": ["FLINT_PROCESSING", "WOOD_CUTTING"],
            "work_unlocked": ["TOOL_MAKER"]
        },
        "FOOD_PRESERVATION": {
            "dependencies": ["DRYING_TECHNIQUES", "CLAY_WORKING"],
            "work_unlocked": []
        },
        "KILN_CONSTRUCTION": {
            "dependencies": ["CLAY_WORKING", "FIRE_CONTROL"],
            "work_unlocked": ["BUILDER"]
        },
        "SMELTING_PREPARATIONS": {
            "dependencies": ["BASIC_MINING", "FIRE_CONTROL"],
            "work_unlocked": []
        },
        "FURNACE_BUILDING": {
            "dependencies": ["KILN_CONSTRUCTION", "SMELTING_PREPARATIONS"],
            "work_unlocked": ["FURNACE_OPERATOR"]
        },
        "BRONZE_SMELTING": {
            "dependencies": ["FURNACE_BUILDING"],
            "work_unlocked": []
        }
    }
    
    # Main loop
    clock = pygame.time.Clock()
    nodes = {}
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill(WHITE)
        nodes = draw_knowledge_tree(screen, knowledge_data, font)
        
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
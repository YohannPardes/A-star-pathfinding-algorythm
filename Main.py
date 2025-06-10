import pygame, time

BOARD_SIZE = 50
CELL_SIZE  = 16
WIDTH = HEIGHT = BOARD_SIZE * CELL_SIZE
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
board = []

class Node:
    starting_node = None
    ending_node = None
    def __init__(self, x, y, starting_node = False, IsAvailable = True):

        self.IsAvailable = IsAvailable
        self.starting_node = starting_node
        self.pos = (x, y)

        self.Fcost = None
        self.Hcost = 0
        self.Gcost = float("inf")

        self.checked = False
        self.searched = False
        self.previous = None


    def get_neighbors(self, board):
        # self.checked = True

        directions = [(1,0), (1, 1), (0, 1), (-1, 0), (-1, 1), (1, -1), (0, -1), (-1, -1)]
        x, y = self.pos
        neighbors = []

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                neighbor = board[ny][nx]
                if neighbor.IsAvailable:
                    neighbors.append(neighbor)
        return neighbors

    def update_costs(self, parent):
        px, py = parent.pos
        cx, cy = self.pos
        diagonal = px != cx and py != cy
        step_cost = 14 if diagonal else 10
        tentative_g = parent.Gcost + step_cost

        if tentative_g < self.Gcost:
            self.previous = parent
            self.Gcost = tentative_g
            dx = abs(cx - Node.ending_node.pos[0])
            dy = abs(cy - Node.ending_node.pos[1])
            self.Hcost = 14 * min(dx, dy) + 10 * abs(dx - dy)
            self.Fcost = self.Gcost + self.Hcost

    def show(self):

        color = (255, 255, 255)  # default white
        if not self.IsAvailable:
            color = (0, 0, 0)  # wall
        elif self.checked:
            color = (255, 255, 0)  # final path
        elif self.searched:
            color = (0, 200, 0)  # explored

        pygame.draw.rect(screen, color, (self.pos[0] * CELL_SIZE, self.pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
def print_board(board):
    for ligne in board:
        print()
        for node in ligne:
            print(node.Fcost, end = " ")

    print()

#initializing the board
for _ in range(BOARD_SIZE):
    board.append([])

for y, ligne in enumerate(board):
    for x in range(BOARD_SIZE):
        ligne.append(Node(x, y))

Node.starting_node = board[0][0]
Node.ending_node = board[BOARD_SIZE - 1][BOARD_SIZE - 1]

start_node = Node.starting_node
end_node = Node.ending_node
start_node.Gcost = 0
start_node.Hcost = 14 * min(abs(start_node.pos[0] - end_node.pos[0]), abs(start_node.pos[1] - end_node.pos[1])) + 10 * abs(abs(start_node.pos[0] - end_node.pos[0]) - abs(start_node.pos[1] - end_node.pos[1]))
start_node.Fcost = start_node.Hcost

open_set = {start_node}
closed_set = set()

done = False
start = False

while not done:
    screen.fill((255, 255, 255))
    for row in board:
        for node in row:
            node.show()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            x = x // (SIZE[0] // BOARD_SIZE)
            y = y // (SIZE[1] // BOARD_SIZE)
            node = board[y][x]
            if node != Node.starting_node and node != Node.ending_node:
                node.IsAvailable = not node.IsAvailable

    if start and open_set:
        current = min(open_set, key=lambda n: n.Fcost)
        open_set.remove(current)
        current.searched = True
        closed_set.add(current)

        if current == Node.ending_node:
            # Reconstruct path
            path = []
            while current:
                current.checked = True
                path.append(current)
                current = current.previous
            start = False
            continue

        for neighbor in current.get_neighbors(board):
            if neighbor in closed_set:
                continue
            neighbor.update_costs(current)
            if neighbor not in open_set:
                open_set.add(neighbor)

    pygame.display.flip()
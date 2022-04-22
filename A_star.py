import pygame, time

WIDTH = HEIGHT = 800
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)

board = []
board_size = 50

class Node:
    starting_node = None
    ending_node = None
    def __init__(self, x, y, starting_node = False, IsAvailable = True):

        self.Fcost = None
        self.pos = (x, y)
        self.starting_node = starting_node

        self.IsAvailable = IsAvailable
        self.checked = False
        self.searched = False

        self.previous = None
    
    def get_neighbors(self, board):
        # self.checked = True

        neighbors = [(1,0), (1, 1), (0, 1), (-1, 0), (-1, 1), (1, -1), (0, -1), (-1, -1)]
        neighbors = [(x, y) for (x, y) in neighbors if (board_size-1)>=self.pos[0]+x>=0 and (board_size-1)>=self.pos[1]+y>=0]

        neighbors = [board[self.pos[1]+y][self.pos[0]+x] for (x, y) in neighbors if board[self.pos[1]+y][self.pos[0]+x].IsAvailable]

        # print(self.pos, [neighbor.pos for neighbor in neighbors])

        return neighbors

    def calc_heuristic_cost(self):
        #calculating Gcost
        x1, y1 = Node.starting_node.pos
        x2, y2 = self.pos

        dist_brut = abs(x2-x1) + abs(y2-y1) 
        dist_adja = abs(abs(x2-x1)-abs(y2-y1)) 
        diagonal = (dist_brut - dist_adja)/2

        Gcost = diagonal*14+dist_adja*10

        #calculating Hcost
        x1, y1 = Node.ending_node.pos
        x2, y2 = self.pos

        dist_brut = abs(x2-x1) + abs(y2-y1) 
        dist_adja = abs(abs(x2-x1)-abs(y2-y1)) 
        diagonal = (dist_brut - dist_adja)/2

        Hcost = diagonal*14+dist_adja*10

        self.Hcost = Hcost
        self.Fcost = Hcost+Gcost

    def show(self):
        color = (100, 100 , 255) if self.IsAvailable else (0,0,0)
        color = (0, 200, 0) if self.searched else color
        color = (200, 0, 0) if self.checked else color
        if self.Fcost or not self.IsAvailable:
            pygame.draw.rect(screen, color, ((self.pos[0]*(SIZE[0]//board_size)), (self.pos[1]*(SIZE[1]//board_size)),((SIZE[0]//board_size)), (SIZE[1]//board_size)))
        
def print_board(board):
    for ligne in board:
        print()
        for node in ligne:
            print(node.Fcost, end = " ")

    print()

for _ in range(board_size):
    board.append([])
for y, ligne in enumerate(board):
    for x in range(board_size):
        ligne.append(Node(x, y))

Node.starting_node = board[0][0]
Node.ending_node = board[board_size-1][board_size-1]
starting_node = board[0][0]
starting_node.Fcost = 0

screen.fill((255, 255, 255))
starting_node.show()
pygame.display.flip()


print(starting_node.get_neighbors(board))
next_node = starting_node
current_node = None

done = False
start = False
while not done:
    next_node.searched = True
    current_node = next_node
    previous = current_node
    screen.fill((255, 255, 255))
    for ligne in board:
            for node in ligne:
                node.show()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN:
            if event.key == 32:
                start = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            x = int(x//(SIZE[0]/board_size))
            y = int(y//(SIZE[1]/board_size))
            
            board[y][x].IsAvailable = False if board[y][x].IsAvailable else True

    if start:
        # time.sleep(0.01)
        for node in current_node.get_neighbors(board):
            node.calc_heuristic_cost()
        # print_board(board)
        # print()

        next_node = None
        best_Fcost = 10000000000
        for ligne in board:
            for node in ligne:
                if node.Fcost and not node.searched:
                    if node.Hcost == 0:
                        Node.ending_node.checked = True
                        start = False
                        path = []
                        path.append(current_node)
                        while current_node.previous:
                            path.append(current_node.previous)
                            current_node = current_node.previous
                        for node in path:
                            node.checked = True

                    if node.Fcost<best_Fcost:
                        next_node = node
        
        next_node.previous = previous


    pygame.display.flip()
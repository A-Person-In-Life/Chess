from game_logic import BoardState
import pygame

WIDTH, HEIGHT = 800, 800
CELL_SIZE = WIDTH // 8
COLORS = [(109, 129, 150), (210, 180, 140), (100, 100, 100), (0,0,0), (118, 118, 118)]
ROWS, COLS = 8, 8

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
fonts = [pygame.font.SysFont('Arial', 56)]

board = BoardState()
selected = None

images = {
            "PawnW" : pygame.image.load("assets/images/white_pawn.png").convert_alpha(),
            "PawnB" : pygame.image.load("assets/images/black_pawn.png").convert_alpha(),
            "BishopW": pygame.image.load("assets/images/white_bishop.png").convert_alpha(),
            "BishopB": pygame.image.load("assets/images/black_bishop.png").convert_alpha(),
            "RookW": pygame.image.load("assets/images/white_rook.png").convert_alpha(),
            "RookB": pygame.image.load("assets/images/black_rook.png").convert_alpha(),
            "QueenW": pygame.image.load("assets/images/white_queen.png").convert_alpha(),
            "QueenB": pygame.image.load("assets/images/black_queen.png").convert_alpha(),
            "KnightW": pygame.image.load("assets/images/white_knight.png").convert_alpha(),
            "KnightB": pygame.image.load("assets/images/black_knight.png").convert_alpha(),
            "KingW": pygame.image.load("assets/images/white_king.png").convert_alpha(),
            "KingB": pygame.image.load("assets/images/black_king.png").convert_alpha(),
            }

captureSound = pygame.mixer.Sound("assets/sound/capture.mp3")
moveSound = pygame.mixer.Sound("assets/sound/move-self.mp3")

def draw_possible_moves(selected):
    legal = board.get_legal_moves(selected[0], selected[1])
    for move in legal:
        if board.getPiece(move[0], move[1]) is None:
            pygame.draw.circle(screen,COLORS[2],((move[1]*CELL_SIZE)+CELL_SIZE//2,(move[0]*CELL_SIZE)+CELL_SIZE//2),40)
        elif board.getPiece(move[0],move[1]).color is not board.getPiece(selected[0],selected[1]).color:
            pygame.draw.circle(screen,COLORS[2],((move[1]*CELL_SIZE)+CELL_SIZE//2,(move[0]*CELL_SIZE)+CELL_SIZE//2),50, 8)

SQUARES = [pygame.Rect(c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE) for c in range(COLS) for r in range(ROWS) ]

def draw():
    for r in range(ROWS):
        for c in range(COLS):
            color = COLORS[(r + c) % 2]
            pygame.draw.rect(screen, color, SQUARES[r * COLS + c])
    if selected:
        draw_possible_moves(selected)
    for r in range(ROWS):
        for c in range(COLS):
            piece = board.getPiece(r,c)
            if piece:
                screen.blit(images[piece.name + piece.color[0].upper()],(c*CELL_SIZE,r*CELL_SIZE))

def drawWin(color):
    x = WIDTH/3
    y = HEIGHT/3
    w = WIDTH/3
    h = HEIGHT/8
    rect = pygame.Rect(x, y, w, h)
    rect.center = WIDTH / 2, HEIGHT / 2

    pygame.draw.rect(screen, COLORS[4], rect, border_radius=10)
    text = fonts[0].render(f"{color} Wins!", True, COLORS[3])#text, antialias, color(rgb)

    pygame.Surface.blit(screen, text, (rect.topleft[0]+10, rect.topleft[1]+15))
                
running = True
ended = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if ended:
                running = False
                continue
            col, row = pygame.mouse.get_pos()
            col, row = col // CELL_SIZE, row // CELL_SIZE
            if selected is None:
                piece = board.getPiece(row, col)
                if piece and piece.color == board.turn:
                    selected = (row, col)
                    
            else:
                if board.is_legal_move(selected[0], selected[1], row, col):
                    board.simulate_move(selected[0], selected[1], row, col)    
                    moveSound.play()
                else:
                    #add invalid move feedback
                    pass
                selected = None

    draw()
    if board.is_checkmate(board.turn):
        drawWin("White" if board.turn == "black" else "Black")
        ended = True
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
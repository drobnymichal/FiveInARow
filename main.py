import pygame
from typing import List, Optional

UNKNOWN = 0
X = 1
O = 2

class Playground:
    def __init__(self, size_x: int, size_y: int) -> None:
        self.size_x: int = size_x
        self.size_y: int = size_y
        self.repre: Optional[List[List[int]]] = None

    def make_repre(self: 'Playground') -> None:
        if self.size_x < 5 or self.size_y < 5:
            print("[ERROR] : Entered too small size of playground.")
            return None
        self.repre = [[UNKNOWN for _ in range(self.size_x)] for _ in range(self.size_y)]
        return None

    def insert(self, a_x: int, a_y: int, value: int) -> bool:
        if a_x < 0 or a_x >= self.size_x or a_y < 0 or a_y >= self.size_x:
            return False
        if self.repre[a_y][a_x] != UNKNOWN:
            return False
        self.repre[a_y][a_x] = value
        return True

    def check_row(self, a_x: int, a_y: int, value: int) -> bool:
        if a_x > self.size_x - 5:
            return False
        for x in range(a_x, a_x + 5):
            if self.repre[a_y][x] != value:
                return False
        return True

    def check_col(self, a_x: int, a_y: int, value: int) -> bool:
        if a_y > self.size_y - 5:
            return False
        for y in range(a_y, a_y + 5):
            if self.repre[y][a_x] != value:
                return False
        return True

    def check_diag_right(self, a_x: int, a_y: int, value: int) -> bool:
        if a_y > self.size_y - 5 or a_x > self.size_x - 5:
            return False
        for var in range(5):
            if self.repre[a_y + var][a_x + var] != value:
                return False
        return True

    def check_diag_left(self, a_x: int, a_y: int, value: int) -> bool:
        if a_y > self.size_y - 5 or a_x < 4:
            return False
        for var in range(5):
            if self.repre[a_y + var][a_x - var] != value:
                return False
        return True

    def check_winner(self) -> bool:
        for y in range(self.size_y):
            for x in range(self.size_x):
                if self.repre[y][x] != UNKNOWN:
                    value = self.repre[y][x]
                    if self.check_row(x, y, value) \
                    or self.check_col(x, y, value) \
                    or self.check_diag_right(x, y, value) \
                    or self.check_diag_left(x, y, value):
                        return True
            
        return False


class Options:
    def __init__(self) -> None:
        self.done = False
        self.screen = None
        self.clock = None
        self.turn = O
        self.reset = False
        self.home_screen = True
        self.game_screen = False
        self.end_screen = False
        self.mouse_pos = (0, 0)
        self.screen_size = [1280, 720]
        self.margin = 10
        self.width = 40
        self.height = 40



# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (30,144,255)


SCREEN_SIZE = [1200, 710]
MARGIN = 10
WIDTH = 40
HEIGHT = 40


def draw_cross(column, row, options):
    pygame.draw.line(options.screen, BLUE, 
            ((MARGIN + WIDTH) * column + MARGIN + 1, (MARGIN + HEIGHT) * row + MARGIN), 
            ((MARGIN + WIDTH) * (column + 1) - 4, (MARGIN + HEIGHT) * (row + 1) - 1), width=8)
    pygame.draw.line(options.screen, BLUE, 
            ((MARGIN + WIDTH) * column + MARGIN + 1, (MARGIN + HEIGHT) * (row + 1) - 1), 
            ((MARGIN + WIDTH) * (column + 1) - 4, (MARGIN + HEIGHT) * row + MARGIN), width=8)


def draw_crircle(column, row, options):
    x = (MARGIN + WIDTH) * column + (MARGIN + WIDTH + MARGIN) // 2
    y = (MARGIN + HEIGHT) * row + (MARGIN + HEIGHT + MARGIN) // 2 
    pygame.draw.circle(options.screen, RED, (x, y), 20, width=8)
    return None

def draw_empty(column, row, options):
    pygame.draw.rect(options.screen, WHITE, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
    return None


def draw_playground(playground: Playground, options: Options):
    for row in range(playground.size_y):
        for column in range(playground.size_x):
            draw_empty(column, row, options)
            
            if playground.repre[row][column] == X:
                draw_cross(column, row, options)
            elif playground.repre[row][column] == O:
                draw_crircle(column, row, options)
    return None


def init_pygame(options: Options):
    pygame.init()
    options.screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Piškvorky")
    options.clock = pygame.time.Clock()
    return None


def interaction(options: Options) -> bool:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            options.done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONUP:
            # User clicks the mouse. Get the position
            if options.home_screen:
                options.home_screen = False
                options.game_screen = True
                return False
            print("INVALID")
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            options.mouse_pos = (pos[0] // (WIDTH + MARGIN), pos[1] // (HEIGHT + MARGIN))
            # Set that location to one
            return True
        elif event.type == pygame.KEYDOWN:
            print("VALID")
            options.reset = True
            return True
    return False


def change_playground(options: Options, playground: Playground):
    if options.mouse_pos[0] >= playground.size_x or options.mouse_pos[1] >= playground.size_y:
        return None
    x = options.mouse_pos[0]
    y = options.mouse_pos[1]
    if playground.insert(x, y, options.turn):
        if options.turn == X:
            options.turn = O
        else:
            options.turn = X
        if playground.check_winner():
            options.end_screen = True
            options.game_screen = False
            draw_playground(playground, options)

            return None
    return None


def end_scr(options: Options):
    name = "ČERVENÝ"
    color = RED
    if options.turn == O:
        name = "MODRÝ"
        color = BLUE
    msg = "VYHRÁL"

    again = "PRO RESTART ZMÁČKNI KLÁVESU R"

    font2 = pygame.font.Font("OpenSans-Bold.ttf", 60)
    text2 = font2.render(name, True, color, WHITE)
    text_rect2 = text2.get_rect()
    text_rect2.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 )

    options.screen.blit(text2, text_rect2)

    font1 = pygame.font.Font("OpenSans-Bold.ttf", 40)
    text = font1.render(msg, True, BLACK, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - 50)
    
    options.screen.blit(text, text_rect)

    font = pygame.font.Font("OpenSans-Bold.ttf", 20)
    text = font.render(again, True, BLACK, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + 150)

    options.screen.blit(text, text_rect)

    return None


def home_screen(options: Options) -> None:
    options.screen.fill(WHITE)

    font = pygame.font.Font("OpenSans-Bold.ttf", 40)
    text = font.render("PRO ZAČÁTEK HRY STISKNI LIBOVOLNOU KLÁVESU", True, BLACK, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)
    options.screen.blit(text, text_rect)
    
    return None
    

def mainloop():
    options = Options()
    init_pygame(options)
    playground = Playground(20, 20)
    playground.make_repre()
    tim = 0

    while not options.done:
        if interaction(options) and not options.end_screen and not options.home_screen:
            if options.reset:
                playground.make_repre()
                new = Options()
                new.screen = options.screen
                new.clock = options.clock
                options = new
                tim = 0
            else:
                change_playground(options, playground)

        if options.reset:
            playground.make_repre()
            new = Options()
            new.screen = options.screen
            new.clock = options.clock
            options = new
            tim = 0
        
        elif options.end_screen:
            tim += 1

        elif options.home_screen:
            home_screen(options)

        elif options.end_screen and tim > 180:
            options.screen.fill(WHITE)
            end_scr(options)

        elif options.game_screen:
            options.screen.fill(BLACK)
            draw_playground(playground, options)
    
        options.clock.tick(60)

        pygame.display.flip()
        
    pygame.quit()
    return None
    


if __name__ == "__main__":
    mainloop()
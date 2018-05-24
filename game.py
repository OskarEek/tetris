import logging
import pygame
import sys
from random import randint

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Konstanter
FPS = 20
SCREEN_SIZE = (800, 600)
CAPTION = "Pygame Example"

COLOR = {'playfield': pygame.Color('#030116'),
         'bg': pygame.Color('#333333'),
}

TILE_COLORS = [False,
               pygame.Color('#0D03FF'),
               pygame.Color('#FF0000'),
               pygame.Color('#FFEB00'),
               pygame.Color('#1AD403'),
               pygame.Color('#E80C86'),
               pygame.Color('#DFF0FE'),
               pygame.Color('#611F03')]

# Game states

class Controller():
    """Game controller."""
    STATE_PREGAME = 1
    STATE_RUNNING = 2
    STATE_GAMEOVER = 3

    def __init__(self):
        """Initialize game controller."""
        self.fps = FPS

        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()




        #self.Shapes = Shapes(self.screen)
        # self.player = Player(self.screen)
        # self.player = Player(self.screen)
        # Initialize game state
        self.game_state = Controller.STATE_PREGAME


    def run(self):
        """Main game loop."""
        while True:
            # if self.game_state == STATE_PREGAME:
            #     if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:


            # Hantera speltillstånd
            if self.game_state == Controller.STATE_PREGAME:
                self.playfield = Playfield(self.screen)
                self.shape = Shape(self)
                self.game_state = Controller.STATE_RUNNING

                self.game_state = Controller.STATE_RUNNING


            if self.game_state == Controller.STATE_RUNNING:
                self.playfield.tick()
                self.shape.tick()

                self.screen.fill(COLOR['bg'])
                self.playfield.draw()
                self.shape.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # ALT + F4 or icon in upper right corner.
                    self.quit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # Escape key pressed.
                    self.quit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    self.shape.move_right()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    self.shape.move_left()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    self.shape.rotate_cw()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    self.shape.rotate_ccw()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.shape.boost()

#                if self.player.y > SCREEN_SIZE[1] - 10 or self.player.y < 10:
#                    logger.debug('OUT OF BOUNDS!')
#                    self.game_state = STATE_GAMEOVER



            if self.game_state == Controller.STATE_GAMEOVER:
                self.quit()  # Gör något bättre.

            pygame.display.flip()

            self.clock.tick(self.fps)
    def quit(self):
        logging.info('Quitting... good bye!')
        pygame.quit()
        sys.exit()

    def next_shape(self):
        self.playfield.add_shape(self.shape)
        self.playfield.remove_rows()
        self.shape = Shape(self)

class Playfield():
    def __init__(self, screen):
        self.x = SCREEN_SIZE[0] / 2  - 300 / 2
        self.y = SCREEN_SIZE[1] / 2 - 600 / 2
        self.screen = screen
        self.grid = [[0 for _ in range(10)] for _ in range(23)]
        self.speed = 1
        self.level = 1

        #self.staticshapes = {}

    def remove_rows(self):
        logger.debug('Attempting to remove full rows.')
        for row in self.grid[:]:
            remove = True
            for tile in row:
                if tile == 0:
                    remove = False

            if remove:
                self.grid.remove(row)
                self.grid.append([0 for _ in range(10)])

    def add_shape(self, shape):
        x, y, color = shape.x, shape.y, shape.color
        for xo, yo in shape.shape:
            self.grid[y + yo][x + xo] = color

    def draw(self):
        surface = pygame.Surface((300, 600))
        surface.fill(COLOR['playfield'])

        for row in range(20):
            for column in range(10):
                if self.grid[row][column] > 0:
                    pygame.draw.rect(surface,
                                     TILE_COLORS[self.grid[row][column]],
                                     (30 * column + 2, 30 * (19 - row) + 2, 26, 26))

        self.screen.blit(surface, (self.x, self.y))


    def tick(self):
        pass
        # for row in range(20):
        #     for column in range(10):
        #         if self.grid[row][column] > 0:
        #             if self.grid[row - 1][column] == 0:
        #                 self.grid[row - 1][column] = self.grid[row][column]
        #                 self.grid[row][column] = 0
        #                 if self.grid[row][column] > 0 and row == 0:



class Shape():
    def __init__(self, controller):
        #self.grid = Playfield(self.grid)
        self.controller = controller
        self.screen = controller.screen
        self.x = 5
        self.y = 20
        self.speed = self.controller.playfield.speed
        self.level = self.controller.playfield.level
        self.playfield_position = (SCREEN_SIZE[0] / 2  - 300 / 2,
                                   SCREEN_SIZE[1] / 2 - 600 / 2)
        self.num_ticks = 0

        self.shape, self.color = Shape._generate_shape()

    @staticmethod
    def _generate_shape():
        a = randint(0, 6)
        SHAPES = [([[0, 1], [-1, 0], [0, 0], [1, 0]], 1),
                  ([[1, 0], [0, 0], [2, 0], [-1, 0]], 2),
                  ([[1, 0], [0, 1], [1, 1], [0, 0]], 3),
                  ([[0, 1], [0, 0], [1, 0], [1, -1]], 4),
                  ([[0, 0], [1, 0], [0, 1], [0, 2]], 5),
                  ([[0, 0], [0, 1], [-1, 0], [-1, -1]], 6),
                  ([[0, 0], [0, 1], [0, 2], [-1, 0]], 7)
                  ]


        return SHAPES[a]

    def move_right(self):
        for xo, yo in self.shape:
            if (self.x + xo + 1) > 9 or self.controller.playfield.grid[self.y + yo][self.x + xo + 1] != 0:
                return
        self.x += 1

    def move_left(self):
        for xo, yo in self.shape:
            if (self.x + xo - 1) < 0 or self.controller.playfield.grid[self.y + yo][self.x + xo - 1] != 0:
                return
        self.x -= 1


    def rotate_cw(self):
        new_shape = []
        for xo, yo in self.shape:
            new_shape.append([yo, -xo])

        for xo, yo in new_shape:
            if (self.x + xo) < 0 or (self.x + xo) > 9 or (self.y + yo) < 0 or \
                    self.controller.playfield.grid[self.y + yo][self.x + xo] != 0:
                return

        self.shape = new_shape


    def rotate_ccw(self):
        new_shape = []
        for xo, yo in self.shape:
            new_shape.append([-yo, xo])

        for xo, yo in new_shape:
            if (self.x + xo) < 0 or (self.x + xo) > 9 or (self.y + yo) < 0 or \
                    self.controller.playfield.grid[self.y + yo][self.x + xo] != 0:
                return

        self.shape = new_shape

    def boost(self):
        boost = True
        while True:
            if self.valid_move():
                self.y -= 1
            else:
                break
        boost = False

    def lvl(self):
        logger.debug('lvlfunc: {}'.format(self.level))
        if self.level == 2:
            logger.debug(self.speed)
            self.controller.playfield.speed += 0.3
            self.controller.playfield.level = 0


    def draw(self):
        surface = pygame.Surface((300, 600), pygame.SRCALPHA)

        for xo, yo in self.shape:
            pygame.draw.rect(surface,
                             TILE_COLORS[self.color],
                             (30 * (self.x + xo) + 2, 30 * (19 - (self.y + yo)) + 2, 26, 26))


        self.screen.blit(surface, self.playfield_position)


    def tick(self):
        # logger.debug('level: {}'.format(self.level))
        # logger.debug('speed: {}'.format(self.speed))
        self.num_ticks = self.num_ticks + self.speed if self.num_ticks < 10 else 0

        if self.num_ticks == 0:
            if self.game_over():
                self.controller.quit()

        if self.num_ticks == 0:
            if self.valid_move():
                self.y -= 1
            else:
                #self.controller.playfield.staticshapes[(self.x, self.y)] = self.shape
                self.controller.playfield.level += 1

                self.controller.next_shape()
                self.lvl()
                #logger.debug(self.controller.playfield.staticshapes)


    def valid_move(self):
        for xo, yo in self.shape:
            if (self.y + yo - 1) < 0 or self.controller.playfield.grid[self.y + yo - 1][self.x + xo ] != 0:
                return False
        return True

    def game_over(self):
        for xo, yo in self.shape:
            if self.controller.playfield.grid[self.y + yo][self.x + xo]:
                return True
        return False


if __name__ == "__main__":
    logger.info('Starting...')
    c = Controller()
    c.run()

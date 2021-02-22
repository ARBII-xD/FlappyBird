import pygame, sys, random
from pygame import font


class Flappy:
    clock = None
    surface = None

    def __init__(self):
        # Initializing blank screen and game font
        pygame.init()
        self.screen = pygame.display.set_mode((280, 510))
        self.clock = pygame.time.Clock()
        self.gameFont = pygame.font.SysFont("calibri", 22)
        # Adding Background
        self.surface = pygame.image.load('images/background-night.png').convert()
        self.start = pygame.image.load("images/start.png").convert()
        # Adding Floor Image
        self.floor = pygame.image.load("images/base.png").convert()
        self.floor_x_position = 0
        # Adding bird picture
        self.player = pygame.image.load('images/yellowbird-midflap.png')
        self.player_rect = self.player.get_rect(center=(50, 255))
        # Code for the downward force on bird
        self.downward_force = 0.25
        self.move = 0
        # start screen
        self.game_condition = False
        # Variables related to poles
        self.pole_surface = pygame.image.load('images/pipe-red.png')
        self.MAKEPIPE = pygame.USEREVENT
        pygame.time.set_timer(self.MAKEPIPE, 1200)
        self.pole_length = [200, 300, 400]
        self.pole_list = []
        self.score = 0
        self.high_score = 0
        # Start Screen Image
        self.gameOver_surface = pygame.image.load("images/start.png").convert_alpha()
        self.gameOver_rect = self.gameOver_surface.get_rect(center=(140, 255))

    # Main function which contains the game loop and all the other functions
    def run_game(self):
        while True:
            # Checking keys using event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Make the bird go up
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE and self.game_condition:
                        self.move = 0
                        self.move -= 7.5

                    if event.key == pygame.K_SPACE and self.game_condition == False:
                        self.game_condition = True
                        self.pole_list.clear()
                        self.player_rect.center = (50, 255)
                        self.move = 0
                        self.score = 0
                # Making pipes at a specified time
                if event.type == self.MAKEPIPE:
                    self.pole_list.extend(self.create_pole())
            # Showing the background of game
            self.screen.blit(self.surface, (0, 0))
            # Making the bird go up on key press
            if self.game_condition:
                self.move += self.downward_force
                self.player_rotate = self.playerRotate()
                self.player_rect.centery += self.move
                # Rotating the bird as it moves
                self.screen.blit(self.player_rotate, self.player_rect)
                # Checking if the bird collides with any objects
                self.game_condition = self.checkCollision()
                # Making the poles move and storing them in list
                self.pole_list = self.movePoles()
                # Making poles
                self.makePoles()
                # Updating score
                self.score += 0.009
                # referencing to playing condition
                self.currentCondition = 'main_game'
                # displaying Score
                self.displayScore()
            # code if the game is over to display start screen and score
            else:
                self.currentCondition = 'game_over'
                self.screen.blit(self.gameOver_surface, self.gameOver_rect)
                if self.score >= self.high_score:
                    self.high_score = self.score
                self.displayScore()
            # Making the floor continously moving
            self.floor_x_position -= 1
            self.draw_floor()
            if self.floor_x_position <= -280:
                self.floor_x_position = 0
            # updating frames
            pygame.display.update()
            self.clock.tick(90)

    def draw_floor(self):
        self.screen.blit(self.floor, (self.floor_x_position, 440))
        self.screen.blit(self.floor, (self.floor_x_position + 280, 440))

    # Creating poles
    def create_pole(self):
        self.random_pipe_pos = random.choice(self.pole_length)
        self.down_pipe = self.pole_surface.get_rect(midtop=(270, self.random_pipe_pos))
        self.upper_pipe = self.pole_surface.get_rect(midbottom=(270, self.random_pipe_pos - 150))
        return self.down_pipe, self.upper_pipe

    # Function to move poles
    def movePoles(self):
        for pipe in self.pole_list:
            pipe.centerx -= 4.5
        return self.pole_list

    # flipping poles to make both upper and bottom poles
    def makePoles(self):
        for pipe in self.pole_list:
            if pipe.bottom >= 510:
                self.screen.blit(self.pole_surface, pipe)
            else:
                self.flip_pipe = pygame.transform.flip(self.pole_surface, False, True)
                self.screen.blit(self.flip_pipe, pipe)

    # checking collision using built-in functions
    def checkCollision(self):
        for pipe in self.pole_list:
            if self.player_rect.colliderect(pipe):
                return False
        if self.player_rect.top < -50 or self.player_rect.bottom >= 500:
            return False

        return True

    def playerRotate(self):
        self.new_player = pygame.transform.rotozoom(self.player, self.move * 3, 1)
        return self.new_player

    # Displaying Score
    def displayScore(self):
        if self.currentCondition == "main_game":
            self.score_surface = self.gameFont.render(str(int(self.score)), True, (255, 255, 255))
            self.score_rect = self.score_surface.get_rect(center=(140, 50))
            self.screen.blit(self.score_surface, self.score_rect)

        if self.currentCondition == "game_over":
            self.score_surface = self.gameFont.render(f'Score: {int(self.score)}', True,
                                                      (255, 255, 255)).convert_alpha()
            self.score_rect = self.score_surface.get_rect(center=(140, 50))
            self.screen.blit(self.score_surface, self.score_rect)

            self.high_score_surface = self.gameFont.render(f'High Score: {int(self.high_score)}', True,
                                                           (255, 255, 255)).convert_alpha()
            self.highscore_rect = self.high_score_surface.get_rect(center=(140, 420))
            self.screen.blit(self.high_score_surface, self.highscore_rect)

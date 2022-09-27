import pygame, sys
import random
import math
from dataclasses import dataclass
from pygame import *


class WhackCheems:
    def __init__(self):
        # Define constants
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.FPS = 60
        self.MOLE_WIDTH = 90
        self.MOLE_HEIGHT = 81
        self.FONT_SIZE = 45
        self.FONT_TOP_MARGIN = 26
        self.LEVEL_SCORE_GAP = 10 #How many score before bump up a level
        self.LEFT_MOUSE_BUTTON = 1
        self.GAME_TITLE = "Whack A Cheems - Assignment 1 - Game Dev"
        
        # Initialize player's score, number of missed hits and level
        self.score = 0
        self.misses = 0
        self.level = 1
        self.time = 30
        # Initialize screen
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption(self.GAME_TITLE)
        self.background = pygame.image.load("images/bg.png")
        
        # Font object for displaying text
        self.font_obj = pygame.font.Font('fonts/Pixelboy.ttf', self.FONT_SIZE)
        
        # Initialize the bat's sprite sheet. bat doesn't work though
        bat_sheet = pygame.image.load("images/bat.png")
        self.bat = []
        self.bat.append(pygame.transform.scale((bat_sheet.subsurface(0, 0, 300, 300)), (100,100)))
        self.bat.append(pygame.transform.scale((bat_sheet.subsurface(300, 0, 300, 300)), (100,100)))
        self.bat.append(pygame.transform.scale((bat_sheet.subsurface(600, 0, 300, 300)), (100,100)))
        
        # Initialize the mole's sprite sheet
        # 6 different states
        sprite_sheet = pygame.image.load("images/mole.png")
        self.mole = []
        self.mole.append(sprite_sheet.subsurface(169, 0, 90, 81))
        self.mole.append(sprite_sheet.subsurface(309, 0, 90, 81))
        self.mole.append(sprite_sheet.subsurface(449, 0, 90, 81))
        self.mole.append(sprite_sheet.subsurface(575, 0, 116, 81))
        self.mole.append(sprite_sheet.subsurface(717, 0, 116, 81))
        self.mole.append(sprite_sheet.subsurface(853, 0, 116, 81))
        
        # Positions of the holes in background
        self.hole_positions = []
        self.hole_positions.append((404, 479))
        self.hole_positions.append((636, 366))
        self.hole_positions.append((658, 232))
        self.hole_positions.append((464, 119))
        self.hole_positions.append((381, 295))
        self.hole_positions.append((119, 366))
        self.hole_positions.append((179, 169))
        self.hole_positions.append((95, 43))
        self.hole_positions.append((603, 11))
        
        # Sound effects
        self.soundEffect = SoundEffect()

    # Calculate the player level according to his current score & the LEVEL_SCORE_GAP constant
    def get_player_level(self):
        newLevel = 1 + int(self.score / self.LEVEL_SCORE_GAP)
        if newLevel != self.level:
            # if player get a new level play this sound
            self.soundEffect.playLevelUp()
        return 1 + int(self.score / self.LEVEL_SCORE_GAP)

    # Get the new duration between the time the mole pop up and down the holes
    # It's in inverse ratio to the player's current level
    def get_interval_by_level(self, initial_interval):
        new_interval = initial_interval - self.level * 0.15
        return new_interval if new_interval > 0 else 0.05

    # Check whether the mouse click hit the mole or not
    def is_mole_hit(self, mouse_position, current_hole_position):
        mouse_x, mouse_y = mouse_position[0:2]
        current_hole_x, current_hole_y = current_hole_position[0:2]
        if (mouse_x > current_hole_x) and (mouse_x < current_hole_x + self.MOLE_WIDTH) and (mouse_y > current_hole_y) and (mouse_y < current_hole_y + self.MOLE_HEIGHT):
            return True
        return False

    # Update the game states, re-calculate the player's score, misses, level
    def update(self):
        # Update the player's level
        current_level_string = "Level: " + str(self.level)
        level_text = self.font_obj.render(current_level_string, True, (255, 255, 255))
        level_text_pos = level_text.get_rect()
        level_text_pos.centerx = self.SCREEN_WIDTH / 8
        level_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(level_text, level_text_pos)
        
        # Update the player's score
        current_score_string = "Score: " + str(self.score)
        score_text = self.font_obj.render(current_score_string, True, (255, 255, 255))
        score_text_pos = score_text.get_rect()
        score_text_pos.centerx = self.SCREEN_WIDTH / 6 * 2 + 20
        score_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(score_text, score_text_pos)
        
        # Update the player's misses
        current_misses_string = "Misses: " + str(self.misses)
        misses_text = self.font_obj.render(current_misses_string, True, (255, 255, 255))
        misses_text_pos = misses_text.get_rect()
        misses_text_pos.centerx = self.SCREEN_WIDTH / 8 * 5
        misses_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(misses_text, misses_text_pos)
        
        # Update the player's misses
        time_string = "Time: " + str(self.time)
        time_text = self.font_obj.render(time_string, True, (255, 255, 255))
        time_text_pos = time_text.get_rect()
        time_text_pos.centerx = self.SCREEN_WIDTH / 8 * 7
        time_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(time_text, time_text_pos)

    def gameover(self):
        global dif
        game_over_back = pygame.Rect(25, 90, 700, 120)
        pygame.draw.rect(self.screen, (47, 143, 194), game_over_back)
        game_over = pygame.font.Font('fonts/Pixelboy.ttf', 150)
        game_over_text = game_over.render('GAME OVER', True, (255, 255, 255))
        self.screen.blit(game_over_text, (125, 100)) 
        #restart button text
        restart_button = pygame.Rect(300, 400, 200, 50)
        pygame.draw.rect(self.screen, (47, 143, 194), restart_button)
        restart_text = self.font_obj.render('Restart', True, (255, 255, 255))
        self.screen.blit(restart_text, (restart_button.x + 10, restart_button.y + 10))  
        #return to menu button text
        menu_button = pygame.Rect(300, 500, 200, 50)
        pygame.draw.rect(self.screen, (47, 143, 194), menu_button)
        menu_text = self.font_obj.render('Menu', True, (255, 255, 255))
        self.screen.blit(menu_text, (menu_button.x + 10, menu_button.y + 10))
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if restart_button.collidepoint(mouse_pos):
                        main()
                    if menu_button.collidepoint(mouse_pos):
                        main_menu()
            pygame.display.update()

        pygame.display.flip()
        
    # Start the game's main loop
    # Contains some logic for handling animations, mole hit events, etc..
    def start(self):
        global dif
        cycle_time = 0
        num = -1
        loop = True
        is_down = False
        interval = 0.1
        initial_interval = 1 if dif == 1 else 0.25
        frame_num = 0
        left = 0
        count = 0
        # Time control variables
        clock = pygame.time.Clock()
        start_ticks=pygame.time.get_ticks() #starter tick

        for i in range(len(self.mole)):
            self.mole[i].set_colorkey((0, 0, 0))
            self.mole[i] = self.mole[i].convert_alpha()

        while loop:
            if self.time <= 0:
                loop = False
                self.gameover()
            
            else:
                mx, my = pygame.mouse.get_pos()        
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        loop = False
                    if event.type == MOUSEBUTTONDOWN and event.button == self.LEFT_MOUSE_BUTTON:
                        self.soundEffect.playFire()
                        if self.is_mole_hit(mouse.get_pos(), self.hole_positions[frame_num]) and num > 0 and left == 0:
                            num = 3
                            left = 14
                            is_down = False
                            interval = 0
                            self.score += 1  # Increase player's score
                            self.level = self.get_player_level()  # Calculate player's level
                            # Stop popping sound effect
                            self.soundEffect.stopPop()
                            # Play hurt sound
                            self.soundEffect.playHurt()
                            self.update()
                        else:
                            self.misses += 1
                            self.update()
                    
                if num > 5:
                    self.screen.blit(self.background, (0, 0))
                    self.update()
                    num = -1
                    left = 0

                if num == -1:
                    self.screen.blit(self.background, (0, 0))
                    self.update()
                    num = 0
                    is_down = False
                    interval = 0.5
                    frame_num = random.randint(0, 8)
                    
                mil = clock.tick(self.FPS)
                sec = mil / 1000.0
                cycle_time += sec
                count = count + mil
                if count >= 1000:
                    if self.time > 0:
                        self.time = self.time - 1
                        count = 0
                    else:
                        self.time = 0
                if cycle_time > interval:
                    pic = self.mole[num]
                    self.screen.blit(self.background, (0, 0))
                    self.screen.blit(pic, (self.hole_positions[frame_num][0] - left, self.hole_positions[frame_num][1]))
                    self.update()
                    if is_down is False:
                        num += 1
                    else:
                        num -= 1
                    if num == 4:
                        interval = 0.3
                    elif num == 3:
                        num -= 1
                        is_down = True
                        self.soundEffect.playPop()
                        interval = self.get_interval_by_level(initial_interval)  # get the newly decreased interval value
                    else:
                        interval = 0.1
                    cycle_time = 0
            # Update the display
            pygame.display.flip()

class SoundEffect:
    def __init__(self):
        self.mainTrack = pygame.mixer.music.load("sounds/theme.mp3")
        self.fireSound = pygame.mixer.Sound("sounds/bonk.mp3")
        self.fireSound.set_volume(1.0)
        self.popSound = pygame.mixer.Sound("sounds/pop.wav")
        self.hurtSound = pygame.mixer.Sound("sounds/oof.mp3")
        self.levelSound = pygame.mixer.Sound("sounds/point.wav")
        pygame.mixer.music.play(-1)

    def playFire(self):
        self.fireSound.play()

    def stopFire(self):
        self.fireSound.sop()

    def playPop(self):
        self.popSound.play()

    def stopPop(self):
        self.popSound.stop()

    def playHurt(self):
        self.hurtSound.play()

    def stopHurt(self):
        self.hurtSound.stop()

    def playLevelUp(self):
        self.levelSound.play()

    def stopLevelUp(self):
        self.levelSound.stop()

#------------------------------------------------------------------------#
def main():
    # Initialize the game
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    pygame.init()
    # Run the main loop
    game = WhackCheems()
    game.start()
    # Exit the game if the main loop ends
    pygame.quit()

def main_menu():
    global dif
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Whack-A-Cheems')
    background = pygame.image.load('images/bg_menu.png')
    background = pygame.transform.scale(background, (800, 600))
    screen.blit(background, (0, 0))
    #Title
    game_title = pygame.font.Font('fonts/Pixelboy.ttf', 90)
    game_title_text = game_title.render('Whack A Cheems', True, (255, 255, 255))
    screen.blit(game_title_text, (145, 100))
    #start button with text
    start_button = pygame.Rect(325, 300, 160, 40)
    pygame.draw.rect(screen, (47, 143, 194), start_button)
    font = pygame.font.Font('fonts/Pixelboy.ttf', 45)
    text = font.render('Start', True, (255, 255, 255))
    screen.blit(text, (375, 310))
    #quit button with text
    quit_button = pygame.Rect(325, 500, 160, 40)
    pygame.draw.rect(screen, (47, 143, 194), quit_button)
    font = pygame.font.Font('fonts/Pixelboy.ttf', 45)
    text = font.render('Quit', True, (255, 255, 255))
    screen.blit(text, (375, 510))
    #options button with text
    options_button = pygame.Rect(325, 400, 160, 40)
    pygame.draw.rect(screen, (47, 143, 194), options_button)
    font = pygame.font.Font('fonts/Pixelboy.ttf', 45)
    text = font.render(("easy" if dif == 1 else "hard"), True, (255, 255, 255))
    screen.blit(text, (375, 410))

    pygame.display.flip()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    main()
                if options_button.collidepoint(event.pos):
                    if dif == 1:
                        dif = 2
                    else:
                        dif = 1
                    pygame.draw.rect(screen, (47, 143, 194), options_button)
                    text = font.render(("easy" if dif == 1 else "hard"), True, (255, 255, 255))
                    screen.blit(text, (375, 410))
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

if __name__ == "__main__":
    global dif
    dif = 1
    main_menu()

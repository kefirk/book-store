import pygame
import random

def make_font(size, font_type = 'freesansbold.ttf'):
    return pygame.font.Font(font_type, size)

class State:
    '''Class to help keep track of the user's progress and to generate a number for the player to guess.'''
    def __init__(self, digit_length = 4, total_guess_number = 100):
        self.digit_length = digit_length
        self.total_guess_number = total_guess_number
        self.guesses_used = 0
        self.real_number=['1', '2', '3', '4']

    def set_real_number(self):
        '''Produces a (self.digit_length) digit long random number with no repeating digits as a list of digits'''
        numberlist =   [0,1,2,3,4,5,6,7,8,9]
        randomnumber = []
        for i in range(self.digit_length):
            randchoice=random.choice(numberlist)
            numberlist.remove(randchoice)
            randomnumber.append(str(randchoice))
        self.real_number = randomnumber

    def hit_blow_checker(self, guess):
        '''checks how good the guess is guess=list() real=list()'''
        hit =  0
        blow = 0
        for index, digit in enumerate(guess):
            if self.real_number.count(digit) == 1:
                if self.real_number[index] == digit:
                    hit += 1
                else:
                    blow += 1
        self.guesses_used += 1
        return self.guesses_used, hit, blow

    def reset_state(self):
        self.guesses_used = 0
        self.set_real_number()


class Button:
    '''Class to create and display buttons'''
    def __init__(self, width, height, pos, colour, text, font, darken = (40, 40, 40), pushed = False):
        self.width = width
        self.height = height
        self.pos = pos
        self.colour = colour
        self.darkened_colour = tuple([(c-d) for c, d in zip(colour, darken)])
        self.darken = darken
        self.text = text
        self.font = font
        self.pushed = pushed
        self.surface = pygame.Surface((width,height))
        self.collisionrect = self.surface.get_rect().move(self.pos)
    
    def text_objects(self):
        '''Method for making the text for a button'''
        textSurface = self.font.render(self.text, True, (0,0,0))
        return textSurface, textSurface.get_rect(center=(int(self.width/2), int(self.height/2)))

    def make_button(self):
        '''Fill button surface with colour and add text'''
        if self.pushed == False:
            self.surface.fill(self.colour)
        else:
            self.surface.fill(self.darken)
        textSurface, textrect = self.text_objects()
        self.surface.blit(textSurface,textrect)

    def place_button(self, screen):
        screen.blit(self.surface, self.pos)

class Number_Button(Button):
    '''Class for allowing the user to input numbers'''
    def __init__(self, width, height, pos, colour, text, darken = (40, 40, 40)):
        super().__init__(width, height, pos, colour, text, make_font(int(height/2)), darken)
        self.num = int(text)

    def button_clicked(self,screen):
        self.pushed = not self.pushed
        self.make_button()
        self.place_button(screen)

class Quit_Button(Button):
    def __init__(self, width, height, pos, colour, darken = (40, 40, 40)):
        super().__init__(width, height, pos, colour, 'Выход ', make_font(int(height/2)), darken)

class Clear_Button(Button):
    '''Class for clearing the current guess from the screen'''
    def __init__(self, width, height, pos, colour, darken = (40, 40, 40)):
        super().__init__(width, height, pos, colour, 'Очистить', make_font(int(height/2)), darken)

class Input_Button(Button):
    def __init__(self, width, height, pos, colour, darken = (40, 40, 40)):
        super().__init__(width, height, pos, colour, 'Ввести', make_font(int(height/2)), darken)




class Board:
    '''Board class for common methods used by the boards of the game'''
    def __init__(self, width, height, pos, colour, font):
        self.width = width
        self.height = height
        self.pos = pos
        self.colour = colour
        self.font = font
        self.surface = pygame.Surface((width,height))

    
    def text_objects(self, text, place_h, place_v):
        '''Method for making the text for a button'''
        textSurface = self.font.render(text, True, (0,0,0))
        return textSurface, textSurface.get_rect(center=(place_h, place_v))
    
    def colour_board(self):
        self.surface.fill(self.colour)
    
    def add_text(self, text, place_h, place_v):
        textSurface, textrect = self.text_objects(text, place_h, place_v)
        self.surface.blit(textSurface, textrect)

    def place_board(self, screen):
        screen.blit(self.surface, self.pos)

class Input_Board(Board):
    '''Board to display the number inputted by the user'''
    def __init__(self, width, height, pos, colour, text = '- - - -'):
        super().__init__(width, height, pos, colour, make_font(int(height/2)))
        self.original_text_list = text.split()
        self.number_list = list(self.original_text_list)
        self.edge_distance = int(self.width/8)
        self.letter_spacing = int(0.2*(self.width - 2*self.edge_distance))
        self.inputted_digits = 0

    def number_display(self,screen):
        for index, digit in enumerate(self.number_list):
            self.add_text(digit, self.edge_distance + (index+1)*self.letter_spacing, int(self.height/2))
        self.place_board(screen)

    def update_number(self, screen, number_text):
        self.inputted_digits += 1
        self.number_list[self.inputted_digits - 1] = number_text
        self.colour_board()
        self.number_display(screen)

    def reset_board(self,screen):
        self.inputted_digits = 0
        self.number_list = list(self.original_text_list)
        self.colour_board()
        self.number_display(screen)




class Score_Board(Board):
    '''Board to display the number of guesses used by the user and to give feedback on the previous guess.'''
    def __init__(self, width, height, pos, colour, text = 'Х: {}  Б: {} К: {}'):
        super().__init__(width, height, pos, colour, make_font(int(height/2)))
        self.letter_text= text
        self.guess_number = 0
        self.hit = 0
        self.blow = 0
    
    def score_display(self,screen):
        self.add_text(self.letter_text.format(str(self.guess_number).zfill(2), str(self.hit), str(self.blow)),
                      int(self.width/2), int(self.height/2))
        self.place_board(screen)
    
    def update_board(self, screen, guess_number, hit , blow):
        self.guess_number = guess_number
        self.hit = hit
        self.blow = blow
        self.colour_board()
        self.score_display(screen)

    def reset_board(self, screen):
        self.guess_number = 0
        self.hit = 0
        self.blow = 0
        self.colour_board()
        self.score_display(screen)
    
    def display_text(self, screen, text, delay):
        self.colour_board()
        self.add_text(text, int(self.width/2), int(self.height/2))
        self.place_board(screen)
        pygame.display.update()
        pygame.time.wait(delay) 
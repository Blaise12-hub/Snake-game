import pygame
from pygame.locals import *
import time
import random   

SIZE = 40
# BACKGROUND_COLOR = (110,110,5)


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    def move(self):
        max_x = (500 // SIZE) - 1  # 11 -> max x = 440
        max_y = (500 // SIZE) - 1  # 11 -> max y = 440
        self.x = random.randint(0, max_x) * SIZE
        self.y = random.randint(0, max_y) * SIZE


class Snake:
    def __init__(self,parent_screen,length):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()    
        
        self.direction = 'down'

        self.length = length
        self.x = [40] * length
        self.y = [40] * length


    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):    
        self.direction = 'down'

    def draw(self):
            self.parent_screen.fill((110,110,5))

            for i in range(self.length):
                self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

    def walk(self):

        for i in range(self.length - 1, 0 , -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]  

        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        self.draw()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


        


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game using pygame library in python")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((500,500))
        self.snake=Snake(self.surface, 1)
        self.snake.draw()
        self.apple=Apple(self.surface)
        self.apple.draw()

    def reset(self):
        self.snake = Snake(self.surface,1)
        self.apple = Apple(self.surface)
    
    def is_collision(self,x1,y1,x2,y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True

        return False
    
    def display_score(self):
            font=pygame.font.SysFont('arial',30)
            score = font.render(f"Score: {self.snake.length}",True,(200,200,200))
            self.surface.blit(score,(350,10))

    #play bg music
    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()

    #function to handle playing sounds/music when crash/collision
    def play_sound(self,sound):
        sound=pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg= pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0,0))
    
    def play(self):
        self.render_background()
        self.snake.walk()
        self.snake.draw()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        #when snake eat apple
        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        #snake eating tiself/colliding with itself
        for i in range(2,self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                self.play_sound("crash")
                raise "Collision occured"

        # Wall collision check inside Game.play()
        if (
            self.snake.x[0] < 0
            or self.snake.x[0] >= 500
            or self.snake.y[0] < 0
            or self.snake.y[0] >= 500
        ):
            self.play_sound("crash")
            raise Exception("Hit wall")
                
    

    def show_game_over(self):
        self.surface.fill((110,110,5))
        font=pygame.font.SysFont('arial',30)
        line1 = font.render(f"Game Over! Your Score is {self.snake.length}",True,(200,200,200))
        self.surface.blit(line1,(100,200))
        line2 = font.render("To play again press Enter. To exit press Escape!",True,(200,200,200))
        self.surface.blit(line2,(100,250))

        pygame.display.flip()

        #have to pause whenver game is over
        pygame.mixer.music.pause()
 
    

    def run(self):
         running = True
         pause = False
        
         while running:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            running = False

                        if event.key == K_RETURN:
                            pygame.mixer.music.unpause() #unpause music 
                            if pause:
                                self.reset()
                                pause = False

                        if not pause:
                            if event.key == K_LEFT:
                                self.snake.move_left()
                            
                            if event.key == K_RIGHT:
                                self.snake.move_right()
                            
                            if event.key == K_UP:
                                self.snake.move_up()
                            if event.key == K_DOWN:
                                self.snake.move_down()
                            
        
                    elif event.type == QUIT:
                         running = False

                try:

                    if not pause:
                     self.play()

                except Exception as e:
                    self.show_game_over()
                    pause = True
                    # self.reset()

                time.sleep(.25)
                



    

if __name__ == "__main__":
    game = Game()
    game.run()

    
    
    # pygame.display.flip()

   




    # time.sleep(5)





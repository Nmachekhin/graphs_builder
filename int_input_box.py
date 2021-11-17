import pygame
import time

class Input_int_box():
    def __init__(self, position:list=[0,0], size:list=[40,10],  text:str="", color:list=[220,220,220], max_input:int=9999):
        self.position=position
        self.id=int(time.time()*1000)
        self.color=color
        self.max_input=max_input
        self.pressed=False
        self.blink=True
        self.delay_time=0.5
        self.text=text
        self.size=size
        self.last_blink_time=0
        self.input=""
        self.input_pos=len(self.input)

    def get_int(self):
        if self.input=="":
            return 0
        return int(self.input)


    def clicked(self, click):
        pressed= (click[0]>=self.position[0] and click[0]<=self.position[0]+self.size[0]) and (click[1]>=self.position[1] and click[1]<=self.position[1]+self.size[1])
        if pressed:
            self.pressed = True
            self.input_pos=len(self.input)
            self.last_blink_time=time.time()
        else:
            self.pressed=False
        return pressed


    def update(self, event):
        if self.pressed:
            if event.type==pygame.KEYDOWN:
                if event.key==13 or event.key==pygame.K_KP_ENTER:
                    self.pressed=False
                if event.key==pygame.K_RIGHT and self.input_pos<len(self.input):
                    self.input_pos+=1
                if event.key==pygame.K_LEFT and self.input_pos>0:
                    self.input_pos-=1
                if str.isdigit(event.unicode):
                    self.input=self.input[:self.input_pos]+event.unicode+self.input[self.input_pos:]
                    self.input_pos+=1
                    self.input=str(int(self.input))
                if event.unicode=="\b" and self.input_pos>0:
                    self.input = self.input[:(self.input_pos-1)]+self.input[self.input_pos:]
                    self.input_pos-=1
                if self.get_int()>self.max_input:
                    self.input=str(self.max_input)
                    self.input_pos=len(self.input)




    def draw(self, screen):
        myfont = pygame.font.SysFont('Arial', 14)
        pygame.draw.rect(screen, (0,0,0), (self.position[0] -1, self.position[1] - 1+ self.size[1]/2,
                                                      self.size[0], self.size[1]/2))
        pygame.draw.rect(screen, self.color, (self.position[0], self.position[1]+ self.size[1]/2,
                                              self.size[0], self.size[1]/2))
        input =self.input
        if self.pressed:
            if time.time()-self.last_blink_time>=self.delay_time:
                self.blink=not self.blink
                self.last_blink_time=time.time()
            if self.blink or self.input_pos!=len(self.input):
                input=input[:self.input_pos]+"|"+input[self.input_pos:]
        if input=="" or input =='|':
            input="0"+input
        textsurface = myfont.render(input, False, (0,0,0))
        text_height = textsurface.get_height()
        mid_y=self.position[1]+self.size[1]*3/4
        screen.blit(textsurface, [self.position[0]+1, mid_y - text_height / 2])
        textsurface = myfont.render(self.text, False, (0, 0, 0))
        screen.blit(textsurface, [self.position[0]+1, self.position[1]])
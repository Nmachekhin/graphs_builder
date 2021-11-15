import pygame
import math

class View_top():
    def __init__(self, data):
        self.total_data=data
        self.id=data["id"]
        self.pos=data["pos"]
        self.num=data["num"]
        self.active=data["active"]
        self.color=(0, 255, 255)
        self.border_color=(0, 0, 0)
        self.active_border_color=(255, 0, 0)
        self.border_radius=2
        self.radius=15


    def set_parameters(self, parameters= [(0, 255, 255), (0, 0, 0), (255, 0, 0), 15, 2]):
        self.color=parameters[0]
        self.border_color=parameters[1]
        self.active_border_color=parameters[2]
        self.radius=parameters[3]
        self.border_radius=parameters[4]


    def is_clicked(self, click):
        dist = math.floor(math.sqrt((self.pos[0] - click[0]) * (self.pos[0] - click[0])
                                    + (self.pos[1] - click[1]) * (self.pos[1] - click[1])))
        if dist <= self.radius+self.border_radius:
            return self.id
        elif dist <= (self.radius+self.border_radius) * 5:
            return "near"
        return None


    def draw(self, screen):
        if self.active:
            pygame.draw.circle(screen, self.active_border_color, self.pos, self.radius+self.border_radius)
        else:
            pygame.draw.circle(screen, self.border_color, self.pos, self.radius+self.border_radius)
        pygame.draw.circle(screen, self.color, self.pos, self.radius)
        myfont = pygame.font.SysFont('Arial', self.radius)
        textsurface = myfont.render(str(self.num), False, (0, 0, 0))
        text_width = textsurface.get_width()
        text_height = textsurface.get_height()
        screen.blit(textsurface,(self.pos[0] - text_width/2,self.pos[1]-text_height/2))


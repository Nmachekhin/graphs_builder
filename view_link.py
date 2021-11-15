from view_top import *
import math
import pygame

class View_link():
    def __init__(self, data):
        self.total_data=data
        self.id=data["id"]
        self.pointing=data["pointing"]
        self.end_id=data["end"]
        self.start_id=data["start"]
        self.has_weight=data["has_weight"]
        self.weight=data["weight"]
        self.color=(0,0,0)
        self.radius=10
        self.wings_len=10


    def get_positions_by_radius(self, position, k_param, b_param, radius): #y=kx_param+b_param,  R^2=(x-x_end)^2+(y-y_end)^2.
        #Розв'язавши, отримаємо квадратне рівняння формату ax^2+bx+c=0
        a=(pow(k_param,2)+1)
        b=(2 * k_param * (b_param - position[1]) - 2 * position[0])
        c= pow(position[0], 2) + pow((b_param - position[1]), 2) - pow(radius, 2)
        x1=(-b+math.sqrt(b*b-4*a*c))/(2*a)
        x2=(-b-math.sqrt(b*b-4*a*c))/(2*a)
        y1=x1*k_param+b_param
        y2=x2*k_param+b_param
        return [[x1,y1], [x2,y2]]




    def get_tops_borders_for_link(self, start:View_top, end:View_top):
        x_start =start.pos[0]
        k=self.get_k(start.pos, end.pos)
        b=self.get_b(start.pos, end.pos)
        y_start=k*x_start+b
        borders=self.get_positions_by_radius(end.pos, k, b, end.radius + end.border_radius)
        dist1=math.sqrt(pow(start.pos[0]-borders[0][0],2)+pow(start.pos[1]-borders[0][1],2))
        dist2=math.sqrt(pow(start.pos[0]-borders[1][0],2)+pow(start.pos[1]-borders[1][1],2))
        if dist1<dist2:
            x_end=borders[0][0]
            y_end=borders[0][1]
        else:
            x_end = borders[1][0]
            y_end = borders[1][1]
        return {"start":[x_start, y_start], "end":[x_end, y_end]}


    def get_text_position(self, start,end):
        angle=self.get_angle(start,end)
        x_pos=(start.pos[0]+end.pos[0])/2
        y_pos=start.pos[1]+(x_pos-start.pos[0])*math.tan(angle)
        return [x_pos,y_pos]

    def set_parameters(self, parameters=[(0,0,0), 10]):
        self.color=parameters[0]
        self.radius=parameters[1]

    def get_arrows_wings(self, start_pos, end_pos):
        k_param=self.get_k(start_pos, end_pos)
        b_param=self.get_b(start_pos, end_pos)
        base_positions=self.get_positions_by_radius(end_pos, k_param, b_param, self.wings_len)
        dist1=math.sqrt(pow(start_pos[0]-base_positions[0][0],2)+pow(start_pos[1]-base_positions[0][1],2))
        dist2=math.sqrt(pow(start_pos[0]-base_positions[1][0],2)+pow(start_pos[1]-base_positions[1][1],2))
        if dist1<dist2:
            base_pos=base_positions[0]
        else:
            base_pos=base_positions[1]
        alt_k_param=-1/k_param
        alt_b_param= (k_param-alt_k_param) * base_pos[0] + b_param
        return self.get_positions_by_radius(base_pos, alt_k_param, alt_b_param, self.wings_len)


    def get_k(self, start_pos, end_pos):
        return (end_pos[1] - start_pos[1])/(end_pos[0] - start_pos[0])

    def get_b(self, start_pos, end_pos):
        return start_pos[1] - start_pos[0] * self.get_k(start_pos, end_pos)

    def get_middle(self, start_pos,end_pos):
        k_param= self.get_k(start_pos, end_pos)
        b_param= self.get_b(start_pos, end_pos)
        perspective_middles=self.get_positions_by_radius(end_pos, k_param, b_param, math.sqrt(pow(start_pos[0]-end_pos[0],2)/4+
                                                                                              pow(start_pos[1]-end_pos[1],2)/4))
        dist1=math.sqrt(pow(start_pos[0]-perspective_middles[0][0],2)+pow(start_pos[1]-perspective_middles[0][1],2))
        dist2=math.sqrt(pow(start_pos[0]-perspective_middles[1][0],2)+pow(start_pos[1]-perspective_middles[1][1],2))
        if dist1<dist2:
            return perspective_middles[0]
        return perspective_middles[1]


    def draw(self, screen, start:View_top, end:View_top):
        tops_borders_points = self.get_tops_borders_for_link(start, end)
        start_point = tops_borders_points["start"]
        end_point = tops_borders_points["end"]
        pygame.draw.line(screen, self.color, start_point, end_point)
        if self.pointing:
            pygame.draw.line(screen, self.color, self.get_arrows_wings(start.pos, end_point)[0], end_point)
            pygame.draw.line(screen, self.color, self.get_arrows_wings(start.pos, end_point)[1], end_point)
        if self.has_weight:
            myfont = pygame.font.SysFont('Arial', 14)
            textsurface = myfont.render(str(self.weight), False, (0, 0, 0))
            middle=self.get_middle(start.pos, end.pos)
            pygame.draw.circle(screen, self.color,middle, max(textsurface.get_width()/2, textsurface.get_height()/2)+3)
            pygame.draw.circle(screen, (255, 255, 255), middle,max(textsurface.get_width()/2, textsurface.get_height()/2)+2)
            screen.blit(textsurface, [middle[0]-textsurface.get_width()/2, middle[1]-textsurface.get_height()/2])
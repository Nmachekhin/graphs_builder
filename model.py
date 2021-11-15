from top import *
from link import *
import time


class Model():
    def __init__(self):
        self.tops={}
        self.links={}
        self.active_top=None


    def delete_state(self):
        self.tops={}
        self.links={}

    def set_loaded_tops(self, data):
        for i in data:
            top=Top()
            top.set_by_converted_data(i)
            self.tops[top.id]=top

    def set_loaded_links(self, data):
        for i in data:
            link=Link()
            link.set_by_converted_data(i, self.tops)
            self.links[link.id]=link


    def new_top(self, pos:list):
        top=Top(int(time.time()*1000), list(pos), len(self.tops.keys())+1)
        self.tops[top.id]=top
        return top

    def activate_top(self, id:int):
        self.tops[id].active=True
        self.active_top=self.tops[id]
        return self.tops[id]

    def deactivate_top(self,id):
        self.tops[id].active=False
        return self.tops[id]

    def tops_link_id(self, start:Top, end:Top):
        for i in self.links.keys():
            if (start.id==self.links[i].start["id"] and end.id==self.links[i].end["id"]) or (end.id==self.links[i].start["id"] and start.id==self.links[i].end["id"]):
                return self.links[i].id
        return None


    def build_link(self, id:int, pointing=False, has_weight=False, weight=0):
        link_id=self.tops_link_id(self.active_top, self.tops[id])
        if self.tops[id]!=self.active_top and link_id==None:
            link=Link(int(time.time()*1000), self.active_top, self.tops[id],pointing, has_weight, weight)
            self.links[link.id]=link
        elif link_id!=None:
            del self.links[link_id]
        self.deactivate_top(self.active_top.id)
        self.active_top=None

    def renumerate_tops(self):
        num=1
        for i in self.tops.keys():
            self.tops[i].number=num
            num+=1

    def delete_top(self, id):
        del self.tops[id]
        self.renumerate_tops()

    def delete_links_near_top(self, top_id):
        del_ids=[]
        for i in self.links.keys():
            link=self.links[i]
            if link.start["id"]==top_id or link.end["id"]==top_id:
                del_ids.append(self.links[i].id)
        for i in del_ids:
            del self.links[i]

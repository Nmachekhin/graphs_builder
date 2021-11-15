from top import *
from view_top import *


class Link():
    def __init__(self, id:int=0, start : Top=None, end:Top=None, pointing:bool =False, has_weight:bool=False, weight:int=0):
        self.id=id
        self.start=None
        self.end=None
        if start!=None and end!=None:
            self.start=start.convert_data()
            self.end=end.convert_data()
        self.pointing=pointing
        self.weight=weight
        self.has_weight=has_weight


    def set_by_converted_data(self,data, tops):
        self.id=data["id"]
        self.start=tops[data["start"]].convert_data()
        self.end=tops[data["end"]].convert_data()
        self.pointing=data["pointing"]
        self.weight=data["weight"]
        self.has_weight=data["has_weight"]


    def convert_data(self):
        return {"start":self.start["id"], "end":self.end["id"], "pointing":self.pointing, "has_weight":self.has_weight,
                "weight":self.weight, "id":self.id}



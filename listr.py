import json,uuid,typing
class Listr:
    def __init__(self, task:str, id:int=0,completed=False,parent:int = 0):
        self.id = id
        self.task = task
        self.completed = completed
        self.parent = parent
    def __str__(self):
        return f"{self.task} {'✅' if self.completed else ''}"
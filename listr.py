import json
class Listr:
    def __init__(self, task, completed=False,children = []):
        self.task = task
        self.completed = completed
        self.children = children
    def __str__(self):
        return f"{self.task} {'✅' if self.completed else ''}"
    def complete(self):
        self.completed = True
        for child in self.children:
            child.complete()
        return self
    def listr_str(self):
        ret_str = f'{self}\n'
        for child in self.children:
            ret_str += f'    {child.listr_str()}'
        return ret_str
    def add_child(self,new_child):
        if not isinstance(new_child,Listr):
            raise TypeError("New child is not of type(Listr)")
        new_child_list = self.children + [new_child]
        return Listr(self.task,self.completed,new_child_list)
    def add_children(self,new_children):
        ret_listr = Listr(self.task,self.completed,self.children)
        for child in new_children:
                ret_listr = ret_listr.add_child(child)
        return ret_listr
    def to_dict(self):
        children = []
        for child in self.children:
            children.append(child.to_dict())
        return {
            "task":self.task,
            "completed":self.completed,
            "children":children
        }
if __name__ == "__main__":
     children = [
        Listr('create list type',True),
        Listr('json functionality'),
        Listr('front end')
     ]
     root_listr = Listr('Make Listr')
     root_listr = root_listr.add_children(children)
     root_dict = root_listr.to_dict()
     print(json.dumps(root_dict))

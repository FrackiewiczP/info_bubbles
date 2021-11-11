
class IdGenerator:
    id =0
    def get():
        IdGenerator.id +=1
        return IdGenerator.id

class Information:
    idGenerator = 1

    def __init__(self,position: list):
        self.id = IdGenerator.get()
        self.position = position

    def getPosition(self,axis:int):
        return self.position[axis]

    def __eq__(self, other):
        if self.id == other.id:
            return True
        return False

    def __str__(self):
        return "{Information id:" + self.id +"position: "+self.position+"}"
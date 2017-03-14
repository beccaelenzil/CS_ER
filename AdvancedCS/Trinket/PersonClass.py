class Person():
    def __init__(self):
        self.name = ""

    def __repr__(self):
        s = "My name is "+self.name+"."
        return s

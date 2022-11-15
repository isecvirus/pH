import random

class Randomize:
    def __init__(self, chars:str="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
        self.chars = chars
    def id(self, length:int=5):
        return ''.join([random.choice(self.chars) for i in range(length)])
randomize = Randomize()
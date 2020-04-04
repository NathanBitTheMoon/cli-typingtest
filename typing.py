import random

class Words:
    def __init__(self, fp):
        self.words = fp.readlines()
        self.range = (0, len(self.words))
    
    def set_range(self, x, y):
        self.range = (x, y)
    
    def next(self, shortest = 2):
        word = ' '
        while len(word) < shortest:
            word = self.words[random.randint(self.range[0], self.range[1])]
        return word.strip()
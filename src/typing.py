import random, string

class Words:
    def __init__(self, fp, split_char = ' ', remove_punctuation = True):
        self.words = fp.read()

        # Remove all punctuation
        if remove_punctuation:
            remove_string = string.punctuation + '’'
            for i in remove_string:
                self.words = self.words.replace(i, '')
            
        # Make string lowercase
        self.words = self.words.lower()

        if '\n' in self.words:
            # Split at new line and at space
            check_list = []
            replace_list = False
            for i in self.words.split('\n'):
                if ' ' in i:
                    replace_list = True
                    check_list.extend(i.split(' '))
            
            if replace_list:
                self.words = check_list
            else:
                self.words = self.words.split('\n')
        else:
            # Split only at space
            self.words = self.words.split(' ')
        
        # Remove all empty chars
        replace_list = []
        for i in self.words:
            if len(i.strip()) != 0:
                replace_list.append(i)
        self.words = replace_list
        
        self.range = (0, len(self.words))
        self.cursor = 0
        self.is_random = False
    
    def set_range(self, x, y):
        if y - 1 < len(self.words):
            self.range = (x, y)
        else:
            self.range = (x, len(self.words))
    
    def random(self):
        random_list = self.words[self.range[0]:self.range[1]]
        output_list = []

        self.is_random = True

        for i in range(self.range[0], self.range[1]):
            item = random.choice(random_list)
            random_list.remove(item)
            output_list.append(item)
        
        self.words = output_list
    
    def next(self, shortest = 2):
        if not self.is_random:
            word = self.words[self.cursor]
            self.cursor += 1
        else:
            word = random.choice(self.words[self.range[0]:self.range[1]])
            while len(word) < shortest:
                word = random.choice(self.words[self.range[0]:self.range[1]])
            return word
        return word.strip()
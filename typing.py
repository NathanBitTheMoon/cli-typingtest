import random, string

class Words:
    def __init__(self, fp, split_char = ' ', remove_punctuation = True):
        self.words = fp.read().split(split_char)
        self.words = [e.strip().lower().replace('\n', '') for e in self.words if e.strip() != '' and e != "\n"]
        if remove_punctuation:
            replace_list = []
            for i in self.words:
                st = i
                for e in string.punctuation + '’':
                    st = st.replace(e, '')
                replace_list.append(st)
            self.words = replace_list
        
        self.range = (0, len(self.words))
        self.cursor = 0
    
    def set_range(self, x, y):
        if y - 1 < len(self.words):
            self.range = (x, y)
        else:
            self.range = (x, len(self.words))
    
    def random(self):
        random_list = self.words[self.range[0]:self.range[1]]
        output_list = []

        for i in range(self.range[0], self.range[1]):
            item = random.choice(random_list)
            random_list.remove(item)
            output_list.append(item)
        
        self.words = output_list
    
    def next(self, shortest = 2):
        word = self.words[self.cursor]
        self.cursor += 1
        # first = True
        # while len(word) <= shortest and not first:
        #     word = self.words[self.cursor]
        #     self.cursor += 1
        #     first = False
        return word.strip()
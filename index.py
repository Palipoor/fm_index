class FMIndex():
    def __init__(self, text):
        self.text = text
        self.rank_array = {'a': [], 'b': [], '$': [0] * len(text)}
        self.c_array = {'$': 0, 'a': 1,'b': text.count('a') + 1} 
        self._build_suffix_array()


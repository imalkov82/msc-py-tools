__author__ = 'imalkov'

class PecubeEnv:
    def __init__(self):
        self.env = {}

    def insert(self, k, v):
        try:
            self.env[k] = v
        except KeyError:
            self.env[k] = v

    def extract(self, k):
        try:
            return self.env[k]
        except KeyError:
            return None
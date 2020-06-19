class Ant:
    def __init__(self, r, c, d):
        self.r = r
        self.c = c
        self.d = d
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
        
    def __str__(self):
        return str((self.r, self.c, self.d))
        
    def move_forward(self, yaxis, xaxis, wrap):
        if self.d == 0:
            self.r = (self.r - 1) % yaxis if wrap else (self.r - 1)
        elif self.d == 1:
            self.c = (self.c + 1) % xaxis if wrap else (self.c + 1)
        elif self.d == 2:
            self.r = (self.r + 1) % yaxis if wrap else (self.r + 1)
        elif self.d == 3:
            self.c = (self.c - 1) % xaxis if wrap else (self.c - 1)
        return self
        
    def next_state(self, state, wrap):
        yaxis, xaxis = len(state), len(state[0])
        try:
            if state[self.r][self.c]:
                self.d = (self.d + 1) % 4
                state[self.r][self.c] = 0
            else:
                self.d = (self.d - 1) % 4
                state[self.r][self.c] = 1
        except IndexError:
            pass
        self = self.move_forward(yaxis, xaxis, wrap)
        return self, state
'''
Created on Apr 8, 2011

@organization: cert.org
'''



class Range(object):
    def __init__(self, low, high):
        self.id = id(self)
        self.min = float(low)
        self.max = float(high)
        self.mean = (self.min + self.max) / 2.0
        self.span = self.max - self.min

    def __repr__(self):
        return '%0.6f-%0.6f' % (self.min, self.max)

#    def __setstate__(self, state):
#        self.__dict__.update(state)

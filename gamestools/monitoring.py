import time
class Monitor:

    def append(self, name):
        if not hasattr(self, name):
            setattr(self, name, [time.clock()])
        else:
            getattr(self,name).append(time.clock())

    def show(self, letters=None):
        if not letters:
            letters = []
            for letter in "abcdefghijklmnopqrstuvwxyz":
                if hasattr(self,letter):
                    letters.append(letter)
        tot = [0.]*len(letters)
        L = len(getattr(self,letters[0]))
        for i in range(1,len(letters)):
            for k in range(L):
                diff = getattr(self,letters[i])[k] - getattr(self,letters[i-1])[k]
                tot[i] += diff
        for i in range(1,len(tot)):
            print(letters[i-1]+"->"+letters[i]+": "+str(tot[i]))
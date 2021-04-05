import time
class Monitor:

    def append(self, name):
        if not hasattr(self, name):
            setattr(self, name, [time.perf_counter()])
        else:
            getattr(self,name).append(time.perf_counter())

    def show(self, letters=None, rnd=None):
        if not letters:
            letters = []
            for letter in "abcdefghijklmnopqrstuvwxyz":
                if hasattr(self,letter):
                    letters.append(letter)
        n_lett = len(letters)
        tot = [0.]*n_lett
        L = len(getattr(self,letters[0]))
        print("Stats on", L, "iterations:")
        for i in range(1,n_lett):
            for k in range(L): #k is the iteration
                diff = getattr(self,letters[i])[k] - getattr(self,letters[i-1])[k]
                tot[i] += diff
        for k in range(1,L): #z->a_previous_iteration
            diff = getattr(self,letters[0])[k] - getattr(self,letters[n_lett-1])[k-1]
            tot[0] += diff
        for i in list(range(1,len(tot)))+[0]: #we want z->a displayed at the end
            if rnd is None:
                n = tot[i]
            else:
                n = round(tot[i], rnd)
            p = round(100*n/sum(tot))
            print(letters[i-1]+"->"+letters[i]+": "+str(n)+" ("+str(p)+"%)")
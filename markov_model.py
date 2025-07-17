from symboltable import SymbolTable
import stdio
import stdrandom

class MarkovModel(object):
    # Creates a Markov model of order k from the given text.
    def __init__(self, text, k):
        self._k = k
        self._st = {}
        circtext = text
        kgram = ""
        amount = 0
        for j in range(0,k):
            circtext += text[j]
        for i in range(0,len(text)):
            st2 = {}
            kgram = ""
            for l in range(i,i+k):
                kgram += circtext[l]
            if kgram not in self._st:
                st2[circtext[i+k]] = 1
                self._st[kgram] = st2
            else:
                if circtext[i+k] in self._st[kgram]:
                    st2 = self._st[kgram]
                    st2[circtext[i+k]] += 1
                else:
                    st2 = self._st[kgram]
                    st2[circtext[i+k]] = 1
                self._st[kgram] = st2
            amount += 1

        

    # Returns the order this Markov model.
    def order(self):
        return self._k

    # Returns the number of occurrences of kgram in this Markov model; and 0 if kgram is nonexistent. Raises an error 
    # if kgram is not of length k.
    def kgram_freq(self, kgram):
        amount = 0
        if kgram not in self._st:
            return 0
        for c in self._st[kgram]:
            amount += self._st[kgram][c]
        return amount

    
    # Returns number of times character c follows kgram in this Markov model; and 0 if kgram is nonexistent or if it 
    # is not followed by c. Raises an error if kgram is not of length k.
    def char_freq(self, kgram, c):
        if kgram not in self._st:
            return 0
        elif c not in self._st[kgram]:
            return 0
        return self._st[kgram][c]

    # Returns a random character following kgram in this Markov model. Raises an error if kgram is not of length k or 
    # if kgram is nonexistent.
    def rand(self, kgram):
        if kgram not in self._st:
            raise KeyError("The kgram does not exist.")

        keys = list(self._st[kgram].keys())
        probs = list(self._st[kgram].values())
        index = stdrandom.discrete(probs)
        return keys[index]

    # Generates and returns a string of length n from this Markov model, the first k characters of which is kgram.
    def gen(self, kgram, n):
        text = kgram
        for i in range(0,n - self._k):
            text += self.rand(kgram)
        text += kgram
        return text

    # Replaces unknown characters (~) in corrupted with most probable characters from this Markov model, and returns 
    # that string.
    def replace_unknown(self, corrupted):
        original = ""
        kgram_before = ""
        for i in range(0,len(corrupted)):
            if corrupted[i] == "~":   
                kgram_after = ""
                for j in range(i+1,len(corrupted)):
                    if corrupted[j] == "~":
                        break
                    else:
                        kgram_after += corrupted[j]
                probs = []
                keys = []
                while len(kgram_before) > self._k:
                    kgram_before = kgram_before[1:]
                while len(kgram_after) > self._k:
                    kgram_after = kgram_after[:-1]
                if kgram_before in self._st:
                    for key in self._st[kgram_before]:
                        keys += [key]
                for hypothesis in self._st[kgram_before]:
                    context = kgram_before + hypothesis + kgram_after
                    p = 1.0
                    for k in range(0,self._k+1):
                        kgram = ""
                        for m in range(k,self._k+k):
                            kgram += context[m]
                        char = context[self._k+k]
                        if kgram not in self._st or char not in self._st[kgram]:
                            p = 0
                            break
                        else:
                            p = p * self._st[kgram][char]
                    probs += [p]
                original += keys[_argmax(probs)]
                kgram_before = ""
            else:
                kgram_before += corrupted[i]
                original += corrupted[i]
        return original

# Given a list a, _argmax returns the index of the maximum value in a.
def _argmax(a):
    return a.index(max(a))

# Unit tests the data type [DO NOT EDIT].
def _main():
    model = MarkovModel("gagggagaggcgagaaa", 2)
    stdio.writeln("model       = MarkoveModel(\"gagggagaggcgagaaa\", k = 2)")
    stdio.writef("freq(ag)    = %d\n", model.kgram_freq("ag"))
    stdio.writef("freq(cg)    = %d\n", model.kgram_freq("cg"))
    stdio.writef("freq(gc)    = %d\n", model.kgram_freq("gc"))
    stdio.writef("freq(xx)    = %d\n", model.kgram_freq("xx"))
    stdio.writef("freq(aa, a) = %d\n", model.char_freq("aa", "a"))
    stdio.writef("freq(ga, g) = %d\n", model.char_freq("ga", "g"))
    stdio.writef("freq(gg, c) = %d\n", model.char_freq("gg", "c"))
    stdio.writef("freq(xx, x) = %d\n", model.char_freq("xx", "x"))
    stdio.writef("freq(gg, x) = %d\n", model.char_freq("gg", "x"))

if __name__ == "__main__":
    _main()

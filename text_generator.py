from markov_model import MarkovModel
import stdio
import sys

# Entry point.
def main():
    k = int(sys.argv[1])
    n = int(sys.argv[2])
    l = 0
    read = sys.stdin.read()
    model = MarkovModel(read,k)
    kgram = ""
    for j in range(0,k):
        kgram += read[j]
    result = kgram
    for i in range(n - k):
        kgram = result[-k:]
        next_char = model.rand(kgram)
        result += next_char
        if l != len(read)-k:
            l += 1
        else:
            l = 0
    stdio.writeln(result)


if __name__ == "__main__":
    main()

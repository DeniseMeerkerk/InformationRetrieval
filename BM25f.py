import numpy as np
import pandas as pd
import string
import time
## Definitions

# Update word frequencies with the next word.
def update_freq(word, Words, weight=1):
    output = Words
    found = False
    for x in Words:
        if x[0] == word:
            x[1] = x[1] + weight
            found = True
            break
    if not found:
        output = output.append([word, weight])
    return output

# Generate a word frequency list of a section, as well as the total number of words
def frequency(s):
    text = s.translate(str.maketrans("","",string.punctuation)).lower()
    text = text.split(" ")
    Frequencies = []
    N = 0
    for x in text:
        if not x == "":
            update_freq(x,Frequencies,1)
            N = N+1
    if N > 0:
        for i in range(0,len(Frequencies)):
            Frequencies[i][1] = Frequencies[i][1]
    return Frequencies, N

# Generate the weighted word frequencies of all sections.
def combine_frequencies(F1,F2,F3, weights=[1,1,1]):
    Frequencies = []
    N = F1[1]*weights[0] + F2[1]*weights[1] + F3[1]*weights[2]
    for x in F1[0]:
        update_freq(x[0],Frequencies,x[1]*weights[0])
    for x in F2[0]:
        update_freq(x[0],Frequencies,x[1]*weights[1])
    for x in F3[0]:
        update_freq(x[0],Frequencies,x[1]*weights[2])
    return Frequencies, N

# Look up the frequency of a word in a document
def lookup_frequency(word,Frequencies):
    s = 0
    for f in Frequencies:
        if word in f[0]:
            s = s + f[1]
    return s

# Convert the recipe database into a list of bags of words
def bag(Data, weights=[1,1,1]):
    output = Data[:,[0,1,2,3]]
    for i in range(len(Data)):
        F1 = frequency(Data[i][1])
        F2 = frequency(Data[i][2])
        F3 = frequency(Data[i][3])
        output[i,[2,3]] = combine_frequencies(F1,F2,F3, weights)
    return output

# Calculate the inverse document frequency for a query word. The IDF is minimized at 0, so no terms van have negative weight.
def IDF(word,Data):
    N = len(Data)
    n = 0.0
    for i in range(N):
        S = Data[i][2]
        for x in S:
            if word in x[0]:
                n = n+1
                break
    return max(0,np.log(0.5+N-n)-np.log(0.5+n))

# Return the section weights of the used algorithm.
def section_weights(Algorithm):
    if Algorithm == "a1":
        return [1,1,1]
    if Algorithm == "a2":
        return [1,1,1]
    return ""

# Calculate the weighted average length of the articles in a database.
def avg_length(Data):
    L = np.zeros(len(Data))
    for i in range(len(Data)):
        L[i] = Data[i][3]
    return np.mean(L)

# Match a query against an article.
def match(Q, article, Data, avglen, weights=[1,1,1], b=0.75, k=1.2):
    l = article[3]
    s = 0
    x = k*(1.0+b*(l/avglen))
    for q in Q:
        idf = q[1]
        f = lookup_frequency(q[0],article[2])
        s = s + idf*f/(f+x)
    return s*(k+1)

# Match a query against the database and return the top N articles.
def BM25f(query, Data, weights=[1,1,1], b=0.75, k=1.2, N=10):
    start = time.time()
    avglen = avg_length(Data)
    Q = frequency(query)[0]
    for q in Q:
        q[1] = IDF(q[0],Data) #Calculate IDF only once for each query term
    s = np.zeros(len(Data))
    for i in range(len(Data)):
        s[i] = match(Q,Data[i],Data,avglen,weights,b,k)
    n = min(N,len(Data))
    top_indices = np.argsort(-s)[:n]
    output = []
    for x in top_indices:
        recept = Recipe(Data[x][1],Data[x][0])
        if s[x] > 0:
            output.append([recept,x])
    end = time.time()
    print("runtime = ", end-start)
    return output

# Output class
class Recipe:
    def __init__(self,title,link):
        self.title = title
        self.link = link
from wagner_fischer import damerau_levenshtein as distance
import collections
import re


def partition(l):
    '''
    Takes an iterable of 2-tuples and returns a dict constructed with the 
    second element of each tuple as the key and the corresponding 1st elements
    being part of the value.
    e.g., if [(2, 3), (4, 3), (5, 6), (9, 10)] is passed, the return value is
    {3: [2, 4], 6: [5], 10: [9]}
    '''
    ret = collections.defaultdict(lambda: [])
    for a, b in l:
        ret[b].append(a)
    return ret


def get_ngrams(s, n=3):
    if len(s) <= n:
        return [s]
    return [s[i:i+n] for i in xrange(len(s) - n + 1)]


class Corrector(object):
    '''
    The Corrector class. Implements a basic spelling suggestor/corrector based
    n-grams partitioning and the Damerau-Levenshtein distance metric.
    Using: 
        c = Corrector()
        c.train('/path/to/document1', '/path/to/document2',...) # takes a while
        c.suggest('someword') -> ['a', 'list', 

    '''
    
    PUNCTUATIONS = """.,;"""

    def __init__(self):
        self.model = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))

    def train(self, *corpus):
        '''
        train(path1, [path2,[...]])
        Takes one or more paths to training text files and trains the corrector
        accordingly. A good corpus is vital for reasonable accuracy.
        '''
        model = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))
        for document in corpus:
            with open(document) as fp:
                for line in fp:
                    words = line.split()
                    for w in words:
                        word = w.strip(self.PUNCTUATIONS).lower()
                        if not word:
                            continue
                        ngrams = get_ngrams(word)
                        for ngram in ngrams:
                            model[ngram][word] += 1
        self.model = model

    def suggest(self, query, min_suggestions=None):
        '''
        get_suggestions(query, min_suggestions=None)
        Takes the query word, which possibly has mistakes in it and returns
        a list of the closest suggestions.
        If min_suggestions is given, it is the minimum number of suggestions 
        expected. If so many suggestions can not be found, fewer than
        min_suggestions suggestions may be returned.
        '''
        # TODO make the querying here and the training case insensitive.
        word = query.strip(self.PUNCTUATIONS).lower()
        if not word:
            return []

        ngrams = get_ngrams(word)
        words = collections.defaultdict(lambda: 0)
        for ngram in ngrams:
            for k, v in self.model[ngram].iteritems():
                words[k] += v
        words_distances = [((w, c), distance(w, word)) for w, c in words.iteritems()]
        words_distances = sorted(words_distances, key=lambda x: x[1])
        limited = partition(words_distances)
        if min_suggestions is None:
            if words_distances:
                return limited[words_distances[0][1]]
            return []
        ret = []
        for key in sorted(limited.keys()):
            ret.extend(limited[key])
            if len(ret) >= min_suggestions:
                break
        return ret

    def correct(self, query, min_suggestions=None):
        '''
        correct(query) -> suggestion
        Takes a query word and returns a suggested "correct" spelling. Depends on
        the corpus used during training.
        Actually, all correct() does is call get_suggestions() and return the 
        suggestion that has the highest frequency in the corpus.
        '''
        suggestions = self.suggest(query, min_suggestions)
        return sorted(suggestions, key=lambda x: x[1])[-1][0]






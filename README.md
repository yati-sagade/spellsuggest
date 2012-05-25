A simple spelling suggestion/correction module.
===============================================


Example usage:
--------------

    >>> import spellsuggest
    >>> c = spellsuggest.Corrector()
    >>> c.train('./big.txt') # takes a while; can pass in more than one path.
    >>> c.suggest('farke')
    [('farce', 1), ('fare', 7)]
    >>> c.suggest('ak')
    [('ak', 3)]
    >>> c.suggest('ake')
    [('lake', 27), ('jake', 1), ('rake', 4), ('bake', 2), ('sake', 69), ('cake', 5), ('make', 494), ('take', 590), ('wake', 27)]
    >>> c.suggest('lys')
    [('lysol', 1)]
    >>> c.suggest('lys', 3)
    [('lysol', 1), ('ulysses', 3), ('analyse', 1), ('analyst', 1)]
    >>> c.correct('sug')
    'sugar'
    >>> c.correct('sug', 10)
    'suggested'

Uses the n-grams partitioning method to index training text. Faaar from 
anything near perfect. I'm improv[is]ing on it. Obviously, result quality 
varies directly as corpus text quality.





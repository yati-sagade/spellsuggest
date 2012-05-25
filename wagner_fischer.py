def levenshtein(s1, s2):
    '''
    Implementation of the Wagner-Fischer algorithm to calculate the Levenshtein
    distance between two strings.
    Levenshtein distance between two strings is defined as the minimum number
    of operations needed to transform one string to the other. Here, an operation
    can be one of insertion of a character, deletion of a character or 
    substitution of a character by another.

    levenshtein('cat', 'car') -> 1
    levenshtein('ping', 'ping') -> 0
    levenshtein('sitting', 'kitten') -> 3

    TODO: since only two rows are required for each step(the current row and the 
    previous row), space can be cut down to O(min(m, n)) from O(m*n) as it is now.
    '''
    m, n = len(s1), len(s2)
    if not m:
        return n
    if not n:
        return m
    matrix = {}
    for i in xrange(m+1):
        matrix[i, 0] = i
    for j in xrange(1, n+1):
        matrix[0, j] = j
    for i in xrange(1, m+1):
        for j in xrange(1, n+1):
            if s1[i-1] == s2[j-1]:
                # use the top-left cell's value as the current value.
                matrix[i, j] = matrix[i-1, j-1]
            else:
                # use the minimum of top, left and top-left cell values.
                matrix[i, j] = min(matrix[i-1, j], 
                                    matrix[i, j-1],
                                    matrix[i-1, j-1]) + 1
    return matrix[m, n]


def damerau_levenshtein(s1, s2):
    '''
    Implementation of the Wagner-Fischer algorithm to calculate the 
    Damerau-Levenshtein distance between two strings.
    Damerau-Levenshtein distance between two strings is defined as the minimum 
    number of operations needed to transform one string to the other. Here, an 
    operation can be one of insertion of a character, deletion of a character,  
    substitution of a character by another or transposition of two adjacent 
    characters.

    levenshtein('cat', 'car') -> 1
    levenshtein('ping', 'ping') -> 0
    levenshtein('sitting', 'kitten') -> 3

    TODO: since only two rows are required for each step(the current row and the 
    previous row), space can be cut down to O(min(m, n)) from O(m*n) as it is now.
    '''
    m, n = len(s1), len(s2)
    if not m:
        return n
    if not n:
        return m
    matrix = {}
    for i in xrange(m+1):
        matrix[i, 0] = i
    for j in xrange(1, n+1):
        matrix[0, j] = j
    for i in xrange(1, m+1):
        for j in xrange(1, n+1):
            if s1[i-1] == s2[j-1]:
                # use the top-left cell's value as the current value.
                matrix[i, j] = matrix[i-1, j-1]
                cost = 0
            else:
                # use the minimum of top, left and top-left cell values.
                matrix[i, j] = min(matrix[i-1, j], 
                                    matrix[i, j-1],
                                    matrix[i-1, j-1]) + 1
                cost = 1
            if i > 1 and j > 1 and s1[i-1] == s2[j-2] and s1[i-2] == s2[j-1]:
                matrix[i, j] = min(matrix[i, j], matrix[i-2, j-2] + cost)
    return matrix[m, n]



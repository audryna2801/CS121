"""
CS121: Analyzing Election Tweets (Solutions)

Rhedintza Audryna

Algorithms for efficiently counting and sorting distinct `entities`,
or unique values, are widely used in data analysis.

Functions to implement:

- count_tokens
- find_top_k
- find_min_count
- find_most_salient

You may add helper functions.
"""

import math
from util import sort_count_pairs


def count_tokens(tokens):
    '''
    Counts each distinct token (entity) in a list of tokens

    Inputs:
        tokens: list of tokens (must be immutable)

    Returns: dictionary that maps tokens to counts
    '''

    token_dict = {}

    for values in tokens:
        token_dict[values] = token_dict.get(values, 0) + 1

    return token_dict


def find_top_k(tokens, k):
    '''
    Find the k most frequently occuring tokens

    Inputs:
        tokens: list of tokens (must be immutable)
        k: a non-negative integer

    Returns: list of the top k tokens ordered by count.
    '''

    # Error checking (DO NOT MODIFY)
    if k < 0:
        raise ValueError("In find_top_k, k must be a non-negative integer")

    token_dict = count_tokens(tokens)
    sorted_lst = sort_count_pairs(token_dict.items())
    top_k_tokens = [token for token, count in sorted_lst[:k]]

    return top_k_tokens


def find_min_count(tokens, min_count):
    '''
    Find the tokens that occur *at least* min_count times

    Inputs:
        tokens: a list of tokens  (must be immutable)
        min_count: a non-negative integer

    Returns: set of tokens
    '''

    # Error checking (DO NOT MODIFY)
    if min_count < 0:
        raise ValueError("min_count must be a non-negative integer")

    token_dict = count_tokens(tokens)
    token_lst = [token for token, count in token_dict.items()
                 if count >= min_count]

    return set(token_lst)


def augmented_freq(doc):
    '''
    Compute the augmented term frequency values of the tokens in a document

    Inputs: 
        doc: a list of tokens

    Returns: dictionary that maps terms to their augmented frequency
    '''

    # Checking if doc is an empty list
    if not doc:
        return {}

    token_dict = count_tokens(doc)
    tf_dict = {}
    max_count = max(token_dict.values())

    for token, count in token_dict.items():
        tf_dict[token] = 0.5 + 0.5 * (count / max_count)

    return tf_dict


def inv_doc_freq(docs):
    '''
    Compute the inverse document frequency of the tokens in a document collection

    Inputs: 
        docs: a list of list of tokens

    Returns: dictionary that maps terms to their idf
    '''

    idf_dict = {}
    num_of_docs = len(docs)

    # Create a set of all tokens in docs
    docs_set = [set(doc) for doc in docs]
    tokens = set.union(*docs_set)

    for token in tokens:
        docs_with_token = sum([1 for doc in docs_set if (token in doc)])
        idf_dict[token] = math.log(num_of_docs / docs_with_token)

    return idf_dict


def find_salient(docs, threshold):
    '''
    Compute the salient words for each document.  A word is salient if
    its tf-idf score is strictly above a given threshold.

    Inputs:
      docs: list of list of tokens
      threshold: float

    Returns: list of sets of salient words
    '''

    idf_dict = inv_doc_freq(docs)
    salient_lst = []

    for doc in docs:
        tf_dict = augmented_freq(doc)
        salient_in_doc = set()
        for token in tf_dict:
            if tf_dict[token] * idf_dict[token] > threshold:
                salient_in_doc.add(token)
        salient_lst.append(salient_in_doc)

    return salient_lst

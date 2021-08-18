"""
Analyze module

Rhedintza Audryna

"""

import unicodedata
import sys

from basic_algorithms import find_top_k, find_min_count, find_salient


##################### DO NOT MODIFY THIS CODE #####################

def keep_chr(ch):
    '''
    Find all characters that are classifed as punctuation in Unicode
    (except #, @, &) and combine them into a single string.
    '''
    return unicodedata.category(ch).startswith('P') and \
        (ch not in ("#", "@", "&"))


PUNCTUATION = " ".join([chr(i) for i in range(sys.maxunicode)
                        if keep_chr(chr(i))])

# When processing tweets, ignore these words
STOP_WORDS = ["a", "an", "the", "this", "that", "of", "for", "or",
              "and", "on", "to", "be", "if", "we", "you", "in", "is",
              "at", "it", "rt", "mt", "with"]

# When processing tweets, words w/ a prefix that appears in this list
# should be ignored.
STOP_PREFIXES = ("@", "#", "http", "&amp")


#####################  MODIFY THIS CODE #####################

############## Part 2 ##############


def make_list_of_entities(tweets, entity_desc):
    '''
    Generates a list of entities of the chosen type

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc

    Returns: list of entities
    '''

    (key, subkey, case_sensitive) = entity_desc
    list_of_entities = []

    for tweet in tweets:
        key_lst = tweet["entities"][key]
        for dict in key_lst:
            if case_sensitive:
                list_of_entities.append(dict[subkey])
            else:
                list_of_entities.append(dict[subkey].lower())

    return list_of_entities


# Task 2.1
def find_top_k_entities(tweets, entity_desc, k):
    '''
    Find the k most frequently occuring entitites

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc
        k: integer

    Returns: list of entities
    '''

    list_of_entities = make_list_of_entities(tweets, entity_desc)
    top_k_entities = find_top_k(list_of_entities, k)

    return top_k_entities


# Task 2.2
def find_min_count_entities(tweets, entity_desc, min_count):
    '''
    Find the entitites that occur at least min_count times

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc
        min_count: integer

    Returns: set of entities
    '''

    list_of_entities = make_list_of_entities(tweets, entity_desc)
    entity_set = find_min_count(list_of_entities, min_count)

    return entity_set


############## Part 3 ##############


def pre_processing(tweet, case_sensitive, remove_stop):
    '''
    Converts an abridged text of a tweet into a list of strings

    Inputs:
        tweet: a dictionary of a single tweet
        case_sensitive (boolean): True if case needs to be preserved
        remove_stop (boolean): True if stop words need to be removed

    Returns: list of strings
    '''

    text = tweet["abridged_text"].split()
    new_text = []

    for word in text:
        word = word.strip(PUNCTUATION)
        if not case_sensitive:
            word = word.lower()
        if remove_stop and (word in STOP_WORDS):
            word = ""
        if word.startswith(STOP_PREFIXES):
            word = ""
        if word:
            new_text.append(word)

    return new_text


def make_ngrams(tweet, case_sensitive, remove_stop, n):
    '''
    Takes a tweet and create n-grams

    Input: 
        tweet: a dictionary of a single tweet
        case_sensitive (boolean): True if case needs to be preserved
        remove_stop (boolean): True if stop words need to be removed
        n: the length of the tuple of strings

    Returns: a list of tuples of strings
    '''

    text = pre_processing(tweet, case_sensitive, remove_stop)
    ngrams = [tuple(text[i:i+n]) for i in range(len(text) - n + 1)]

    return ngrams


def make_list_of_ngrams(tweets, case_sensitive, remove_stop, n):
    '''
    Generates a list of ngrams from a group of tweets

    Inputs:
        tweets: a list of tweets
        case_sensitive (boolean): True if case needs to be preserved
        remove_stop (boolean): True if stop words need to be removed
        n: integer

    Returns: list of n-grams from a series of tweets
    '''

    list_of_ngrams = []

    for tweet in tweets:
        ngrams = make_ngrams(tweet, case_sensitive, remove_stop, n)
        for ngram in ngrams:
            list_of_ngrams.append(ngram)

    return list_of_ngrams


def find_top_k_ngrams(tweets, n, case_sensitive, k):
    '''
    Find k most frequently occurring n-grams

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        k: integer

    Returns: list of n-grams
    '''

    list_of_ngrams = make_list_of_ngrams(tweets, case_sensitive, True, n)
    top_k_ngrams = find_top_k(list_of_ngrams, k)

    return top_k_ngrams


def find_min_count_ngrams(tweets, n, case_sensitive, min_count):
    '''
    Find n-grams that occur at least min_count times

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        min_count: integer

    Returns: set of n-grams
    '''

    list_of_ngrams = make_list_of_ngrams(tweets, case_sensitive, True, n)
    ngrams_set = find_min_count(list_of_ngrams, min_count)

    return ngrams_set


def find_salient_ngrams(tweets, n, case_sensitive, threshold):
    '''
    Find the salient n-grams for each tweet

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        threshold: float

    Returns: list of sets of strings
    '''

    list_of_list_of_ngrams = []

    for tweet in tweets:
        ngrams = make_ngrams(tweet, case_sensitive, False, n)
        list_of_list_of_ngrams.append(ngrams)

    salient_lst = find_salient(list_of_list_of_ngrams, threshold)

    return salient_lst

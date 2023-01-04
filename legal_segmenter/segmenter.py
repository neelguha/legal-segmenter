"""
Functions for segmenting a legal text into a sequence of sentences.
"""

from legal_segmenter.constants import *
from typing import List


def segment(text: str) -> List[List[str]]:
    """
    Segments text into list of lists. The top level lists 
    denote different paragraphs, and elements of the top level lists
    contain sentences.  
    
    Args: 
        text: input text to segment 
    Returns: 
        paragraphs: list of sentences
    """
    paragraphs = []
    # Split by newline first
    for paragraph_text in text.split("\n"):
        sentences = [[]]
        words = paragraph_text.split(" ")
        for idx in range(len(words)): 
            word = words[idx]

            # First word of sentence, just add it
            if idx == 0: 
                sentences[-1].append(word)
                continue 
            
            prior_word = words[idx-1]
            
            # sentence must end on period, so any words which don't end with a period
            # are not terminal words
            if not contains_terminal_punctuation(prior_word):
                sentences[-1].append(word)
                continue

            # Check if the word is a common abbreviation. If so, it is unlikely to be
            # a terminal word.
            if is_abbreviation(prior_word):
                sentences[-1].append(word)
                continue
            
            # If there is another period in the word, it is usually an abbreviation. However, 
            # sometimes the previous word is the end of a parenthetical, in which case you get
            # ".).". This checks for that.
            
            if "." in prior_word[:len(prior_word)-1] and not word_with_punctuation(prior_word):
                sentences[-1].append(word)
                continue
            
            
            # This is almost always a pincite. 
            if word == "at":
                sentences[-1].append(word)
                continue
            
            # The last word of the previous sentence is one letter long (an initial)
            if len(prior_word) < 3:
                sentences[-1].append(word)
                continue


            # The first letter of the word is lowercase, so its unlikely to be 
            # the start of a new sentence.
            if word[0].islower():
                sentences[-1].append(word)
                continue
            
            # If none of the above conditionals fire, then it's probably the case that
            # the word is the start of a new sentence.
            sentences.append([word])
        
        # Convert sentence representation from list of words to sentences.
        for i in range(len(sentences)):
            sentences[i] = " ".join(sentences[i])
        paragraphs.append(sentences)

    return paragraphs


def contains_terminal_punctuation(word):
    """ 
    Returns true if the word contains punctuation which should indicate the
    end of a sentence.
    """

    if "..." in word:
        return False

    if word.endswith("."):
        return True 

    if word.endswith(".)"):
        return True

    if word.endswith(".\""):
        return True 

    if word.endswith(".)"):
        return True

    if word.endswith(".”"):
        return True

    if word.endswith(".’"):
        return True

    if word.endswith("!"):
        return True 

    if word.endswith("?"):
        return True 

    if word.endswith(".”"):
        return True
    
    return False


def word_with_punctuation(word):
    if ")" in word: 
        return True 
    if "\"" in word: 
        return True
    if "”" in word:
        return True
    return False


def is_abbreviation(word):
    """ Returns true if word is abbreviation """
    word = word.replace(")", "")
    word = word.replace("(", "")
    word = word.replace("\"", "")
    word = word.replace("”", "")
    word = word.replace("-", "")
    word = word.replace("’", "")

    if word in NON_TERMINAL_WORDS:
        return True

    return False
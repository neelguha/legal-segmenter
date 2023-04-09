"""
Functions for segmenting a legal text into a sequence of sentences.
"""

from typing import List

from legal_segmenter.constants import *

import importlib.resources


class Segmenter:
    """
    Defines a segmenter object. Our algorithm for segmentation combines a set of heuristic rules and common legal abbreviations. We apply these rules and abbreviations to determine when a word has a high chance of corresponding to a terminal token in a sentence.


    """

    def __init__(self, constants: set = None, override: bool = False):
        """
        Initializes a segmenter object.
        """
        self.constants = set()
        if override:
            self.constants.update(constants)
        else:
            FILES = [
                "case_names.txt",
                "court_documents.txt",
                "court_names.txt",
                "geographical_terms.txt",
                "judges_and_officials.txt",
                "legislative_docs.txt",
                "months.txt",
                "periodicals.txt",
                "publishing_terms.txt",
                "services.txt",
                "subdivisions.txt",
            ]
            for file in FILES:
                fpath = f"constants/file"
                string = importlib.resources.read_text(
                    "legal_segmenter.constants", file
                )
                for s in string.split("\n"):
                    self.constants.add(s.strip())

    def segment(self, text: str) -> List[List[str]]:
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

                prior_word = words[idx - 1]

                # sentence must end on period, so any words which don't end with a period
                # are not terminal words
                if not self.contains_terminal_punctuation(prior_word):
                    sentences[-1].append(word)
                    continue

                # Check if the word is a common abbreviation. If so, it is unlikely to be
                # a terminal word.
                if self.is_abbreviation(prior_word):
                    sentences[-1].append(word)
                    continue

                # If there is another period in the word, it is usually an abbreviation. However,
                # sometimes the previous word is the end of a parenthetical, in which case you get
                # ".).". This checks for that.

                if "." in prior_word[
                    : len(prior_word) - 1
                ] and not self.word_with_punctuation(prior_word):
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

    def contains_terminal_punctuation(self, word: str) -> bool:
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

        if word.endswith('."'):
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

    def word_with_punctuation(self, word: str) -> bool:
        """
        Returns true if there is punctuation in the word.
        """
        if ")" in word:
            return True
        if '"' in word:
            return True
        if "”" in word:
            return True
        return False

    def is_abbreviation(self, word: str) -> bool:
        """
        Returns true if word is abbreviation.
        """
        word = word.replace(")", "")
        word = word.replace("(", "")
        word = word.replace('"', "")
        word = word.replace("”", "")
        word = word.replace("-", "")
        word = word.replace("’", "")

        if word in self.constants:
            return True

        return False

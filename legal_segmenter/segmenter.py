"""
Functions for segmenting a legal text into a sequence of sentences.
"""

from typing import List, Union, TypedDict

from legal_segmenter.constants import *

import importlib.resources


class Sentence(TypedDict):
    text: str
    tokens: List[str]
    start: int
    end: int


class Paragraph(TypedDict):
    sentences: List[Sentence]
    start: int
    end: int


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

    def segment(
        self, text: str, include_metadata: bool = False
    ) -> Union[List[List[str]], List[Paragraph]]:
        """
        Segments text into list of lists. The top level lists
        denote different paragraphs, and elements of the top level lists
        contain sentences.

        Args:
            text: input text to segment
        Returns:
            paragraphs: list of paragraphs, each of which is a list of sentences. If include_metadata=False,
            this is simply a list of lists of strings. If include_metadata=True, this is a list of Paragraph objects,
            each of which contains a "sentences" key, which is a list of Sentence objects.
        """
        paragraphs = []
        curr_paragraph_offset = 0
        # Split by newline first
        for paragraph_text in text.split("\n"):
            if len(paragraph_text) == 0:
                curr_paragraph_offset += 1
                continue

            curr_paragraph: Paragraph = {
                "sentences": [],
                "start": curr_paragraph_offset,
                "end": None,
            }
            curr_sentence: Sentence = {
                "text": None,
                "tokens": [],
                "start": curr_paragraph_offset,
                "end": None,
            }
            words = paragraph_text.split(" ")
            for idx, word in enumerate(words):
                # First word of sentence, just add it
                if idx == 0:
                    curr_sentence["tokens"].append(word)
                    continue
                
                if len(word) == 0:
                    curr_sentence["tokens"].append(word)
                    continue

                prior_word = words[idx - 1]

                # sentence must end on period, so any words which don't end with a period
                # are not terminal words
                if not self.contains_terminal_punctuation(prior_word):
                    curr_sentence["tokens"].append(word)
                    continue

                # Check if the word is a common abbreviation. If so, it is unlikely to be
                # a terminal word.
                if self.is_abbreviation(prior_word):
                    curr_sentence["tokens"].append(word)
                    continue

                # If there is another period in the word, it is usually an abbreviation. However,
                # sometimes the previous word is the end of a parenthetical, in which case you get
                # ".).". This checks for that.

                if "." in prior_word[
                    : len(prior_word) - 1
                ] and not self.word_with_punctuation(prior_word):
                    curr_sentence["tokens"].append(word)
                    continue

                # This is almost always a pincite.
                if word == "at":
                    curr_sentence["tokens"].append(word)
                    continue

                # The last word of the previous sentence is one letter long (an initial)
                if len(prior_word) < 3:
                    curr_sentence["tokens"].append(word)
                    continue

                # The first letter of the word is lowercase, so its unlikely to be
                # the start of a new sentence.
                if word[0].islower():
                    curr_sentence["tokens"].append(word)
                    continue

                # If none of the above conditionals fire, then it's probably the case that
                # the word is the start of a new sentence.
                curr_sentence["text"] = " ".join(curr_sentence["tokens"])
                curr_sentence["end"] = curr_sentence["start"] + len(
                    curr_sentence["text"]
                )
                curr_paragraph["sentences"].append(curr_sentence)

                # Create the next sentence with the current word as the first token
                curr_sentence = {
                    "text": None,
                    "tokens": [word],
                    "start": curr_sentence["end"] + 1,
                    "end": None,
                }

            # Add last sentence
            curr_sentence["text"] = " ".join(curr_sentence["tokens"])
            curr_sentence["end"] = curr_sentence["start"] + len(curr_sentence["text"])
            curr_paragraph["sentences"].append(curr_sentence)

            curr_paragraph["end"] = curr_paragraph["start"] + len(paragraph_text)
            paragraphs.append(curr_paragraph)
            curr_paragraph_offset += len(paragraph_text) + 1

        if include_metadata:
            return paragraphs
        return [[s["text"] for s in p["sentences"]] for p in paragraphs]

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

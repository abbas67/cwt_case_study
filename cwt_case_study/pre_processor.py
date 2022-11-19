import re
from abc import ABC, abstractmethod

import spacy
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords


class PreProcessor(ABC):
    """
    Abstract class to preprocess data for model.
    """

    @staticmethod
    def remove_digits(text):
        return ''.join([i for i in text if not i.isdigit()])

    @staticmethod
    def lowercase(text):
        return text.lower()

    @staticmethod
    def remove_punctuation(text):
        return re.sub(r'[^\w\s]', '', text)

    @abstractmethod
    def remove_stop_words(self, text):
        pass

    @abstractmethod
    def get_lemma(self, text):
        pass


class NltkPreProcessor(PreProcessor):

    def get_lemma(self, text):
        return " ".join([WordNetLemmatizer().lemmatize(w) for w in text.split()])

    def remove_stop_words(self, text):
        return" ".join([w for w in text.split() if w not in set(stopwords.words("english"))])


class SpacyPreProcessor(PreProcessor):

    def __init__(self):
        super().__init__()
        self.nlp = spacy.load("en_core_web_sm", disable=["tok2vec", "textcat", "ner"])

    def get_lemma(self, text):
        # TODO: Investigate why this isn't working.
        return ' '.join([str(token.lemma_) for token in self.nlp(text)])

    def remove_stop_words(self, text):

        return ' '.join([str(token) for token in self.nlp(text) if not token.is_stop])





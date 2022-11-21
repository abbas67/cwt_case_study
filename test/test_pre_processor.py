import unittest
from cwt_case_study.pre_processor import NltkPreProcessor, SpacyPreProcessor


class TestPreProcessor(unittest.TestCase):

    def test_remove_digits(self):
        pre_processor = NltkPreProcessor()
        result = pre_processor.remove_digits("1Hello 23My 4Name5 is Abba24s")
        self.assertEqual("Hello My Name is Abbas", result)

    def test_lowercase(self):
        pre_processor = NltkPreProcessor()
        result = pre_processor.lowercase("HELLO MY NAME IS ABBAS")
        self.assertEqual("hello my name is abbas", result)

    def test_remove_punctuation(self):
        pre_processor = NltkPreProcessor()
        result = pre_processor.remove_punctuation("hello, my name is (abbas). Hope you're well!")
        self.assertEqual("hello my name is abbas Hope youre well", result)

    def test_all_general(self):
        pre_processor = NltkPreProcessor()
        result = pre_processor.remove_digits("HE1LLO MY N2AME IS (ABBA3S). HOP4E YOU5'RE WE6LL.")
        result = pre_processor.lowercase(result)
        result = pre_processor.remove_punctuation(result)
        self.assertEqual("hello my name is abbas hope youre well", result)

        pre_processor = NltkPreProcessor()
        result = pre_processor.remove_digits("")
        result = pre_processor.lowercase(result)
        result = pre_processor.remove_punctuation(result)
        self.assertEqual("", result)

        pre_processor = NltkPreProcessor()
        result = pre_processor.remove_digits("123")
        result = pre_processor.lowercase(result)
        result = pre_processor.remove_punctuation(result)
        self.assertEqual("", result)


class TestPreProcessorNlkt(unittest.TestCase):

    def test_remove_stop_words(self):

        pre_processor = NltkPreProcessor()
        result = pre_processor.remove_stop_words("delete are the is are")
        self.assertEqual("delete", result)

    def test_get_lemma(self):
        pre_processor = NltkPreProcessor()
        result = pre_processor.get_lemma("rocks corpora")
        self.assertEqual("rock corpus", result)

    def test_all_processing(self):

        pre_processor = NltkPreProcessor()
        result = pre_processor.remove_digits("HE1LLO MY N2AME IS (ABBA3S). HOP4E YOU5'RE WE6LL. ROCKS")
        result = pre_processor.lowercase(result)
        result = pre_processor.remove_punctuation(result)
        result = pre_processor.remove_stop_words(result)
        result = pre_processor.get_lemma(result)
        self.assertEqual(result, "hello name abbas hope youre well rock")


class TestPreProcessorSpacy(unittest.TestCase):

    def test_remove_stop_words(self):
        pre_processor = SpacyPreProcessor()
        result = pre_processor.remove_stop_words("foo bar are the is are")
        self.assertEqual("foo bar", result)

    @unittest.skip("Issue with spacy lemmatization")
    def test_get_lemma(self):
        pre_processor = SpacyPreProcessor()
        result = pre_processor.get_lemma("apples, oranges")
        self.assertEqual("apple, orange", result)

    def test_all_processing(self):
        pre_processor = SpacyPreProcessor()
        result = pre_processor.remove_digits("HE1LLO MY N2AME IS (ABBA3S). HOP4E YOU5'RE WE6LL. ROCKS")
        result = pre_processor.lowercase(result)
        result = pre_processor.remove_punctuation(result)
        result = pre_processor.remove_stop_words(result)
        self.assertEqual(result, "hello abbas hope rocks")


if __name__ == '__main__':
    unittest.main()

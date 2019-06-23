import unittest
from tfidf.tfidfAlgorithms import TFAlgorithm, IDFSmoothAlgorithm, TFIDF

class TestTFIDFAlgorithms(unittest.TestCase):
    def compareFn(self, a, b):
        return a == b

    def testTFAlgorithm(self):
        algorithm = TFAlgorithm()
        wordCount = 1
        term = "test1"
        fileWords = ["test1"]
        self.assertEqual(algorithm(wordCount, term, fileWords, self.compareFn), 1.0)

    def testIDFAlgorithm(self):
        algorithm = IDFSmoothAlgorithm()
        self.assertEqual(algorithm(6,2), 0.3010299956639812)

    def testTFIDF(self):
        tfidf = TFIDF()
        self.assertEqual(tfidf.compute(2,3), 6) 

if __name__ == '__main__':
    unittest.main()
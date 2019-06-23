import unittest
import mock
from tfidf.tfidf import App
from tfidf.tfidfAlgorithms import TFFile


class TestTFIDF(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestTFIDF, self).__init__(*args, **kwargs)
        self.testDict = {
            'test1': 0.6666666666666666, 
            'test2': 0.3333333333333333
            }
        self.testTerms = ["test1","test2"]
        testFile = TFFile("testFile")
        testFile.setTF(self.testDict)
        self.testFiles = [testFile]

    def testComputeText(self):
        app = App()
        app.terms = self.testTerms
        testText = "test1 test1 test2"
        frequencies = app.computeTFForText(testText)
        self.assertEquals(frequencies, self.testDict)

    def getFileContentsMock(self, fileName, threadName = ''):
        return "test1 test1 test2"

    def testParseFile(self):
        with mock.patch.object(App, 'getFileContents', new=self.getFileContentsMock):
            app = App()
            app.terms = self.testTerms
            app.parseFile("testFile")
            app.parseFile("testFile2")
            self.assertEquals(len(app.tfFiles), 2)
            self.assertEquals(app.tfFiles[0].name,"testFile")
            self.assertDictEqual(app.tfFiles[0].termsTF, self.testDict)

    def testReport(self):
        app = App()
        app.search = mock.MagicMock(return_value=0)
        app.terms = self.testTerms
        app.N = 5
        # Test no files should call search with empty computedFiles
        app.report()
        app.search.assert_called_with(5, {})

        # Test one file 
        app.tfFiles = self.testFiles
        app.directoryChecksum = '1'
        app.report()
        outList = {}
        outList[self.testFiles[0].name] = -0.3010299956639812 
        app.search.assert_called_with(5, outList)


if __name__ == '__main__':
    unittest.main()
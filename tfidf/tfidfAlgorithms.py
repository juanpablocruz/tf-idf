from math import log10

class TFFile:
    """
    Class used to hold TF information for a file
    
    ...

    Attributes
    ----------
    name: str
        The name of the file
    termsTF: dict
        A dictionary holding each term as key with it's TF as value

    Methods
    -------
    setTF(tfs)
        Sets the file computed TFs dict
    getTF(term)
        Returns the term's TF for this file
    printFile()
        Helper for displaying the name and the TF's
    """
    def __init__(self, name):
        self.name = name
        self.termsTF = {}

    def setTF(self, tfs):
        self.termsTF = tfs

    def getTF(self, term):
        return self.termsTF.get(term, 0)

    def printFile(self):
        print self.name, self.termsTF

    def __repr__(self):
        return self.name


class TFAlgorithm:
    def computeAparitions(self, fileWords, term, compareText):
        frequencies = 0
        for word in fileWords:
            if compareText(word, term):
                frequencies = frequencies + 1
        return frequencies


    """ Defines a Term Frequency calculation algorithm """
    def __call__(self, wordCount,term, fileWords, compareText):
        frequencies = self.computeAparitions(fileWords, term, compareText)
        return frequencies/float(wordCount)


class TFRawCount(TFAlgorithm):
    def __call__(self, wordCount,term, fileWords, compareText):
        frequency = self.computeAparitions(fileWords, term, compareText)
        return frequency


class TFBinary(TFAlgorithm):
    def __call__(self, wordCount,term, fileWords, compareText):
        frequency = self.computeAparitions(fileWords, term, compareText)
        return frequency > 0


class TFLogNormalization(TFAlgorithm):
    def __call__(self, wordCount,term, fileWords, compareText):
        frequency = self.computeAparitions(fileWords, term, compareText)
        return log10(1 + frequency)


class TFDoubleNormalization(TFAlgorithm):
    def mostFrequent(self, List):
        count = 0
        elem = List[0]

        for i in List:
            currFrequency = List.count(i)
            if (currFrequency > count):
                count = currFrequency
                elem = i
        return (elem,count)

    def __call__(self, wordCount,term, fileWords, compareText):
        frequency = self.computeAparitions(fileWords, term, compareText)
        (mostFrequent, masOcurrences) = self.mostFrequent(fileWords)
        return 0.5 + (0.5 * (frequency / masOcurrences))


class IDFAlgorithm:
    def __call__(self, totalDocs, totalOccurrences):
        return log10(totalDocs/(totalOccurrences))


class IDFUnaryAlgorithm(IDFAlgorithm):
    def __call__(self, totalDocs, totalOccurrences):
        return 1


class IDFSmoothAlgorithm(IDFAlgorithm):
    def __call__(self, totalDocs, totalOccurrences):
        return log10(totalDocs/(1.0+totalOccurrences))


class IDFProbabilistic(IDFAlgorithm):
    def __call__(self, totalDocs, totalOccurrences):
        return (totalDocs - totalOccurrences) / float(totalOccurrences)


class TFIDF:
    """ 
    TFIDF class contains a TermFrequency and a Inverse Document Frequency algorithms
    It provides a compute method which returns the tf-idf value
    """
    def __init__(self, tfAlgorithm = TFAlgorithm, idfAlgorithm = IDFSmoothAlgorithm):
        self.tfAlgorithm = tfAlgorithm()
        self.idfAlgorithm = idfAlgorithm()

    def compute(self, tf, idf):
        return tf*idf

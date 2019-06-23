#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, getopt
from os import listdir
from os.path import isfile, join, isdir
from watcher import Watcher
import operator
from tfidfAlgorithms import TFIDF, TFFile
import threading
import time
import hashlib

class App():
    def __init__(self):
        self.directory=''
        self.tfFiles = []
        self.terms = []
        self.tfidf = TFIDF() 
        self.N = 0
        self.sortedFiles = {}
        self.directoryChecksum = ''
        self.lastReportChecksum = ''

    def compareText(self, str1, str2):
        """
        Comparition function to determine if str1 and str2 are
        simillar enough
        ENHANCE: it can be enhanced to return true in case of 
        simillarity instead of equallity. (eg. Needleman–Wunsch)
        """
        return str1 == str2

    def computeTFForText(self, fileText):
        """ 
        Computes the Term Frequency of every term in the input query for 
        the given text using the configured tf algorithm
        """
        frequencies = {}
        fileWords = fileText.split()
        wordCount = len(fileWords)
        algorithm = self.tfidf.tfAlgorithm
        
        if wordCount:
            for term in self.terms:
                frequencies[term] = algorithm(wordCount, term, fileWords, self.compareText)
        return frequencies 

    def search(self, N, files):
        """ Prints the top N files in descending order """
        sortedFiles = sorted(files.items(), key=operator.itemgetter(1), reverse=True)
        for file in sortedFiles[:N]:
            print file[0], file[1]
        print("\n")

    def cleanText(self, text):
        """ 
        Removes any unwanted character from the string in order to easier 
        word matching
        """
        blackList = [',', '.']
        for character in blackList:
            text = text.replace(character, '')
        return text

    def getFileContents(self, fileName):
        """
        Retrieve the contents of the file
        """
        fp = open(fileName, "r")
        return fp.read()

    def parseFile(self, fileName, threadId = ''):
        """
        Reads the file 'fileName' and removes the characters , and .
        And then computes the TF for that text and stores a TFFile
        """
        shortName = fileName.replace(self.directory+"/", '')
        f = TFFile(shortName)
        fileText = self.cleanText(self.getFileContents(fileName))
        f.setTF(self.computeTFForText(fileText))
        self.tfFiles.append(f)

    def notify(self, file):
        """
        Process the TF calculations for the new added file
        """
        #We know there's a change in the directory so we update the checksum
        files = [f for f in listdir(self.directory) if isfile(join(self.directory, f))]
        self.directoryChecksum = self.checksum(files)

        self.parseFile(file)

    def calculateTermOcurrences(self):
        """
        Returns the total ocurrences of each term accross all the
        documents in the corpus
        """
        termOcurrences = {}
        for term in self.terms:
            totalOccurrences = 0
            for file in self.tfFiles:
                if file.getTF(term) > 0:
                    totalOccurrences = totalOccurrences + 1
            termOcurrences[term] = totalOccurrences
        return termOcurrences

    def computeTFIDF(self, termOcurrences):
        """
        Computes the TF-IDF for each file and returns 
        a dict of files with its value
        """
        computedFiles = {}

        if len(self.tfFiles) == 0:
            return computedFiles

        idfAlgorithm = self.tfidf.idfAlgorithm
        idfCompute = self.tfidf.compute

        for term in self.terms:
            termIdf = idfAlgorithm(len(self.tfFiles), termOcurrences.get(term,0))
            for file in self.tfFiles:
                idfComputed = idfCompute(file.getTF(term), termIdf)
                computedFiles[file.name] = computedFiles.get(file.name,0) + idfComputed

        self.sortedFiles = computedFiles
        return computedFiles

    def report(self):
        """
        This method is called every P seconds
        It computes the IDF for every TFFile and prints the top N
        """ 
        computedFiles = self.sortedFiles
        #We only want to recompute everything 
        #if the directory has changed
        if self.lastReportChecksum != self.directoryChecksum :
            self.lastReportChecksum = self.directoryChecksum
            #Calculate in how many documents appears each file
            termOcurrences = self.calculateTermOcurrences()
            #Calculate the TF-IDF for each file for all terms
            computedFiles = self.computeTFIDF(termOcurrences)
            #Sort and output the top N files 
        self.search(self.N, computedFiles)


    def directoryWatch(self):
        """ Enables the directory watch """
        w = Watcher(self.directory, self.notify)
        w.run()

    def printHelp(self):
        """ Prints the usage message """
        print("Usage:")
        print('tfidf.py -d, -n, -t, -p')
        print('     -d  [directory]')
        print('     -n  [top n files to return]')
        print('     -p  [period of report in seconds]')
        print('     -t  [space separated list of terms to query]')

    def checksum(self, files):
        checksum = hashlib.md5()
        for file in files:
            checksum.update(hashlib.md5(file).hexdigest())
        return checksum.hexdigest()   

    def parseCMD(self, argv):
        TT = ''
        try:
            opts, args = getopt.getopt(argv,"d:n:p:t:")
        except getopt.GetoptError:
            self.printHelp()
            sys.exit(2)

        for opt, arg in opts:
            if opt == '-d':
                self.directory = arg
            elif opt == '-n':
                self.N = int(arg)
            elif opt == '-p':
                self.P = int(arg)
            elif opt == '-t':
                TT = arg
        self.terms = TT.split()

    def run(self, argv): 
        self.parseCMD(argv)
        error = False
        if (isdir(self.directory) != True):
            print(self.directory + " folder not found.")
            error = True

        if (len(self.terms) < 1):
            print("-t cannot be empty")
            error = True

        if (error  or self.N < 0 or self.P < 0) :
            self.printHelp()
            sys.exit(2)

        files = [f for f in listdir(self.directory) if isfile(join(self.directory, f))]
        self.lastReportChecksum = 0
        #In order to not compute again everything if anything has changed
        #we want to cache the  current directory status by making a checksum
        #of the files in the dir
        self.directoryChecksum = self.checksum(files)
        threads = []
        #Process each file in a separate thread 
        for file in files:
            fileName = self.directory + "/" + file
            thread = threading.Thread(target=self.parseFile, args=(fileName, "thread-"+file))
            thread.start()
            threads.append(thread)
        
        #Watch for any new file in the directory in a separate thread as a daemon
        watch = threading.Thread(target=self.directoryWatch, name='DirectoryWatch')
        watch.setDaemon(True)
        watch.start()

        #Wait for all threads to finish
        for t in threads:
            t.join()
        try:
            while True:
                self.report()
                time.sleep(self.P)
        except:
            print("")


def main():
    app = App()
    app.run(sys.argv[1:])

if __name__ == "__main__":
    main()

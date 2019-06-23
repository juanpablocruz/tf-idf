# TFIDF 

This program watches over a directory and returns the N top ranked files for a given query string.

### Algorithm
>Term Frequency - Inverse Document Frequency is an algorithm for computing the relevance of a word in a file against itself and the corpus of all the others files in the directory.

The time complexity in the worst case is:
- <img src="https://latex.codecogs.com/gif.latex?O(n^3)\text\ On\ single\ thread" /> 
- <img src="https://latex.codecogs.com/gif.latex?O(n^2)\text\ On\ multithread" /> 
assuming there are the same number of terms as files and words in files

And the space is <img src="https://latex.codecogs.com/gif.latex?O(2n)" /> as an array and a dict of files are stored.

### Dependencies
In order to watch over a directory TFIDF uses the watchdog module.

### Installation
`$ python setup.py install`

This will add tfidf script to PATH. In OSX/UNIX it will be added to /usr/local/bin

### Usage
`$ python tfidf.py -d dir -n N -p P -t "terms"`

### Run tests
`$ python -m unittest discover -s test -t tfidf`

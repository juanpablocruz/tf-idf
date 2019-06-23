from setuptools import setup

import os
thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setup(name='tfidf',
      version='0.1',
      description='TF-IDF',
      url='http://github.com/juanpablocruz/tf-idf',
      author='Juan Pablo Cruz Maseda',
      author_email='juanpablocruzmaseda@gmail.com',
      license='MIT',
      packages=["tfidf"],
      install_requires=install_requires,
      scripts=["bin/tfidf"],
      zip_safe=False)
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re, sys
import urllib2, nltk

reload(sys)
sys.setdefaultencoding('utf8')

class Scrapper:
    """The authors array from the faculty web page."""
    authors = [];
    dataSet = [];
    dictionary = list();

    @classmethod
    def getAuthors(self):
        urlRequest = urllib2.Request("https://www.eecs.mit.edu/people/faculty-advisors");
        document = urllib2.urlopen(urlRequest);
        soup = BeautifulSoup(document, 'html.parser', from_encoding="utf-8");
        for author in soup.select('span.card-title a'):
            self.authors.append(author.get_text());

    """
    Get abstracts for a given author.
    Request for abstracts looks like:
        https://arxiv.org/search/?query=Elfar+Adalsteinsson&searchtype=author&abstracts=show&order=-announced_date_first&size=50
    """
    @classmethod
    def getAbstracts(self, author):
        rawAuthor = author.replace(' ', '+').replace('.', '');
        url = "https://arxiv.org/search/?query=";
        url += rawAuthor;
        url += "&searchtype=author&abstracts=show&order=-announced_date_first&size=50";
        urlRequest = urllib2.Request(url);
        document = urllib2.urlopen(urlRequest);
        soup = BeautifulSoup(document, 'html.parser');
        for abstract in soup.select('span.abstract-full'):
            """id looks like: 1509.03687v1-abstract-full, kept only numerical index"""
            id = abstract['id'].split('v')[0].split('/')[0];
            abstract = abstract.get_text().replace('\n', '').replace('\S+', ' ');
            """Write data in a different file for each abstract"""
            fileName = 'tmp/' + rawAuthor.replace('+', '_') + '-' + id + '.txt';
            abstractFile = open(fileName, "w+");
            abstractFile.write(abstract.encode('utf-8', errors="ignore").strip());
            abstractFile.close();
            fileIndex = open('file_index.txt', "a+");
            fileIndex.write(fileName + "\n");
            fileIndex.close()
            self.updateDictionary(abstract);

        wordListFile = open('dict.txt', 'w+');
        for word in self.dictionary:
            wordListFile.write(word + '\n');
        wordListFile.close();

    @classmethod
    def updateDictionary(self, abstract):
        # wordList = self.loadDictionary();
        doc = abstract.lower();
        tokens = nltk.wordpunct_tokenize(doc);

        for word in tokens:
            if word not in self.dictionary:
                self.dictionary.append(word);

    @classmethod
    def loadDictionary(self):
        wordList = list();
        wordListFile = open('dict.txt', 'r');
        for word in wordListFile.read().split('\n'):
            wordList.append(word);
        return wordList;




    def main():
        """Default action re-collect data and put it in a file."""


if __name__ == '__main__':
    scrapper = Scrapper();
    scrapper.getAuthors();
    for author in scrapper.authors:
        scrapper.getAbstracts(author);

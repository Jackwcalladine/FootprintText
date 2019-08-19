import urllib
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from collections import OrderedDict
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import re

#here is where the keyword is stored
page = requests.get("https://www.google.dz/search?q=kids parties")
soup = BeautifulSoup(page.content)

links = soup.findAll("a")
text_list = []
for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
    text_list.append(re.split(":(?=http)",link["href"].replace("/url?q=","")))

#gets the pages URL without the extra nonsense at the end    
def trunc_at(s, d, n=3):
    "Returns s truncated at the n'th (3rd by default) occurrence of the delimiter, d."
    return d.join(s.split(d, n)[:n])

fixed_list = []
for item in text_list:
    fixed_list.append(str(item[0]))

truncated = []
for item in fixed_list:
    truncated.append(trunc_at(item, '/'))

usable_list = list(OrderedDict.fromkeys(truncated))

#presents html in a list with spaces, tags and other HTML elements removed
final_list = []
for item in usable_list:
    try:
        url = item
        html = urlopen(url).read()
        soup = BeautifulSoup(html)
        for script in soup(["script", "style"]):
            script.extract()  # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        final_list.append(text)
    except urllib.error.HTTPError:
        pass

tokenizer = RegexpTokenizer(r'\w+')

final_list = str(final_list)
tokenized_sents = tokenizer.tokenize(final_list)
stopWords = set(stopwords.words('english'))
stopWords = list(stopWords)
wordsFiltered = []

for w in tokenized_sents:
    if w not in stopWords:
        wordsFiltered.append(w)

filtered = []
for w in wordsFiltered:
   filtered.append(w.lower())

fd = nltk.FreqDist(filtered)
fd.plot(20, cumulative = False)

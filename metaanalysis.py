import requests
from bs4 import BeautifulSoup
import time
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


def fetch_results(search_term, number_results, language_code):
    assert isinstance(search_term, str), 'Search term must be a string'
    assert isinstance(number_results, int), 'Number of results must be an integer'
    escaped_search_term = search_term.replace(' ', '+')

    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results, language_code)
    response = requests.get(google_url, headers=USER_AGENT)
    response.raise_for_status()

    return search_term, response.text

def parse_results(html, keyword):
    soup = BeautifulSoup(html, 'html.parser')

    found_results = []
    rank = 1
    result_block = soup.find_all('div', attrs={'class': 'g'})
    for result in result_block:

        link = result.find('a', href=True)
        title = result.find('h3')
        description = result.find('span', attrs={'class': 'st'})
        if link and title:
            link = link['href']
            title = title.get_text()
            if description:
                description = description.get_text()
            if link != '#':
                found_results.append({'keyword': keyword, 'rank': rank, 'title': title, 'description': description})
                rank += 1
    return found_results

def scrape_google(search_term, number_results, language_code):
    try:
        keyword, html = fetch_results(search_term, number_results, language_code)
        results = parse_results(html, keyword)
        return results
    except AssertionError:
        raise Exception("Incorrect arguments parsed to function")
    except requests.HTTPError:
        raise Exception("You appear to have been blocked by Google")
    except requests.RequestException:
        raise Exception("Appears to be an issue with your connection")


if __name__ == '__main__':
    keywords = ['kids party']
    data1 = []
    for keyword in keywords:
        try:
            results = scrape_google(keyword, 100, "en")
            for result in results:
                data1.append(result)
        except Exception as e:
            pass
        except TypeError:
            pass
        finally:
            time.sleep(10)
    print(data1)

newrow = [d['rank'] for d in data1]
newrow1 = [d['keyword'] for d in data1]
newrow2 = [d['title'] for d in data1]
newrow3 = [d['description'] for d in data1]

tokenizer = RegexpTokenizer(r'\w+')

newrow3 = str(newrow3)
tokenized_sents = tokenizer.tokenize(newrow3)
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

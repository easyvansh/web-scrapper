from encodings import utf_8
import requests
from bs4 import BeautifulSoup
import pymongo
def scrape_quotes():
    more_links = True
    page =1 

    # list to hold the quotes
    quotes = []


    while (more_links):
        # make a request to the site and get it as a string
        markup = requests.get(f'http://quotes.toscrape.com/').text
        # passing the string to BeautifulSoup will
        soup  = BeautifulSoup(markup,'html.parser')

        # now we can select elements
        for item in soup.select('.quote'):
            quote = {}
            quote['text'] = item.select_one('.text').get_text()
            quote['author'] = item.select_one('.author').get_text()
            # get the tags element
            tags = item.select_one('.tags')
            # geting tags from the tags element
            quote['tags'] = [tag.get_text() for tag in tags.select('.tags')]
            quotes.append(quote)

        next_link = soup.select_one('.next > a')

        # print which page was scraped
        print(f'scraped page {page}')
        # check if the next link element exists
        if page == 100:
            more_links =False
        elif(next_link):
            page += 1
        else:
            more_links = False
    return quotes

quotes = scrape_quotes()
quotes = sorted(quotes,key=lambda d:d['author'])

data =''
for i in quotes:

    data += 'Quote:'+str(i['text']) + '\n'
    data += 'By:' +str(i['author']) + '\n'
    data += '\n'
    # data += 'Image:' + str(item[1][0])+ '\n'
# print(data)


with open('scrapped.txt','w',encoding='utf_8') as f:
    f.write(data)
# print all scraped quotes
# print(quotes)

client = pymongo.MongoClient("mongodb+srv://v:123@cluster0.i425r.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# db = client.test
db = client.db.quotes
try:
    db.insert_many(quotes)
    print(f'inserted {len(quotes)} articles')
except:
    print('an error occurred quotes were not stored to db')
from youtubesearchpython import SearchVideos
from nltk import tokenize
import wikipediaapi

def get_sentences(text, sen=2):
    strings = tokenize.sent_tokenize(text)
    strings = [strings[x] for x in range(sen)]
    return strings


def get_wiki(subject, sen=2):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page_py = wiki_wiki.page(subject)
    if page_py.exists():
        print("Page - Title: %s" % page_py.title)
        wiki = ' '.join(map(str, page_py.summary))  # convert list to string for display
        print("Page - Summary: %s" % wiki)
        
      
      
def get_video(message, n=2):
    search = SearchVideos(message.content, offset=1, mode="dict", max_results=2)
    search = search.result()
    for i in range(n):
        await message.author.send(str(search['search_result'][i]['link']))

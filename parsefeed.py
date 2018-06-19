import feedparser
import re


def get_feed(selected):
    feed = feedparser.parse(selected[1])
    for x in range(0, len(feed['entries'])):
        feed['entries'][x]['summary'] = re.sub('<[^>]+>', '', feed['entries'][x]['summary'])
        feed['entries'][x]['summary'] = feed['entries'][x]['summary'].replace("&nbsp;", " ")
        feed['entries'][x]['summary'] = feed['entries'][x]['summary'].replace("\n", " ")
        feed['entries'][x]['summary'] = feed['entries'][x]['summary'].replace("ë", "e")
        feed['entries'][x]['summary'] = feed['entries'][x]['summary'].replace("ï", "i")
        feed['entries'][x]['summary'] = feed['entries'][x]['summary'].replace("ö", "o")
        feed['entries'][x]['summary'] = feed['entries'][x]['summary'].replace("ä", "a")
        feed['entries'][x]['summary'] = feed['entries'][x]['summary'].replace("ü", "u")
        #feed['entries'][x]['summary'] = feed['entries'][x]['summary'].replace("'s a", "sa") # 's avonds
        #feed['entries'][x]['summary'] = feed['entries'][x]['summary'].replace("'", "")

    return feed['entries']

import feedparser
import re


def get_feed(selected):
    feed = feedparser.parse(selected[1])
    for x in range(0, len(feed['entries'])):
        feed['entries'][x]['summary'] = re.sub('<[^>]+>', '', feed['entries'][x]['summary'])
        feed['entries'][x]['summary'] = feed['entries'][x]['summary'].replace("&nbsp;", " ")
        feed['entries'][x]['summary'] = feed['entries'][x]['summary'].replace("\n", " ")

    return feed['entries']

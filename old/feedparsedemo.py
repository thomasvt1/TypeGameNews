import feedparser
import re

python_wiki_rss_url = "https://feeds.feedburner.com/jeugdjournaal"

feed = feedparser.parse( python_wiki_rss_url )
for x in range(0, 20):
    feed['entries'][x]['summary'] = re.sub('<[^>]+>', '', feed['entries'][x]['summary'])

for x in range(0, 20):
    print(feed['entries'][x]['summary'])

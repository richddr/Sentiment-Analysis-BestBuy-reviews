import re
__author__ = 'Richard Garcia || Ricardo Batista'
#pip install python-amazon-product-api
import Tkinter
import lxml
import urllib2
import requests
from pprint import pprint
from amazonproduct import API
config = {
    'access_key': 'AKIAIOPFA44WF2W7AAQA',
    'secret_key': '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',
    'associate_tag': 'richddrtmproj-20',
    'locale': 'us'
}
api = API(cfg=config)
# # get all books from result set and
# # print author and title
#for book in api.item_search('Books', Publisher='Galileo Press'):
    #pprint(vars(book.ItemAttributes))
    # print '%s: "%s"' % (book.ItemAttributes.Author,
    #                     book.ItemAttributes.Title)
#result = api.item_lookup('0446525685', ResponseGroup='Reviews', TruncateReviewsAt=256, IncludeReviewsSummary=False)
#pprint(vars(result.Items.Item.CustomerReviews))
# for item in result.Items.Item:
#     pprint(vars(item))

nreviews_re = {'com': re.compile('\d[\d,]+(?= customer review)'),
               'co.uk':re.compile('\d[\d,]+(?= customer review)'),
               'de': re.compile('\d[\d\.]+(?= Kundenrezens\w\w)')}
no_reviews_re = {'com': re.compile('no customer reviews'),
                 'co.uk':re.compile('no customer reviews'),
                 'de': re.compile('Noch keine Kundenrezensionen')}


def get_number_of_reviews(asin, country='com'):
    url = 'http://www.amazon.{country}/product-reviews/{asin}'.format(country=country, asin=asin)
    html = requests.get(url).text
    try:
        return int(re.compile('\D').sub('',nreviews_re[country].search(html).group(0)))
    except:
        if no_reviews_re[country].search(html):
            return 0
        else:
            return None  # to distinguish from 0, and handle more cases if necessary
#print get_number_of_reviews('0446525685', 'com')

countries=['com']
books=[
        '''http://www.amazon.%s/Glass-House-Climate-Millennium-ebook/dp/B005U3U69C''',
        '''http://www.amazon.%s/The-Japanese-Observer-ebook/dp/B0078FMYD6''',
        '''http://www.amazon.%s/Falling-Through-Water-ebook/dp/B009VJ1622''',
      ]

for book in books:
    print '-'*40
    print book.split('%s/')[1]
    for country in countries:
        asin=book.split('/')[-1]; title=book.split('/')[3]
        url='''http://www.amazon.%s/product-reviews/%s'''%(country,asin)
        try: f = urllib2.urlopen(url)
        except: page=""
        page = f.read().lower(); print '%s=%s'%(country, page.count('member-review'))
print '-'*40
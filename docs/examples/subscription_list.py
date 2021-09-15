from email.utils import parsedate_to_datetime as rfc2822_to_datetime
from opml import OpmlDocument

document = OpmlDocument(
    title='mySubscriptions.opml',
    date_created=rfc2822_to_datetime('Sat, 18 Jun 2005 12:11:52 GMT'),
    date_modified=rfc2822_to_datetime('Tue, 02 Aug 2005 21:42:48 GMT'),
    owner_name='Dave Winer',
    owner_email='dave@scripting.com',
    vertical_scroll_state=1,
    window_top=61,
    window_left=304,
    window_bottom=562,
    window_right=842
)

document.add_rss(
    'CNET News.com',
    'http://news.com.com/2547-1_3-0-5.xml',
    description='Tech news and business reports by CNET News.com. Focused on information technology, core topics include computers, hardware, software, networking, and Internet media.',
    html_url='http://news.com.com/',
    language='unknown',
    title='CNET News.com',
    version='RSS2'
)

document.add_rss(
    'washingtonpost.com - Politics',
    'http://www.washingtonpost.com/wp-srv/politics/rssheadlines.xml',
    description='Politics',
    html_url='http://www.washingtonpost.com/wp-dyn/politics?nav=rss_politics',
    language='unknown',
    title='washingtonpost.com - Politics',
    version='RSS2'
)

document.add_rss(
    'Scobleizer: Microsoft Geek Blogger',
    'http://radio.weblogs.com/0001011/rss.xml',
    description='Robert Scoble\'s look at geek and Microsoft life.',
    html_url='http://radio.weblogs.com/0001011/',
    language='unknown',
    title='Scobleizer: Microsoft Geek Blogger',
    version='RSS2'
)

document.dump('subscriptionList.opml', pretty=True, encoding='ISO-8859-1')

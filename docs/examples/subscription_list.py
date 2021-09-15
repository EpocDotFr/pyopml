# Python implementation of http://hosting.opml.org/dave/spec/subscriptionList.opml
from opml import OpmlDocument
from datetime import datetime

document = OpmlDocument(
    title='mySubscriptions.opml',
    date_created=datetime.now(),
    date_modified=datetime.now(),
    owner_name='Dave Winer',
    owner_email='dave@scripting.com',
    vertical_scroll_state=1,
    window_top=61,
    window_left=304,
    window_bottom=562,
    window_right=842,
)

document.add_link(
    'CNET News.com',
    description='Tech news and business reports by CNET News.com. Focused on information technology, core topics include computers, hardware, software, networking, and Internet media.' 
)

from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        print('start--<%s>' % tag)
        print('start--attrs--%s' % attrs)

    def handle_endtag(self, tag):
        print('end--</%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        print('startend--<%s/>' % tag)

    def handle_data(self, data):
        print('data')
        print data

    def handle_comment(self, data):
        print('<!-- -->')

    def handle_entityref(self, name):
        print('entityref-----&%s;' % name)

    def handle_charref(self, name):
        print('charref-----&#%s;' % name)

parser = MyHTMLParser()
parser.feed('<html><head></head><body><p>Some <a href=\"#\">html</a> tutorial...<br>END</p></body></html>')
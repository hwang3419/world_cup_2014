import urllib2
import pickle
from HTMLParser import HTMLParser
import json
URL= 'http://en.wikipedia.org/wiki/2014_FIFA_World_Cup_squads'
CACHE_FILE ='./FIFA'
JSON_FILE = './WORLD_CUP_2014.txt'

def read_html(url):
    response = urllib2.urlopen(url)
    html = response.readlines()
    return html

def dump_data(data):
    pickle.dump(data,open(CACHE_FILE,'wb'))


def load_data():
    return pickle.load(open(CACHE_FILE,'rb'))

def dump_json(data):
    with open(JSON_FILE,'w') as f:
        json.dump(data,f)

class MyParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.CURRENT_IN_HTML = ''
    def handle_data(self,data):
        self.CURRENT_IN_HTML = self.CURRENT_IN_HTML + data

def start_scrape():
    raw = {}
    Parser = MyParser()
    TABLE_FOUND = False
    html = read_html(URL)
    for line in html:
        if TABLE_FOUND:
            #print line
            if line.startswith('<tr>'):
                row = []
            if line.startswith('<th'):
                Parser.feed(line)
                head = Parser.CURRENT_IN_HTML
                Parser.CURRENT_IN_HTML = ''
                head_list.append(head.strip())
            if line.startswith('<td'):
                Parser.feed(line)
                data = Parser.CURRENT_IN_HTML
                Parser.CURRENT_IN_HTML = ''
                row.append(data.strip())
            if line.startswith('</tr>'):
                if row:
                    rows.append(row)


        if line.startswith('<table')  and 'sortable' in line:
            TABLE_FOUND = True
            head_list = []
            row = []
            rows = []
        if line.startswith('</table'):
            TABLE_FOUND = False
            if rows:
                players = [dict(zip(head_list,x)) for x in rows]
                raw[current_country]['players'] = players
            rows = []

        if line.startswith('<h2') and 'mw-headline' in line:
            Parser.feed(line)
            current_group = Parser.CURRENT_IN_HTML.strip()
            Parser.CURRENT_IN_HTML = ''
        if line.startswith('<h3') and 'mw-headline' in line:
            rows = []
            Parser.feed(line)
            current_country = Parser.CURRENT_IN_HTML.strip()
            if current_country.startswith('Player'):
                break
            Parser.CURRENT_IN_HTML = ''
            raw[current_country]={}
            raw[current_country]['group'] = current_group.strip()
            #print current_country
    return raw
        
if __name__ == '__main__':
    data = start_scrape()
    dump_json(data)
    from pprint import pprint
    pprint(data)
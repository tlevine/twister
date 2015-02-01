import requests
import lxml.html
from vlermv import cache

def main():
    import csv, sys
    writer = csv.writer(sys.stdout)
    writer.writerow(('language', 'tongue twister', 'translation'))
    writer.writerows(twister)

def twister():
    for language_url in languages():
        language = parse_language(url)
        for original, translation in language['tongue_twisters']:
            yield language, original, translation

get = cache('~/.twister')(requests.get)
def gethtml(url):
    html = lxml.html.fromstring(get(url).text)
    html.make_links_absolute(url)
    return html

def languages():
    html = gethtml('http://www.uebersetzung.at/twister/index.html')
    return map(str, html.xpath('//p/a[contains(text(), "tongue twisters")]/@href'))

def _parse_pad(pad):
    id = pad.xpath('p[@class="SLC"]/b/a/@href')[0].split('#')[1]
    original = '\n'.join(pad.xpath('p[@class="TXT"]/text()'))
    translation = ''.join(html.xpath('//li[a[@name="T100163"]]/text()')).strip()
    yield original, translation

def parse_language(url):
    html = gethtml(language_url)
    xpath = '//h1[contains(text(), "Tongue Twisters")]'
    return {
        'language': html.xpath(xpath)[0].text_content().strip().replace(' Tongue Twisters', '')
        'tongue_twisters': list(map(_parse_pad, html.xpath('//td[@class="PAD"]')))
    }

if __name__ == '__main__':
    main()

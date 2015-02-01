#!/usr/bin/env python3
import requests
import lxml.html
from vlermv import cache

def main():
    import csv, sys
    writer = csv.writer(sys.stdout)
    writer.writerow(('language', 'tongue twister', 'translation'))
    writer.writerows(twister())

def twister():
    for language_url in languages():
        try:
            language = parse_language(gethtml(language_url))
        except Exception as e:
            e.args = ('%s (%s)' % (e.args[0], language['language']),) + e.args[1:]
            raise e
        for original, translation in language['tongue_twisters']:
            yield language['language'], original, translation

get = cache('~/.twister')(requests.get)
def gethtml(url):
    try:
        html = lxml.html.fromstring(get(url).content.decode('utf-8'))
    except Exception as e:
        print(url)
        raise e
    html.make_links_absolute(url)
    return html

def languages():
    html = gethtml('http://www.uebersetzung.at/twister/index.html')
    for href in html.xpath('//p/a[contains(text(), "tongue twisters")]/@href'):
        code = href.replace('http://www.uebersetzung.at/twister/', '').replace('.htm', '')
        if code not in {'sk', 'sl', 'xog'}:
            yield href

def parse_language(html):
    xpath = '//h1[contains(text(), "Tongue Twisters")]'
    language = html.xpath(xpath)[0].text_content().strip().replace(' Tongue Twisters', '')
    def _parse_pad(pad):
        original = pad.xpath('p[@class="TXT"]')[0].text_content()
        hrefs = pad.xpath('descendant::a/@href')
        if len(hrefs) == 0 or \
                hrefs[0] == 'http://www.squarewheels.com/content2/copyrightexpl.html':
            translation = None
        else:
            name = hrefs[0].split('#')[1]
            translation = html.xpath('//li[a[@name="%s"]]' % name)[0].text_content()
        return original, translation

    pads = html.xpath('//td[@class="PAD"]')
    return {
        'language': language,
        'tongue_twisters': list(map(_parse_pad, pads))
    }

if __name__ == '__main__':
    main()

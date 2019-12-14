import re
from lxml import etree
import json
from bs4 import BeautifulSoup
from ADC_function import *


def getTitle(a):
    try:
        html = etree.fromstring(a, etree.HTMLParser())
        result = str(html.xpath(
            '/html/body/section/div/h2/strong/text()')).strip(" ['']")
        return re.sub('.*\] ', '', result.replace('/', ',').replace('\\xa0', '').replace(' : ', ''))
    except:
        return re.sub('.*\] ', '', result.replace('/', ',').replace('\\xa0', ''))


def getActor(a):  # //*[@id="center_column"]/div[2]/div[1]/div/table/tbody/tr[1]/td/text()
    # //table/tr[1]/td[1]/text()
    html = etree.fromstring(a, etree.HTMLParser())
    result1 = str(html.xpath(
        '//strong[contains(text(),"演員")]/../following-sibling::span/text()')).strip(" ['']")
    result2 = str(html.xpath(
        '//strong[contains(text(),"演員")]/../following-sibling::span/a/text()')).strip(" ['']")
    return str(result1 + result2).strip('+').replace(",\\xa0", "").replace("'", "").replace(' ', '').replace(',,', '').lstrip(',').replace(',', ', ')


def getStudio(a):
    # //table/tr[1]/td[1]/text()
    html = etree.fromstring(a, etree.HTMLParser())
    result1 = str(html.xpath(
        '//strong[contains(text(),"製作")]/../following-sibling::span/text()')).strip(" ['']")
    result2 = str(html.xpath(
        '//strong[contains(text(),"製作")]/../following-sibling::span/a/text()')).strip(" ['']")
    return str(result1+result2).strip('+').replace("', '", '').replace('"', '')


def getRuntime(a):
    # //table/tr[1]/td[1]/text()
    html = etree.fromstring(a, etree.HTMLParser())
    result1 = str(html.xpath(
        '//strong[contains(text(),"時長")]/../following-sibling::span/text()')).strip(" ['']")
    result2 = str(html.xpath(
        '//strong[contains(text(),"時長")]/../following-sibling::span/a/text()')).strip(" ['']")
    return str(result1 + result2).strip('+').rstrip('mi')


def getLabel(a):
    # //table/tr[1]/td[1]/text()
    html = etree.fromstring(a, etree.HTMLParser())
    result1 = str(html.xpath(
        '//strong[contains(text(),"系列")]/../following-sibling::span/text()')).strip(" ['']")
    result2 = str(html.xpath(
        '//strong[contains(text(),"系列")]/../following-sibling::span/a/text()')).strip(" ['']")
    return str(result1 + result2).strip('+').replace("', '", '').replace('"', '')


def getNum(a):
    html = etree.fromstring(a, etree.HTMLParser())
    result1 = str(html.xpath(
        '//strong[contains(text(),"番號")]/../following-sibling::span/a/text()')).strip(" ['']")
    result2 = str(html.xpath(
        '//strong[contains(text(),"番號")]/../following-sibling::span/text()')).strip(" ['']")
    return str(result1 + result2).strip('+')


def getYear(getRelease):
    try:
        result = str(re.search('\d{4}', getRelease).group())
        return result
    except:
        return getRelease


def getRelease(a):
    # //table/tr[1]/td[1]/text()
    html = etree.fromstring(a, etree.HTMLParser())
    result1 = str(html.xpath(
        '//strong[contains(text(),"時間")]/../following-sibling::span/text()')).strip(" ['']")
    result2 = str(html.xpath(
        '//strong[contains(text(),"時間")]/../following-sibling::span/a/text()')).strip(" ['']")
    return str(result1 + result2).strip('+')


def getTag(a):
    # //table/tr[1]/td[1]/text()
    html = etree.fromstring(a, etree.HTMLParser())
    result1 = str(html.xpath(
        '//strong[contains(text(),"类别")]/../following-sibling::span/text()')).strip(" ['']")
    result2 = str(html.xpath(
        '//strong[contains(text(),"类别")]/../following-sibling::span/a/text()')).strip(" ['']")
    return str(result1 + result2).strip('+').replace(",\\xa0", "").replace("'", "").replace(' ', '').replace(',,', '').lstrip(',')


def getCover(htmlcode):
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath(
        '/html/body/section/div/div[2]/div[1]/a/img/@src')).strip(" ['']")
    if result == '':
        result = str(html.xpath(
            '/html/body/section/div/div[3]/div[1]/a/img/@src')).strip(" ['']")
    return result


def getDirector(a):
    # //table/tr[1]/td[1]/text()
    html = etree.fromstring(a, etree.HTMLParser())
    result1 = str(html.xpath(
        '//strong[contains(text(),"導演")]/../following-sibling::span/text()')).strip(" ['']")
    result2 = str(html.xpath(
        '//strong[contains(text(),"導演")]/../following-sibling::span/a/text()')).strip(" ['']")
    return str(result1 + result2).strip('+').replace("', '", '').replace('"', '')


def getOutline(htmlcode):
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath(
        '//*[@id="introduction"]/dd/p[1]/text()'))
    if result:
        result = result.strip(" ['']")
        return result
    else:
        return ''


def main(number):
    try:
        a = get_html('https://javdb3.com/search?q=' +
                     number + '&f=all').replace(u'\xa0', u' ')
        # //table/tr[1]/td[1]/text()
        html = etree.fromstring(a, etree.HTMLParser())
        # result1 = str(html.xpath(
        #    '//*[@id="videos"]/div/div/a/@href')).strip(" ['']")
        xpath_rules = '//*[@id="videos"]/div/div/a/div[contains(text(),$number)]/parent::a/@href'
        #xpath_rules = xpath_rules.format(number).extract_first()
        # print(xpath_rules)
        result1 = str(html.xpath(xpath_rules, number=number)).strip(" ['']")

        b = get_html('https://javdb3.com' + result1).replace(u'\xa0', u' ')
        dic = {
            'actor': getActor(b),
            'title': getTitle(b).replace("\\n", '').replace('        ', '').replace(getActor(a), '').replace(getNum(a),
                                                                                                             '').replace(
                '无码', '').replace('有码', '').lstrip(' '),
            'studio': getStudio(b),
            'outline': getOutline(b),
            'runtime': getRuntime(b),
            'director': getDirector(b),
            'release': getRelease(b),
            'number': getNum(b),
            'cover': getCover(b),
            'imagecut': 0,
            'tag': getTag(b),
            'label': getLabel(b),
            # str(re.search('\d{4}',getRelease(a)).group()),
            'year': getYear(getRelease(b)),
            'actor_photo': '',
            'website': 'https://javdb3.com' + result1,
            'source': 'javdb.py',
        }
        js = json.dumps(dic, ensure_ascii=False, sort_keys=True,
                        indent=4, separators=(',', ':'), )  # .encode('UTF-8')
        # print(dic)
        return js
    except:
        a = get_html('https://javdb3.com/search?q=' +
                     number + '&f=all').replace(u'\xa0', u' ')
        # //table/tr[1]/td[1]/text()
        html = etree.fromstring(a, etree.HTMLParser())
        result1 = str(html.xpath(
            '//*[@id="videos"]/div/div/a/@href')).strip(" ['']")
        b = get_html('https://javdb3.com' + result1).replace(u'\xa0', u' ')
        dic = {
            'actor': getActor(b),
            'title': getTitle(b).replace("\\n", '').replace('        ', '').replace(getActor(a), '').replace(
                getNum(b),
                '').replace(
                '无码', '').replace('有码', '').lstrip(' '),
            'studio': getStudio(b),
            'outline': getOutline(b),
            'runtime': getRuntime(b),
            'director': getDirector(b),
            'release': getRelease(b),
            'number': getNum(b),
            'cover': getCover(b),
            'imagecut': 0,
            'tag': getTag(b),
            'label': getLabel(b),
            # str(re.search('\d{4}',getRelease(a)).group()),
            'year': getYear(getRelease(b)),
            'actor_photo': '',
            'website': 'https://javdb3.com' + result1,
            'source': 'javdb.py',
        }
        # print(dic)
        js = json.dumps(dic, ensure_ascii=False, sort_keys=True,
                        indent=4, separators=(',', ':'), )  # .encode('UTF-8')
        return js


# if __name__ == "__main__":
#     main('SIRO-2057')
# print(get_html('https://javdb1.com/v/WwZ0Q'))

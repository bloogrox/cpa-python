class Error(Exception):
    pass


class AppstoreImageParserManager(object):

    def __init__(self):
        pass

    def get_image_parser_class(self, platform):
        if platform == 'iOS':
            return ItunesImageParser
        elif platform == 'Android':
            return GoogleImageParser
        else:
            raise Error('Unknown appstore type')


class BaseAppstoreImageUrlParser(object):

    selector = None
    icon_attribute = None

    def __init__(self, page):
        self.page = page

    def get_url(self):
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(self.page)
        result = soup.select(self.selector)

        if len(result):
            return result[0][self.icon_attribute]
        else:
            return None


class ItunesImageParser(BaseAppstoreImageUrlParser):
    selector = '#left-stack div.artwork img'
    icon_attribute = 'src-swap'


class GoogleImageParser(BaseAppstoreImageUrlParser):
    selector = '#body-content div.details-info div.cover-container img.cover-image'
    icon_attribute = 'src'

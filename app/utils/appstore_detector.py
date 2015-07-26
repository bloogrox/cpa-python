ITUNES = 'iTunes'
PLAY_GOOGLE = 'PlayGoogle'


def detect_appstore_type(url):
    """
    >>> detect_appstore_type('https://itunes.apple.com/gb/app/888-poker-texas-holdem-poker/id534130702?mt=8')
    'iTunes'
    >>> detect_appstore_type('https://play.google.com/store/apps/details?id=com.gameinsight.thetribezcastlez')
    'PlayGoogle'
    """
    if 'itunes.apple.com' in url:
        return ITUNES
    elif 'play.google.com' in url:
        return PLAY_GOOGLE
    else:
        return None


if __name__ == "__main__":
    import doctest
    doctest.testmod()

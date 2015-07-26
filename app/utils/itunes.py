def extract_id_from_url(url):
    """
    >>> extract_id_from_url('https://itunes.apple.com/gb/app/888-poker-texas-holdem-poker/id534130702?mt=8')
    '534130702'
    """
    import re

    m = re.search('/id(\d+)', url)

    if m:
        return m.group(1)
    else:
        return None


if __name__ == "__main__":
    import doctest
    doctest.testmod()
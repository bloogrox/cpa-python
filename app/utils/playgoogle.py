def extract_id_from_url(url):
    """
    >>> extract_id_from_url('https://play.google.com/store/apps/details?id=jp.konami.pesclubmanager&hl=.')
    'jp.konami.pesclubmanager'
    """
    from urllib.parse import urlparse, parse_qs

    res = urlparse(url)
    id_ = parse_qs(res.query).get('id', None)

    try:
        return id_[0]
    except:
        return None


if __name__ == "__main__":
    import doctest
    doctest.testmod()
def update_or_create_offer(network, offer):
    """
    :param network: Network object model
    :param offer: dict of importing offer data
    :return:
    """
    from app.models import Offer, OfferEvent
    from app import db

    db_offer = Offer.query.filter_by(network_id=network.id, remote_id=offer['id']).first()

    if db_offer:
        """update"""
        db_offer.name = offer['name'][:128]
        db_offer.preview_url = offer['preview_url'][:512]
        db_offer.payout = float(offer['payout'])
        db_offer.status = Offer.STATUS_ACTIVE

        return db_offer, True
    else:
        """insert"""
        db_offer = Offer()
        db_offer.remote_id = offer['id']
        db_offer.name = offer['name'][:128]
        db_offer.preview_url = offer['preview_url'][:512]
        db_offer.payout = offer['payout']
        db_offer.status = Offer.STATUS_ACTIVE
        db_offer.network = network

        db.session.add(db_offer)

        """create event"""
        offer_event = OfferEvent()
        offer_event.name = OfferEvent.TYPE_NEW
        offer_event.offer = db_offer

        db.session.add(offer_event)

        return db_offer, False


def update_offers_status(network, offers):
    """
    :param network: Network model object
    :param offers: list of dictionaries with importing offer data
    :return:
    """
    from app.models import Offer, OfferEvent
    from app import db

    local_offer_ids = set([offer.remote_id for offer in network.get_active_offers()])
    remote_offer_ids = set([offer['id'] for offer in offers])
    diff = list(local_offer_ids - remote_offer_ids)

    if diff:
    #     # logger.debug('Paused offers %s' % str(diff))
        (Offer.query
         .filter(Offer.remote_id.in_(diff), Offer.network == network)
         .update({Offer.status: Offer.STATUS_STOPPED}, synchronize_session=False))

        """create offer stopped event"""
        for offer_id in diff:
            db_offer = Offer.query.filter_by(network_id=network.id, remote_id=offer_id).first()
            if db_offer:
                offer_event = OfferEvent()
                offer_event.name = OfferEvent.TYPE_STOPPED
                offer_event.offer = db_offer

                db.session.add(offer_event)


def update_offer_countries(offer, new_countries):
    """
    :param offer: Offer model object
    :param new_countries: list of country codes, ex. - ['RU', 'US', 'IT']
    :return:
    """
    from app import db
    from app.models import Country

    current_countries = [c.code for c in offer.countries]

    if set(current_countries) - set(new_countries) or set(new_countries) - set(current_countries):
        # logger.debug('Update countries for offer %s' % offer.ho_id)

        offer.countries = []
        for country_code in new_countries:
            db_country = Country.query.get(country_code)
            if not db_country:
                db_country = Country(code=country_code)
                db.session.add(db_country)
            offer.countries.append(db_country)


def tie_offer_to_app(offer):
    from app import db
    from app.models import App, Platform
    from app.utils.appstore_detector import detect_appstore_type, ITUNES, PLAY_GOOGLE

    appstore_type = detect_appstore_type(offer.preview_url)

    if appstore_type == ITUNES:
        from app.utils.itunes import extract_id_from_url
        app_id = extract_id_from_url(offer.preview_url)
    elif appstore_type == PLAY_GOOGLE:
        from app.utils.playgoogle import extract_id_from_url
        app_id = extract_id_from_url(offer.preview_url)
    else:
        return None

    if app_id:

        platform = Platform.get_by_appstore_type(appstore_type)

        app = App.query.filter(App.app_id == app_id, App.platform == platform).first()

        if not app:
            ### create app
            app = App()
            app.app_id = app_id
            app.platform = platform
            db.session.add(app)

        ### tie to app
        offer.app = app
        db.session.flush()

    else:
        return None
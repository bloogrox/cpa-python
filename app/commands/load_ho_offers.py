from hobuilder2 import Api
from hobuilder2.api import Error
import logging
import time

from app import manager
from app import db
from app.models import Network

from app.utils.offer_loader import update_offer_countries, tie_offer_to_app, update_or_create_offer, update_offers_status


logger = logging.getLogger('cpa')


@manager.command
def load_ho_offers():

    for network in Network.query.filter(Network.tracker == 'hasoffers').all():

        start_time = time.time()

        ######################
        ### request to api ###
        ######################
        try:
            ho = Api(network.api_key, network.network_id, api_type='affiliate', debug=False)

            response_offers = ho.Offer.findAll(contain=['Country'], limit=10000).extract_all()
        except Error as e:
            logger.warning('%s: %s' % (network.name, str(e)))
            continue

        ####################
        ### prepare data ###
        ####################
        offers = []

        for offer in response_offers:

            o = dict()
            o['id'] = int(offer.id)
            o['name'] = offer.name
            if len(offer.Country) and type(offer.Country) == dict:
                o['countries'] = [code for code in list(offer.Country.keys()) if len(code) == 2]
            else:
                o['countries'] = []
            o['payout'] = float(offer.default_payout)
            o['preview_url'] = offer.preview_url

            offers.append(o)

        logger.info('Loaded %s offers: %d' % (network.name, len(offers)))

        #####################
        ### import offers ###
        #####################
        for offer in offers:

            ###########################
            ### add or update offer ###
            ###########################
            db_offer, created = update_or_create_offer(network, offer)

            ########################
            ### update countries ###
            ########################
            if offer['countries']:
                update_offer_countries(db_offer, offer['countries'])
            else:
                db_offer.countries = []

            ##################
            ### tie to App ###
            ##################
            if not db_offer.app:
                tie_offer_to_app(db_offer)

            db.session.commit()

        #############################
        ### detect stopped offers ###
        #############################
        update_offers_status(network, offers)

        db.session.commit()

        complete_time = time.time() - start_time
        logger.info('Finished load %s offers in %ds' % (network.name, int(complete_time)))

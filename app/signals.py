from sqlalchemy import event
from flask.signals import Namespace
from flask.ext.sqlalchemy import models_committed
from sqlalchemy.util.langhelpers import symbol
from app import application, models, db


db_signals = Namespace()

"""
:param sender:
:param instance:
:param operation: insert, update, delete
"""
model_committed = db_signals.signal('model-committed')


@models_committed.connect_via(application)
def on_models_committed(sender, changes):
    for instance, change in changes:
        model_committed.send(instance.__class__, instance=instance, operation=change)


@event.listens_for(models.Offer.payout, 'set')
def create_offer_event_on_payout_changed(target, value, old_value, initiator):
    if old_value != symbol('NO_VALUE'):
        if value != old_value:
            offer_event = models.OfferEvent()
            event_type = models.OfferEvent.TYPE_PAYOUT_UP if value > old_value else models.OfferEvent.TYPE_PAYOUT_DOWN
            offer_event.name = event_type
            offer_event.offer = target
            db.session.add(offer_event)
            db.session.flush()


@event.listens_for(models.Offer.payout, 'set')
def create_offer_payout(target, value, old_value, initiator):
    if value != old_value:
        offer_payout = models.OfferPayout()
        offer_payout.payout = value
        offer_payout.offer = target
        db.session.add(offer_payout)
        db.session.flush()

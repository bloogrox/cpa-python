from marshmallow import fields
from flask_restful import Resource, Api, reqparse
from flask_marshmallow import Marshmallow
from sqlalchemy import desc

from app import application, models


api = Api(application)
ma = Marshmallow(application)


###############
### SCHEMAS ###
###############
class CountrySchema(ma.Schema):
    code = fields.Str(dump_only=True)


class NetworkSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class PlatformSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class AppSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    app_id = fields.Str()
    icon_url = fields.Str()
    platform = fields.Nested(PlatformSchema)


class OfferSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    payout = fields.Float()
    countries = fields.Nested(CountrySchema, many=True)
    network = fields.Nested(NetworkSchema)
    app = fields.Nested(AppSchema)


class AppExtendedSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    app_id = fields.Str()
    icon_url = fields.Str()
    platform = fields.Nested(PlatformSchema)
    offers = fields.Nested(OfferSchema, many=True)


class OfferEventSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    created = fields.DateTime()
    offer = fields.Nested(OfferSchema)


###########
### API ###
###########
class CountryView(Resource):
    def get(self):
        countries = models.Country.query.order_by(models.Country.code).all()
        return CountrySchema(many=True).dump(countries).data


class NetworkView(Resource):
    def get(self):
        networks = models.Network.query.order_by(models.Network.name).all()
        return NetworkSchema(many=True).dump(networks).data


class OfferView(Resource):

    def get(self):

        from app.models import Offer, Platform, Network, Country, App

        parser = reqparse.RequestParser()
        parser.add_argument('offset', type=int)
        parser.add_argument('ordering', type=str)
        parser.add_argument('networks', type=int, action='append')
        parser.add_argument('countries', type=str, action='append')
        parser.add_argument('platform_id', type=int)
        parser.add_argument('app_id', type=int)

        args = parser.parse_args()
        q = Offer.query

        # only Active offers
        q = q.filter(Offer.status == Offer.STATUS_ACTIVE)

        # only mobile offers
        q = q.filter(Offer.app_id.isnot(None))

        ### filter ###
        if args.platform_id:
            q = q.join(Offer.app).join(App.platform).filter(Platform.id == args.platform_id)

        if args.networks:
            q = q.join(Offer.network).filter(Network.id.in_(args.networks))

        if args.countries:
            q = q.join(Offer.countries).filter(Country.code.in_(args.countries))

        if args.app_id:
            q = q.filter(Offer.app_id == args.app_id)

        ### order ###
        if args.ordering:
            if args.ordering == 'new':
                q = q.order_by(desc(Offer.created))
            elif args.ordering == 'max_payout':
                q = q.order_by(desc(Offer.payout))

        ### pagination ###
        if args.offset:
            q = q.offset(args.offset)

        offers = q.limit(20).all()

        return OfferSchema(many=True).dump(offers).data


class EventView(Resource):

    def get(self):

        from app.models import Offer,  Network, Country, OfferEvent

        parser = reqparse.RequestParser()
        parser.add_argument('offset', type=int)
        parser.add_argument('event', type=str)
        parser.add_argument('networks', type=int, action='append')
        parser.add_argument('countries', type=str, action='append')

        args = parser.parse_args()
        q = OfferEvent.query

        # select only mobile offers
        q = q.join(OfferEvent.offer).filter(Offer.app_id.isnot(None))

        q = q.filter(OfferEvent.name != OfferEvent.TYPE_PAYOUT_DOWN)

        ### filter ###
        if args.networks:
            q = q.join(Offer.network).filter(Network.id.in_(args.networks))

        if args.countries:
            q = q.join(Offer.countries).filter(Country.code.in_(args.countries))

        if args.event:
            q = q.filter(OfferEvent.name == args.event)

        ### order ###
        q = q.order_by(desc(OfferEvent.created))

        ### pagination ###
        if args.offset:
            q = q.offset(args.offset)

        events = q.limit(20).all()

        return OfferEventSchema(many=True).dump(events).data


class EventCounterView(Resource):

    def get(self):

        from app.models import OfferEvent, Offer

        import pytz
        import datetime

        msk = pytz.timezone('Europe/Moscow')

        start_date = datetime.datetime.now(tz=msk)
        end_date = datetime.datetime.now(tz=msk)

        start_date = datetime.datetime.combine(start_date.date(), datetime.time.min)
        end_date = datetime.datetime.combine(end_date.date(), datetime.time.max)

        return (OfferEvent.query
                .join(OfferEvent.offer).filter(Offer.app_id.isnot(None))
                .filter(OfferEvent.name == OfferEvent.TYPE_NEW,
                        OfferEvent.created >= start_date,
                        OfferEvent.created <= end_date)
                .count())


class AppView(Resource):

    def get(self, id):

        from app.models import App

        app = App.query.get(id)

        return AppSchema(many=False).dump(app).data


class AppsView(Resource):

    def get(self):

        from app import models as m

        parser = reqparse.RequestParser()
        parser.add_argument('offset', type=int)
        parser.add_argument('platform_id', type=int)

        args = parser.parse_args()

        q = m.App.query

        ### filter ###
        if args.platform_id:
            q = q.join(m.App.platform).filter(m.Platform.id == args.platform_id)

        q = q.order_by(desc(m.App.id))

        if args.offset:
            q = q.offset(args.offset)

        apps = q.limit(20).all()

        return AppExtendedSchema(many=True).dump(apps).data


############
### URLS ###
############
api.add_resource(CountryView, '/api/countries/')
api.add_resource(NetworkView, '/api/networks/')
api.add_resource(OfferView, '/api/offers/')
api.add_resource(EventView, '/api/events/')
api.add_resource(AppView, '/api/apps/<int:id>/')
api.add_resource(AppsView, '/api/apps/')
api.add_resource(EventCounterView, '/api/events/new_offers_count/')

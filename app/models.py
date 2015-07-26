#################
#### models #####
#################
import datetime

from app import db


class User(db.Model):

    TYPES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    login = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __repr__(self):
        return '<User %r>' % self.nickname

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(120))
    text = db.Column(db.UnicodeText, nullable=False)


class Network(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    api_key = db.Column(db.String(64))
    network_id = db.Column(db.String(64))
    tracker = db.Column(db.String(30))

    def __repr__(self):
        return '<Network %r>' % self.name

    def __str__(self):
        return self.name

    def get_active_offers(self):
        return Offer.query.filter(Offer.network == self, Offer.status == Offer.STATUS_ACTIVE)

    def get_stopped_offers(self):
        return Offer.query.filter(Offer.network == self, Offer.status == Offer.STATUS_STOPPED)

    def get_offer_by_remote_id(self, remote_id):
        return Offer.query.filter_by(network=self, remote_id=remote_id).first()


class Country(db.Model):

    code = db.Column(db.String(2), primary_key=True)

    def __repr__(self):
        return '<Country %r>' % self.code


offer_countries = db.Table('offer_countries',
    db.Column('offer_id', db.Integer, db.ForeignKey('offer.id'), index=True),
    db.Column('country_code', db.String, db.ForeignKey('country.code'), index=True),

    db.UniqueConstraint('offer_id', 'country_code', name='_offer_id_country_code_uc')
)


class Offer(db.Model):

    STATUS_ACTIVE = 'active'
    STATUS_STOPPED = 'stopped'

    id = db.Column(db.Integer, primary_key=True)
    remote_id = db.Column(db.Integer)
    name = db.Column(db.String(128))
    preview_url = db.Column(db.String(512))
    payout = db.Column(db.Float(2))
    # todo переделать на enum
    status = db.Column(db.String(10), default=STATUS_ACTIVE, index=True)
    created = db.Column(db.DateTime(), default=datetime.datetime.utcnow())

    network_id = db.Column(db.Integer, db.ForeignKey('network.id'))
    network = db.relationship('Network', backref=db.backref('offers', lazy='dynamic'))

    app_id = db.Column(db.Integer, db.ForeignKey('app.id'), nullable=True)
    app = db.relationship('App', backref=db.backref('offers', lazy='dynamic'))

    countries = db.relationship('Country', secondary=offer_countries, backref=db.backref('offers', lazy='dynamic'))

    __table_args__ = (db.UniqueConstraint('remote_id', 'network_id', name='_remote_id_network_id_uc'),)

    def __repr__(self):
        return '<Offer %r>' % self.name


class OfferEvent(db.Model):

    TYPE_NEW = 'new'
    TYPE_STOPPED = 'stopped'
    TYPE_PAYOUT_UP = 'payout_up'
    TYPE_PAYOUT_DOWN = 'payout_down'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), index=True)
    created = db.Column(db.DateTime(), default=datetime.datetime.utcnow())

    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'))
    offer = db.relationship('Offer', backref=db.backref('events', lazy='dynamic'))

    def __repr__(self):
        return '<OfferEvent %r>' % self.name


class OfferPayout(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    payout = db.Column(db.Float(2))
    created = db.Column(db.DateTime(), default=datetime.datetime.utcnow())

    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'))
    offer = db.relationship('Offer', backref=db.backref('payouts', lazy='dynamic'))

    def __repr__(self):
        return '<OfferPayout %r>' % self.payout


class App(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.String(64), index=True, nullable=False)
    icon_url = db.Column(db.String(512), nullable=True)

    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'), nullable=False)
    platform = db.relationship('Platform', backref=db.backref('apps', lazy='dynamic'))

    __table_args__ = (db.UniqueConstraint('app_id', 'platform_id', name='_app_id_platform_id_uc'),)

    def __repr__(self):
        return '<App %r>' % self.id


class Platform(db.Model):

    TYPE_IOS = 'iOS'
    TYPE_ANDROID = 'Android'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(TYPE_IOS, TYPE_ANDROID, name='platform_types'), unique=True)

    def __repr__(self):
        return '<Platform %r>' % self.name

    @staticmethod
    def get_by_appstore_type(appstore_type):
        from app.utils.appstore_detector import ITUNES, PLAY_GOOGLE

        if appstore_type == ITUNES:
            return Platform.query.filter_by(name=Platform.TYPE_IOS).first()
        elif appstore_type == PLAY_GOOGLE:
            return Platform.query.filter_by(name=Platform.TYPE_ANDROID).first()
        else:
            return None

import requests

from app import manager, models, db
from app.utils.appstore_thumbnail import AppstoreImageParserManager


@manager.command
def load_app_icons():

    apps = models.App.query.filter(models.App.icon_url == None).all()

    for app in apps:
        offer = app.offers.first()
        if offer:
            try:
                page = requests.get(offer.preview_url).text
                parser = AppstoreImageParserManager().get_image_parser_class(app.platform.name)
                icon_url = parser(page).get_url()
                if icon_url:
                    app.icon_url = icon_url
                    db.session.commit()
            except Exception as e:
                print(str(e))

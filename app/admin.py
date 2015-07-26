#################
####  admin  ####
#################
from flask import url_for, redirect, request
from flask.ext.admin import Admin, AdminIndexView
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext import login
from wtforms import form, fields, validators
from flask.ext.admin import helpers, expose
from werkzeug.security import generate_password_hash, check_password_hash

from app import application, db
from app import models


#############
### LOGIN ###
#############

# Initialize flask-login
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(application)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(models.User).get(user_id)


class MyModelView(ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated()


# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(models.User).filter_by(login=self.login.data).first()


# Create customized index view class that handles login & registration
class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated():
            return redirect(url_for('.index'))

        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()


    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


####################
### admin models ###
####################
class UserAdmin(MyModelView):
    column_filters = ('nickname',)


class NetworkAdmin(MyModelView):
    form_excluded_columns = ('offers',)


class OfferAdmin(MyModelView):
    form_excluded_columns = ('events',)
    column_list = ('id', 'remote_id', 'name', 'network', 'payout', 'status',)
    column_exclude_list = ('network',)


class CountryAdmin(MyModelView):
    column_list = ('code',)
    form_excluded_columns = ('offers',)
    can_edit = False


class AppAdmin(MyModelView):
    form_excluded_columns = ('offers',)
    column_list = ('id', 'platform', 'app_id', 'icon_url',)
    column_sortable_list = ('id', 'app_id', 'icon_url',)


init_login()


admin = Admin(application, index_view=MyAdminIndexView(), base_template='my_master.html')


admin.add_view(MyModelView(models.Post, db.session))
admin.add_view(UserAdmin(models.User, db.session))
admin.add_view(NetworkAdmin(models.Network, db.session))
admin.add_view(OfferAdmin(models.Offer, db.session))
admin.add_view(MyModelView(models.OfferEvent, db.session))
admin.add_view(CountryAdmin(models.Country, db.session))
admin.add_view(MyModelView(models.Platform, db.session))
admin.add_view(AppAdmin(models.App, db.session))
admin.add_view(MyModelView(models.OfferPayout, db.session))
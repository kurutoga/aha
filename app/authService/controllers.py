from flask import Flask, render_template
from flask_security import Security, SQLAlchemyUserDatastore, utils, current_user, login_required, UserMixin, RoleMixin
from app.authService.models import *
from app.authService.forms import *
from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from wtforms.fields import PasswordField


from app import db, app

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=AHARegisterForm)

# Customized User model for SQL-Admin
class UserAdmin(sqla.ModelView):

    # Don't display the password on the list of Users
    column_exclude_list = ('password',)

    # Don't include the standard password field when creating or editing a User (but see below)
    form_excluded_columns = ('password',)

    # Automatically display human-readable names for the current and available Roles when creating or editing a User
    column_auto_select_related = True

    # Prevent administration of Users unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')

    # On the form for creating or editing a User, don't display a field corresponding to the model's password field.
    # There are two reasons for this. First, we want to encrypt the password before storing in the database. Second,
    # we want to use a password field (with the input masked) rather than a regular text field.
    def scaffold_form(self):

        # Start with the standard form as provided by Flask-Admin. We've already told Flask-Admin to exclude the
        # password field from this form.
        form_class = super(UserAdmin, self).scaffold_form()

        # Add a password field, naming it "password2" and labeling it "New Password".
        form_class.password2 = PasswordField('New Password')
        return form_class

    # This callback executes when the user saves changes to a newly-created or edited User -- before the changes are
    # committed to the database.
    def on_model_change(self, form, model, is_created):

        # If the password field isn't blank...
        if len(model.password2):

            # ... then encrypt the new password prior to storing it in the database. If the password field is blank,
            # the existing password in the database will be retained.
            model.password = utils.encrypt_password(model.password2)


# Customized Role model for SQL-Admin
class RoleAdmin(sqla.ModelView):

    # Prevent administration of Roles unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')

# Initialize Flask-Admin
admin = Admin(app)

# Add Flask-Admin views for Users and Roles
admin.add_view(UserAdmin(User, db.session))
admin.add_view(RoleAdmin(Role, db.session))


#@app.before_first_request
#    user_datastore.create_user(email='bishudash@gmail.com', password='password')
#    db.session.commit()

#@security.context_processor
#def security_context_processor():
#    return dict(
#        admin_base_template=admin.base_template,
#        admin_view=admin.index_view,
#        h=admin_helpers,
#        get_url=url_for
#    )

# Executes before the first request is processed.
@app.before_first_request
def before_first_request():

    # Create any database tables that don't exist yet.
    db.create_all()

    # Create the Roles "admin" and "end-user" -- unless they already exist
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='end-user', description='End user')

    # Create two Users for testing purposes -- unless they already exists.
    # In each case, use Flask-Security utility function to encrypt the password.
    encrypted_password = utils.encrypt_password('password')
    en = 'user@wsu.edu'
    ad = 'admin@wsu.edu'
    if not user_datastore.get_user(en):
        user_datastore.create_user(email=en, password=encrypted_password, name='Test User')
        user_datastore.add_role_to_user(en, 'end-user')
    if not user_datastore.get_user(ad):
        user_datastore.create_user(email=ad, password=encrypted_password, name='Test Admin')
        user_datastore.add_role_to_user(ad, 'admin')

    # Commit any database changes; the User and Roles must exist before we can add a Role to the User
    db.session.commit()


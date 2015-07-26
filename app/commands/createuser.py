from app import manager, models, db
from werkzeug.security import generate_password_hash


@manager.command
def createuser(username, password):

    user = models.User()
    user.login = username
    user.password = generate_password_hash(password)

    db.session.add(user)
    db.session.commit()

    print('User created.')
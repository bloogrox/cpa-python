from app import manager


##################
### migrations ###
##################
from flask.ext.migrate import Migrate, MigrateCommand
from app import application, db
migrate = Migrate(application, db)
manager.add_command('db', MigrateCommand)


################
### commands ###
################
from app import commands


if __name__ == '__main__':
    manager.run()
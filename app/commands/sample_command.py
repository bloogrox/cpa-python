from app import manager


@manager.command
def sample_command():
    print('Running sample command')
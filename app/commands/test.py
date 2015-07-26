import unittest

from app import manager
from app.config import BASE_DIR


@manager.command
def test():
    tests = unittest.TestLoader().discover(BASE_DIR)
    unittest.TextTestRunner(verbosity=2).run(tests)
    print(BASE_DIR)
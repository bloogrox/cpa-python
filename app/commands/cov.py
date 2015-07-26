import os
import unittest
import coverage

from app import manager
from app.config import BASE_DIR


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    cov = coverage.coverage(
        branch=True,
        include='app/*'
    )
    cov.start()
    tests = unittest.TestLoader().discover(BASE_DIR)
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print('Coverage Summary:')
    cov.report()
    covdir = os.path.join(BASE_DIR, '..', 'coverage')
    cov.html_report(directory=covdir)
    cov.erase()
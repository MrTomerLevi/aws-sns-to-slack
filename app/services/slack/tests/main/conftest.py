import os


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    os.environ['SLACK_HOOK_URL'] = ''


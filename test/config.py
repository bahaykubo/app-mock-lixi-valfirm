import os


def hostname():
    if os.environ.get('appenv') == 'local':
        return 'http://localhost:8000'
    return 'https://lixi-mock-valfirm-service.azurewebsites.net'

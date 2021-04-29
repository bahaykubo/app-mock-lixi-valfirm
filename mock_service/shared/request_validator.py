def is_authorized(request):
    if 'authorization' in request.headers and request.headers['authorization'].startswith('Bearer'):
        return True
    return False

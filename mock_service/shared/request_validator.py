def is_authorized(request_headers):
    if 'authorization' in request_headers and request_headers['authorization'].startswith('Bearer'):
        return True
    return False

import random
import string
import json


def generate_token_dictionary():
    dummy_token = dict()
    dummy_token['access_token'] = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(500))
    dummy_token['token_type'] = 'Bearer'
    dummy_token['expires_in'] = 86400
    return json.dumps(dummy_token)

def authorized(username, password):
    if all(input is None for input in [username, password]):
        raise ValueError('no username and password provided')
    elif any(input is None for input in [username, password]):
        raise ValueError('no username or password provided')
    elif username == '1platform' and password == '1platform':
        result = True
    else:
        result = False
    return result

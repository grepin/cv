from jwt import decode


def get_redis_token_key(token_data: dict):
    return "{}:{}".format(token_data['id'], token_data['jti'])


def get_token_data(token: str, key: str):
    return decode(token, key, algorithms="HS256")


def get_auth_header(token: str):
    return {'Authorization': 'Bearer ' + token}



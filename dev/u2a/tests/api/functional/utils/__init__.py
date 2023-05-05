def get_cache_key(
    function_name: str,
    kwargs: dict,
    subscription: int = 0
):
    cache_key = function_name + "=" + str(subscription)
    for k, v in kwargs.items():
        cache_key += "::" + str(k) + "::" + str(v)
    return cache_key
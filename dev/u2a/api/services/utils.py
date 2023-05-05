
class SubscriptionLevels:
    NO_SUBSCRIPTION = 0
    STANDARD_SUBSCRIPTION = 1


def roles2subscription(roles: list):
    if roles is None:
        return SubscriptionLevels.NO_SUBSCRIPTION
    if 'user' in roles:
        return SubscriptionLevels.STANDARD_SUBSCRIPTION
    return SubscriptionLevels.NO_SUBSCRIPTION

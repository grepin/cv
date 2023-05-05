USER = {
    "login": "adam",
    "email": "adam@mankind.com",
    "password": "adam1man",
    "name": "adam",
    "lastname": "firstman"
}
ROLE = {
    "name": "tester",
}

SUFFICIENT_ROLES_WITH_USER_FOR_LIST = [
    ('administrator', USER),
    ('editor', USER)
]

SUFFICIENT_ROLES_WITH_USER_FOR_GRANT = [
    ('administrator', 'subscriber', USER),
    ('editor', 'subscriber', USER)
]
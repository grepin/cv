import json
import random
from datetime import date
from copy import deepcopy

base = 'data.json'
records_modified = 10  # up to 992
records_new = 10


def string_part(s: str, date_stamp: str) -> str:
    left = random.randint(0, min(len(s), 20))
    right = random.randint(left, min(left + 20, len(s)))
    return 'mod@' + date_stamp + ' = [' + s[left:right] + ']'


def modify(record: dict, date_stamp: str, identifier_postfix: str = '') -> None:
    record['modified'] = date_stamp
    record['identifier'] += identifier_postfix
    record['description'] = string_part(record['description'], date_stamp)
    record['title'] = string_part(record['title'], date_stamp)
    record['license'] = string_part(record['license'], date_stamp)
    record['publisher']['name'] = string_part(record['publisher']['name'], date_stamp)
    record['distribution'][0]['accessURL'] = string_part(record['distribution'][0]['accessURL'], date_stamp)
    record['keyword'].append('mod@' + date_stamp)


for ds in ['2023-05-22']:
    with open(base, "r") as fp:
        js = json.load(fp)
    new_base = deepcopy(js['dataset'][0])
    for i in range(records_new):
        new_one = deepcopy(new_base)
        modify(new_one, ds, identifier_postfix='-' + ds + '-' + str(i))
        js['dataset'].append(new_one)
    for i in range(records_modified):
        modify(js['dataset'][i], ds)
    with open(ds + '.' + base, "w") as fp:
        json.dump(js, fp)

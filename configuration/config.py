import re
import yaml


def check(string, text):
    return bool(re.search(string, text))


def load_yaml(self):
    with open(self, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_value(self, index):
    data = load_yaml(self)
    value = list(data[index].values())[0][0]
    return list(value.values())[0]


def name(self):
    return get_value(self, 0)


def method(self):
    return get_value(self, 1)


def urlpath(self):
    return get_value(self, 2)


def payload(self):
    return get_value(self, 3)


def status(self):
    return int(get_value(self, 4))


def word(self):
    return get_value(self, 5)[0]


def method_v(self):
    return get_value(self, 6)


def verify(self):
    return get_value(self, 7)


def command(self):
    return get_value(self, 8)


def searchip(self):
    return bool(re.search("<IP>", payload(self)))


def searchdns(self):
    return bool(re.search("<DNS>", payload(self)))



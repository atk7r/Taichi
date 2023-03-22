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


def method(self):
    return get_value(self, 0)


def payload(self):
    data = load_yaml(self)[1]
    value = list(data.values())[0]
    dict_payload = {}
    for i in value:
        dict_payload.update(i)
    return dict_payload


def word(self):
    return get_value(self, 2)[0]


def url(self):
    return get_value(self, 3)


def method_v(self):
    return get_value(self, 4)


def verify(self):
    return get_value(self, 5)

# a = method("poc.yaml")
# b = payload("poc.yaml")
# c = word("poc.yaml")
# d = url("poc.yaml")
# e = method_v("poc1.yaml")
# f = verify("poc1.yaml")
#
# print(a)
# print(b)
# print(c)
# print(d)
# print(e)
# print(f)

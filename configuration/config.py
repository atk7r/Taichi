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


def type(self):
    return get_value(self, 0)


def method(self):
    return get_value(self, 1)


def payload(self):
    data = load_yaml(self)[2]
    value = list(data.values())[0]
    dict_payload = {}
    for i in value:
        dict_payload.update(i)
    return dict_payload


def word(self):
    return get_value(self, 3)[0]


def url(self):
    return get_value(self, 4)


def method_v(self):
    return get_value(self, 5)


def verify(self):
    return get_value(self, 6)


# x = type("exp.yaml")
# a = method("exp.yaml")
# b = payload("exp.yaml")
# c = word("exp.yaml")
# d = url("exp.yaml")
# e = method_v("exp.yaml")
# f = verify("exp.yaml")
#
# print(x)
# print(a)
# print(b)
# print(c)
# print(d)
# print(e)
# print(f)

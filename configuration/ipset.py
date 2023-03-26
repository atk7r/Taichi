from configuration.config import payload


def ldap_payload(poc):
    ip = "192.168.0.1"  # 你的 ldap ip(不需要端口)
    old = payload(poc)
    new = old.replace("<IP>", ip)
    return new


def dnslog_payload(poc):
    ip = "192.168.0.1"  # 你的 dnslog ip
    old = payload(poc)
    new = old.replace("<DNS>", ip)
    return new

# ldap_payload("C:\\Users\\CCJ\\Desktop\\Taichi-main\\pocs\\seeyou\\SeeyouOA_Fastjson_Deserialization.yaml")
# dnslog_payload("C:\\Users\\CCJ\\Desktop\\Taichi-main\\pocs\\LandrayOA\\LandrayOA_treexml_rce.yaml")

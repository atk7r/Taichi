import http.client
from configuration.config import searchip, searchdns, urlpath, verify
from configuration.head import header, cmd_header
from configuration.ipset import ldap_payload, dnslog_payload


def send_request(host, method, urlpath, payload, command, poc, verify_method, verify_urlpath):
    global response
    conn = http.client.HTTPConnection(host, timeout=5)
    if payload == "isNone":
        conn.request(method, url=urlpath, headers=header(host))
        response = conn.getresponse()

    elif payload != "isNone":
        if command == "isNone":
            conn.request(method, url=urlpath, body=payload, headers=header(host))
            response = conn.getresponse()
        elif command != "isNone":
                if searchip(poc):
                    conn.request(method, url=urlpath, body=ldap_payload(poc), headers=cmd_header(host, poc))
                    response = conn.getresponse()

                elif searchdns(poc):
                    conn.request(method, url=urlpath, body=dnslog_payload(poc), headers=cmd_header(host, poc))
                    response = conn.getresponse()

                else:
                    conn.request(method, url=urlpath, body=payload, headers=cmd_header(host,poc))
        else:
            print("Data Exception")
    else:
        print("Data Exception")


    # 二次访问判断
    if verify_method == "isNone":
        pass
    else:
        if verify_method != "None":
            conn.request(verify_method, url=verify_urlpath, headers=header(host))
            response = conn.getresponse()
        else:
            print("Data Exception")

    return response

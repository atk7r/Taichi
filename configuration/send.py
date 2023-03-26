from configuration.config import searchip, searchdns
from configuration.head import header, cmd_header
from configuration.ipset import ldap_payload, dnslog_payload


def send_request(session, payload, method, httpline, command, poc, verify_method, verify_url):
    if payload == "isNone":
        if method == "post":
            response = session.post(url=httpline, headers=header(httpline), verify=False, timeout=5)
        elif method == "get":
            response = session.get(url=httpline, headers=header(httpline), verify=False, timeout=5)
        else:
            print("Data Exception")

    elif payload != "isNone":
        if command == "isNone":
            if method == "post":
                response = session.post(url=httpline, data=payload, headers=header(httpline), verify=False, timeout=5)
            elif method == "get":
                response = session.get(url=httpline, params=payload, headers=header(httpline), verify=False, timeout=5)
            else:
                print("Data Exception")
        else:
            if command != "isNone":
                if searchip(poc):
                    if method == "post":
                        response = session.post(url=httpline, data=ldap_payload(poc), headers=cmd_header(httpline, poc), verify=False, timeout=5)
                    else:
                        print("Data Exception")
                    # elif method == "get":
                    #     response = session.get(url=httpline, params=ldap_payload, headers=header(httpline), verify=False, timeout=5)
                elif searchdns(poc):
                    if method == "post":
                        response = session.post(url=httpline, data=dnslog_payload(poc), headers=header(httpline), verify=False, timeout=5)
                    else:
                        print("Data Exception")
                else:
                    if method == "post":
                        response = session.post(url=httpline, data=payload, headers=cmd_header(httpline, poc), verify=False, timeout=5)
                    else:
                        print("Data Exception")



    # 二次访问判断
    if verify_method == "isNone":
        pass
    else:
        if verify_method != "None":
            httpline_verify = httpline + verify_url
            if verify_method == "post":
                response = session.post(url=httpline_verify, headers=header(httpline), verify=False, timeout=5)
            elif verify_method == "get":
                response = session.get(url=httpline_verify, headers=header(httpline), verify=False, timeout=5)
            else:
                print("Data Exception")

    return response

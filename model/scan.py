import threading
import requests
import urllib3
import configuration
from configuration import agent, color


def scan_one(rhost, poc=None, outfile=None):
    httpline = "http://" + rhost
    headers = {"Referer": httpline,
               "User-Agent": agent.random_ua(),
               "Content-Type": "application/x-www-form-urlencoded",
               "Accept-Encoding": "gzip",
               }

    try:
        urllib3.disable_warnings()
        with requests.Session() as session:
            httpline_req = httpline + configuration.config.url(poc)

            if configuration.config.payload(poc) == {'isNone': 'isNone'}:

                if configuration.config.method(poc) == "post":
                    session.post(url=httpline_req, headers=headers, verify=False, timeout=5)
                    response = session.post(url=httpline_req, headers=headers, verify=False, timeout=5)


                elif configuration.config.method(poc) == "get":
                    session.get(url=httpline, headers=headers, verify=False, timeout=5)
                    response = session.post(url=httpline_req, headers=headers, verify=False, timeout=5)
            else:
                payload = configuration.config.payload(poc)

                if configuration.config.method(poc) == "post":
                    session.post(url=httpline_req, data=payload, headers=headers, verify=False, timeout=5)
                    response = session.post(url=httpline_req, data=payload, headers=headers, verify=False, timeout=5)


                elif configuration.config.method(poc) == "get":
                    session.get(url=httpline, data=payload, headers=headers, verify=False, timeout=5)
                    response = session.post(url=httpline_req, data=payload, headers=headers, verify=False, timeout=5)

        if response.status_code == 200:
            resp_text = response.text
            result = configuration.config.check(configuration.config.word(poc), resp_text)
            if result:
                print(configuration.color.vuln(httpline_req))
                if outfile is not None:
                    with open(outfile, "a") as f:
                        f.writelines(httpline_req + "\n")
            else:
                print(configuration.color.not_vuln(httpline_req))
        else:
            print(configuration.color.not_vuln(httpline_req))
    except:
        print(configuration.color.error(httpline_req))


def scan_all(file, poc=None, outfile=None):
    for line in file:
        rhost = line.strip()
        scan_one(rhost, poc, outfile)


def scan_all_threads(file, poc=None, thread_num=None, outfile=None):
    if thread_num is not None:
        threads = []
        for i in range(thread_num):
            t = threading.Thread(target=scan_all, args=(file, poc, outfile))
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()

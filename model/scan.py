import threading
import requests
import urllib3
import config
import config.color
import config.agent
from config import agent, color


def scan_one(rhost, poc=None, outfile=None):

    httpline = "https://" + rhost
    headers = {"Referer": httpline,
               "User-Agent": agent.random_ua(),
               "Content-Type": "application/x-www-form-urlencoded",
               "Accept-Encoding": "gzip",
               }

    try:
        urllib3.disable_warnings()

        httpline_req = httpline + config.url(poc)
        payload = config.payload(poc)

        if config.method(poc) == "post":
            requests.post(url=httpline_req, data=payload, headers=headers, verify=False, timeout=5)
            response = requests.post(url=httpline_req, data=payload, headers=headers, verify=False, timeout=5)


        elif config.method(poc) == "get":
            requests.get(url=httpline, params=payload, headers=headers, verify=False, timeout=5)
            response = requests.post(url=httpline_req, params=payload, headers=headers, verify=False, timeout=5)

        if response.status_code == 200:
            resp_text = response.text
            result = config.check(config.word(poc), resp_text)
            if result:
                print(color.vuln(httpline_req))
                if outfile is not None:
                    with open(outfile, "a") as f:
                        f.writelines(httpline_req + "\n")
            else:
                print(color.not_vuln(httpline_req))
        else:
            print(color.not_vuln(httpline_req))
    except:
        print(color.error(httpline_req))


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
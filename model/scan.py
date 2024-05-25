import threading
import requests
import configuration
from configuration import color
from configuration.color import pocname
import configuration.final_result
from configuration.send import send_request


def scan_one(rhost, poc=None, outfile=None):
    host = rhost
    httpline = "http://" + host
    command = configuration.config.command(poc)
    method = configuration.config.method(poc)
    urlpath = configuration.config.urlpath(poc)
    payload = configuration.config.payload(poc)
    verify_method = configuration.config.method_v(poc)
    verify_urlpath = configuration.config.verify(poc)

    try:

        # 发送请求
        resp = send_request(host, method, urlpath, payload, command, poc, verify_method, verify_urlpath)

        # 输出结果

        configuration.final_result.result(resp, poc, httpline, urlpath, outfile)

    except:
        print(configuration.color.error(httpline+urlpath) + pocname(poc))


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

import threading
import requests
import configuration
from configuration import color
from configuration.color import pocname
import configuration.final_result
from configuration.send import send_request


def scan_one(rhost, poc=None, outfile=None):
    httpline = rhost
    # try:
    with requests.Session() as session:
        command = configuration.config.command(poc)
        method = configuration.config.method(poc)
        httpline_req = httpline + configuration.config.url(poc)
        payload = configuration.config.payload(poc)
        verify_method = configuration.config.method_v(poc)
        verify_url = configuration.config.verify(poc)

        # 发送请求
        response = send_request(session, payload, method, httpline, command, poc, verify_method, verify_url)

        # 输出结果

        configuration.final_result.result(response, poc, httpline_req, outfile)




    # except:
    #     print(configuration.color.error(httpline_req) + pocname(poc))


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

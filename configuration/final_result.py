from configuration.color import pocname
import configuration
from configuration.config import status


def result(response, poc, httpline_req, outfile):
    if response.status_code == status(poc):
        resp_text = response.text
        res = configuration.config.check(configuration.config.word(poc), resp_text)
        if res:
            print(configuration.color.vuln(httpline_req) + pocname(poc))
            if outfile is not None:
                with open(outfile, "a") as f:
                    f.writelines(httpline_req + "\n")
        else:
            print(configuration.color.not_vuln(httpline_req) + pocname(poc))
    else:
        print(configuration.color.not_vuln(httpline_req) + pocname(poc))


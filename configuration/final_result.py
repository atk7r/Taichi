import gzip
from io import BytesIO

from configuration.color import pocname
import configuration
from configuration.config import status


def result(resp, poc, httpline,urlpath, outfile):
    if status(poc) == resp.status:
        if 'Content-Encoding' in resp.headers and resp.headers['Content-Encoding'] == 'gzip':
            buf = BytesIO(resp.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read().decode('utf-8')
        else:
            data = resp.read().decode('utf-8')

        res = configuration.config.check(configuration.config.word(poc), data)
        if res:
            print(configuration.color.vuln(httpline+urlpath) + pocname(poc))
            if outfile is not None:
                with open(outfile, "a") as f:
                    f.writelines(httpline+urlpath + "\n")
        else:
            print(configuration.color.not_vuln(httpline+urlpath) + pocname(poc))
    else:
        print(configuration.color.not_vuln(httpline+urlpath) + pocname(poc))


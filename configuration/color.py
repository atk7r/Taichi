from configuration.config import name

yellow = "\033[33m"
green = "\033[32m"
red = "\033[31m"
end = "\033[0m"


def vuln(self):
    vuln_color = "\033[33m[+]\033[0m" + "\033[33m{}\033[0m".format(self) + "\033[33m is vulnerable! \033[0m"
    return vuln_color


def not_vuln(self):
    not_vuln_color = "\033[32m[-]\033[0m" + "\033[32m{}\033[0m".format(self) + "\033[32m not vulnerable.\033[0m"
    return not_vuln_color


def error(self):
    error_color = "\033[31m[x]\033[0m" + "\033[31m{}\033[0m".format(self) + "\033[31m error \033[0m"
    return error_color


def success(self):
    success_color = "\033[33m[+]\033[0m" + "\033[33m{}\033[0m".format(self) + "\033[33m attack successful! \033[0m"
    return success_color


def failed(self):
    failed_color = "\033[32m[-]\033[0m" + "\033[33m{}\033[0m".format(self) + "\033[32m attack failed. \033[0m"
    return failed_color


def pocname(self):
    name_color = "\033[34m[Poc: \033[0m" + "\033[34m{}\033[0m".format(name(self)) + "\033[34m]\033[0m"
    return name_color

from configuration import agent
from configuration.config import command


def header(self):
    general_headers = {"Referer": self,
                       "User-Agent": agent.random_ua(),
                       "Content-Type": "application/x-www-form-urlencoded",
                       "Accept-Encoding": "gzip",
                       }
    return general_headers


def cmd_header(self, poc):
    cmd_headers = {"Referer": self,
                   "User-Agent": agent.random_ua(),
                   "Content-Type": "application/x-www-form-urlencoded",
                   "Accept-Encoding": "gzip",
                   "cmd": command(poc)
                   }
    return cmd_headers

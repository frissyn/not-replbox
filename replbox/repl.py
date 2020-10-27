import os
import json
import urllib
import requests
import datetime

from .util import mainf
from .util import ensure_json

from .errors import APIError


def is_file(name):
    if len(name.split(".")) <= 1:
        return False
    else:
        return True


def get_repl_action(id, fileN, dateObj, action, cookies=None):
    r = requests.get(
        f"https://repl.it/data/repls/signed_urls/{id}/{fileN}?d={dateObj}",
        cookies=cookies,
    ).json()

    ensure_json(r)

    try:
        return r["urls_by_action"][action]
    except KeyError:
        raise APIError(
            "PermissionError",
            f"You don't have permission to perform action: ({action})",
            403,
        )


class Repl(object):
    def __init__(self, replObj, token):
        self.cur = replObj
        self.token = token
        self.mainF = mainf(replObj["fileNames"], replObj["language"])

        self.set_attributes(self.cur)
        self.__setattr__("json", self.cur)

    def __str__(self):
        return f"Repl(id:{self.cur['id']}, lang:{self.cur['language']})"

    def __getattribute__(self, name):
        return super(Repl, self).__getattribute__(name)

    def set_attributes(self, attrs):
        for attr, value in attrs.items():
            self.__setattr__(attr, value)

    def read(self, fileN):
        url = get_repl_action(
            self.cur["id"],
            urllib.parse.quote_plus(fileN),
            datetime.datetime.now(),
            "read",
        )

        content = requests.get(url).text

        return content

    def read_main(self):
        return self.read(self.mainF)

    def dump(self, fileN, fp):
        fp.write(self.read(fileN))

    def ensure_path(self, path):
        fofs = str(path).split("/")

        for inx, fof in enumerate(fofs):
            if fof:
                if is_file(fof) and fof == fofs[-1]:
                    dirs = path[0 : len(path) - len(fof)]
                    try:
                        os.makedirs(dirs, mode=0o777)
                    except FileExistsError:
                        pass
                else:
                    pass
            else:
                pass

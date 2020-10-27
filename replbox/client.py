import bs4
import json
import requests

from .repl import Repl

from .errors import LoginError

from .util import update_dict
from .util import ensure_json
from .util import confirm_login
from .util import fetch_pot_token


class Client(object):
    def __init__(self):
        pass

    def __getattribute__(self, name):
        return super(Client, self).__getattribute__(name)

    def login(self, sid):
        cookie = {"connect.sid": str(sid), "domain": "repl.it", "path": "/"}

        s = requests.get("https://repl.it/~", cookies=cookie).text
        soup = bs4.BeautifulSoup(s, "html.parser")

        if confirm_login(soup.title.text):
            return UserClient(cookie, sid)
        else:
            raise LoginError(
                "LoginError", "SID could not connect to a repl.it account", 401
            )

        return None

    def create(self, language="python3", **kwargs):
        data = {"language": language}
        data = update_dict(data, kwargs)

        r = requests.post(
            "https://repl.it/data/repls/new",
            data=json.dumps(data),
            headers={
                "Accept": "application/json",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://repl.it/",
                "Content-Type": "application/json",
            },
        ).json()
        ensure_json(r)

        repl = update_dict({}, r)
        token = fetch_pot_token(repl["id"])

        return Repl(repl)

    def load_from_path(self, path):
        r = requests.get(f"https://repl.it/data/repls/{path}").json()
        ensure_json(r)

        repl = update_dict({}, r)
        token = fetch_pot_token(repl["id"])

        return Repl(repl)


class UserClient(Client):
    def __init__(self, cookie, sid):
        self.sid = sid
        self.user = cookie

    def __getattribute__(self, name):
        return super(UserClient, self).__getattribute__(name)

    def login(self):
        pass

    def logout(self):
        del self.sid
        del self.user

        return Client()

    def create(self, language="python3", **kwargs):
        data = {"language": language}
        data = update_dict(data, kwargs)

        r = requests.post(
            "https://repl.it/data/repls/new",
            data=json.dumps(data),
            cookies=self.user,
            headers={
                "Accept": "application/json",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://repl.it/",
                "Content-Type": "application/json",
            },
        ).json()
        ensure_json(r)

        repl = update_dict({}, r)
        token = fetch_pot_token(repl["id"])

        return Repl(repl, token)

    def load_from_path(self, path):
        r = requests.get(f"https://repl.it/data/repls/{path}", cookies=self.user).json()
        ensure_json(r)

        repl = update_dict({}, r)
        token = fetch_pot_token(repl["id"])

        return Repl(repl, token)

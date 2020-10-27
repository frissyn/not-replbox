import json
import requests

from .errors import APIError


def fetch_langs():
    langs = []
    r = requests.get("https://eval.repl.it/languages").json()

    for langObj in r:
        langs.append(
            {
                "name": langObj["name"],
                "displayName": langObj["displayName"],
                "category": langObj["category"],
                "extension": langObj["extension"],
            }
        )

    return langs


def fetch_token(replID, apiKey):
    r = requests.post(
        f"https://repl.it/api/v0/repls/{replID}/token",
        data=json.dumps({"apiKey": apiKey}),
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )

    return r.json()


def fetch_pot_token(replID):
    r = requests.post(
        f"https://repl.it/api/v0/repls/{replID}/token",
        data=json.dumps({"liveCodingToken": None, "polyglott": False}),
        headers={
            "Referer": "https://repl.it/",
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    return r.json()


def mainf(files, lang):
    ext = get_lang_exts()[lang]
    name = "main." + ext
    for file in files:
        if file == name:
            return file
        else:
            pass
    return files[0]


def confirm_login(content):
    if content == "Repl.it - Login":
        return False
    elif content == "Repl.it - Home":
        return True
    else:
        return None


def ensure_json(tokenjson):
    try:
        if tokenjson["message"]:
            raise APIError(
                tokenjson["name"],
                tokenjson["message"],
                tokenjson["status"],
            )
        else:
            pass
    except (KeyError, TypeError):
        pass


def update_dict(stale, latest):
    for key, items in latest.items():
        stale[key] = latest[key]

    return stale


def set_lang_exts():
    r = requests.get("https://eval.repl.it/languages").json()
    with open("replbox/misc/exts.json", "a") as fp:
        fp.write("{\n")
        for langObj in r:
            fp.write(f"\t\"{langObj['name']}\":\"{langObj['extension']}\"")
            if langObj != r[-1]:
                fp.write(",\n")
            else:
                fp.write("\n")
        fp.write("}")

    return True


def get_lang_exts():
    with open("replbox/misc/exts.json", "r") as fp:
        res = json.load(fp)

    return res

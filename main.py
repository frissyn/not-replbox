import os
import json
import replbox


client = replbox.Client()

repl = client.load_from_path("@replbox/dummy-repl")

path = os.getcwd() + "/" + repl.slug + "/"
for file in repl.fileNames:
    repl.ensure_path(path + file, suppress=True)
    print(f"Created directory: {path + file}")

    with open(path + file, "w+") as fp:
        repl.dump(file, fp)
        print(f"Contents successfully dumped.")

    print()

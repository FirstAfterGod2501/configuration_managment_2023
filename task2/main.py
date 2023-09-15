import requests


def get_package(name, sep, deps):
    try:
        result = requests.get(f'https://pypi.org/pypi/{name}/json')
    except Exception as e:
        get_package(name, sep, deps)
        return
    if ("info" in result.json() and "requires_dist" in result.json()["info"] and result.json()["info"][
        "requires_dist"]):
        for i in result.json()["info"]["requires_dist"]:
            pack = str(i).split()[0].split(">", 1)[0].split("=", 1)[0].split("<", 1)[0].split("[", 1)[0].split(';', 1)[
                0].split('~', 1)[0]
            if deps and pack not in deps:
                print(sep + " " + pack)
                deps.append(pack)
                new_deps = deps
                get_package(pack, pack + "->", new_deps)

            if not deps:
                print(sep + " " + pack)
                deps.append(pack)
                new_deps = deps
                get_package(pack, pack + "->", new_deps)


if __name__ == "__main__":
    get_package("tensorflow", "tensorflow->", [])

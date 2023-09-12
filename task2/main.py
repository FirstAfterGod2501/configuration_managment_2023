import time

import networkx as nx
import requests
import json


# https://pypi.org/pypi/pdfplumber/json

def getPackage(name, sep, deps):
    try:
        result = requests.get(f'https://pypi.org/pypi/{name}/json')
    except  Exception as e:
        normal = "true"
        return
    if ("info" in result.json() and "requires_dist" in result.json()["info"] and result.json()["info"][
        "requires_dist"]):
        for i in result.json()["info"]["requires_dist"]:
            pack = str(i).split()[0].split(">", 1)[0].split("=", 1)[0].split("<", 1)[0].split("[", 1)[0].split(';', 1)[0].split('~', 1)[0]
            if deps and pack not in deps:
                #print(deps)
                print(sep + " " + pack)
                deps.append(pack)
                newDeps = deps
                getPackage(pack, sep + pack + "->", newDeps)

            if not deps:
                print(sep + " " + pack)
                deps.append(pack)
                newDeps = deps
                getPackage(pack, sep + pack + "->", newDeps)


if __name__ == "__main__":
    dependency_graph = nx.DiGraph()
    getPackage("tensorflow", "tensorflow->", [])

    # print(graphviz)

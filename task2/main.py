import argparse
import json
import sys

from packaging import version
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
from packaging.pypi.simple import SimpleIndex

def get_dependencies_graph(package_name):
    graph = {}

    package_info = SimpleIndex().info(package_name)
    if not package_info:
        print(f"Package '{package_name}' not found.")
        return graph

    def get_dependencies(package, version_spec):
        package_key = canonicalize_name(package)

        if package_key in graph:
            return

        graph[package_key] = []

        try:
            package_info = SimpleIndex().info(package)
            requires_dist = package_info['info']['requires_dist']
        except:
            return

        for requirement in requires_dist:
            req = Requirement(requirement)
            dep_package = canonicalize_name(req.name)

            if dep_package not in graph[package_key]:
                graph[package_key].append(dep_package)

            if version_spec:
                for available_version in SimpleIndex().iter_versions(dep_package):
                    if version_spec.contains(version.parse(available_version)):
                        get_dependencies(dep_package, f"=={available_version}")
            else:
                get_dependencies(dep_package, req.specifier)

    get_dependencies(package_info["name"], "")

    return graph


def generate_graphviz(graph):
    graphviz = "digraph Dependencies {\n"

    for package, dependencies in graph.items():
        graphviz += f'\t"{package}" [label="{package}"];\n'
        for dependency in dependencies:
            graphviz += f'\t"{package}" -> "{dependency}";\n'

    graphviz += "}\n"
    return graphviz


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dependency graph generator.")
    parser.add_argument("package", help="Package name")
    args = parser.parse_args()

    dependencies_graph = get_dependencies_graph(args.package)
    graphviz = generate_graphviz(dependencies_graph)

    print(graphviz)
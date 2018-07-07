#!/usr/bin/python3

import re
import sys

import devpipeline_core.resolve


def _dotify(string):
    """This function swaps '-' for '_'."""
    return re.sub("-", lambda m: "_", string)


def _do_dot(targets, components, layer_fn):
    def _handle_layer_dependencies(resolved_dependencies, attributes):
        for component in resolved_dependencies:
            stripped_name = _dotify(component)
            component_dependencies = components[component].get("depends")
            if component_dependencies:
                for dep in devpipeline_core.config.config.split_list(
                        component_dependencies):
                    print("{} -> {} {}".format(stripped_name,
                                               _dotify(dep), attributes))
            print("{} {}".format(stripped_name, attributes))

    print("digraph dependencies {")
    try:
        devpipeline_core.resolve.process_dependencies(
            targets, components, lambda rd: layer_fn(
                rd, lambda rd: _handle_layer_dependencies(
                    rd, "")))
    except devpipeline_core.resolve.CircularDependencyException as cde:
        layer_fn(
            cde._components,
            lambda rd: _handle_layer_dependencies(
                rd, "[color=\"red\"]"))
    print("}")


def print_layers(targets, components):
    layer = 0

    def _add_layer(resolved_dependencies, dep_fn):
        nonlocal layer

        print("subgraph cluster_{} {{".format(layer))
        print("label=\"Layer {}\"".format(layer))
        dep_fn(resolved_dependencies)
        print("}")
        layer += 1

    _do_dot(targets, components, _add_layer)


def print_graph(targets, components):
    # pylint: disable=protected-access
    _do_dot(targets, components, lambda rd, dep_fn: dep_fn(rd))


def print_dot(targets, components):
    print("Warning: dot option is deprecated.  Use graph instead.",
          file=sys.stderr)
    print_graph(targets, components)

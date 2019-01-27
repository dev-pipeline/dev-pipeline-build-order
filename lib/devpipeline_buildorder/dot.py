#!/usr/bin/python3

"""
Output methods that use dot syntax to represent dependency information.
"""

import re
import sys

import devpipeline_core.resolve


def _dotify(string):
    """This function swaps '-' for '_'."""
    return re.sub("-", lambda m: "_", string)


def _do_dot(targets, components, tasks, layer_fn):
    print("digraph dependencies {")
    try:

        def _make_attribute_fn():
            if len(tasks) > 1:
                return lambda component_task: ' [label="{}"]'.format(component_task[1])
            return lambda component_task: ""

        def _print_dependency(
            indentation, component_task, dependent_task, attribute_fn
        ):
            if component_task[0] != dependent_task[0]:
                print(
                    "{}{} -> {}{}".format(
                        indentation,
                        _dotify(component_task[0]),
                        _dotify(dependent_task[0]),
                        attribute_fn(component_task),
                    )
                )

        attribute_fn = _make_attribute_fn()
        dm = devpipeline_core.resolve.calculate_dependencies(targets, components, tasks)

        def _print_dependencies(indentation, component_tasks):
            for component_task in component_tasks:
                dependencies = dm.get_dependencies(component_task)
                if dependencies:
                    for dependency_task in dependencies:
                        _print_dependency(
                            indentation, component_task, dependency_task, attribute_fn
                        )
                else:
                    print("{}{}".format(indentation, _dotify(component_task[0])))
                task_queue.resolve(component_task)

        task_queue = dm.get_queue()
        for component_tasks in task_queue:
            layer_fn(
                lambda indentation: _print_dependencies(indentation, component_tasks)
            )
    except devpipeline_core.resolve.CircularDependencyException as cde:
        del cde
    print("}")


def _print_layers(targets, components, tasks):
    """
    Print dependency information, grouping components based on their position
    in the dependency graph.  Components with no dependnecies will be in layer
    0, components that only depend on layer 0 will be in layer 1, and so on.

    If there's a circular dependency, those nodes and their dependencies will
    be colored red.

    Arguments
    targets - the targets explicitly requested
    components - full configuration for all components in a project
    """
    layer = 0

    def _add_layer(dep_fn):
        nonlocal layer

        indentation = " " * 4
        print("{}subgraph cluster_{} {{".format(indentation, layer))
        print('{}label="Layer {}"'.format(indentation * 2, layer))
        dep_fn(indentation * 2)
        print("{}}}".format(indentation))
        layer += 1

    _do_dot(targets, components, tasks, _add_layer)


_LAYERS_TOOL = (
    _print_layers,
    "Print a dot graph that groups components by their position in a layered "
    "architecture.  Components are only permitted to depend on layers with a "
    "lower number.",
)


def _print_graph(targets, components, tasks):
    """
    Print dependency information using a dot directed graph.  The graph will
    contain explicitly requested targets plus any dependencies.

    If there's a circular dependency, those nodes and their dependencies will
    be colored red.

    Arguments
    targets - the targets explicitly requested
    components - full configuration for all components in a project
    """
    indentation = " " * 4
    _do_dot(targets, components, tasks, lambda dep_fn: dep_fn(indentation))


_GRAPH_TOOL = (
    _print_graph,
    "Print a dot graph where each " "component points at its dependnet components.",
)


def _print_dot(targets, components, tasks):
    """
    Deprecated function; use print_graph.

    Arguments
    targets - the targets explicitly requested
    components - full configuration for all components in a project
    """
    print("Warning: dot option is deprecated.  Use graph instead.", file=sys.stderr)
    _print_graph(targets, components, tasks)


_DOT_TOOL = (_print_dot, 'Deprecated -- use the "graph" option instead.')

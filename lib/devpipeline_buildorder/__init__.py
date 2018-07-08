#!/usr/bin/python3

import devpipeline_core.resolve


def _print_list(targets, components):
    build_order = devpipeline_core.resolve.order_dependencies(
        targets, components)
    print(build_order)


_LIST_TOOL = (_print_list, "Print a sequential order of components.")

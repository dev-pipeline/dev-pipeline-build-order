#!/usr/bin/python3

"""
Root module for the build-order tool.
"""

import devpipeline_core.resolve


# For some reason, setup.py can't find this in the build_order moudle.  Move it
# back when I figure out why.
def _print_list(targets, components, tasks):
    def _make_print_fn():
        if len(tasks) > 1:
            return lambda component_task: "{}.{}".format(
                component_task[0], component_task[1]
            )
        return lambda component_task: component_task[0]

    dm = devpipeline_core.resolve.calculate_dependencies(targets, components, tasks)
    build_order = []
    task_queue = dm.get_queue()
    print_fn = _make_print_fn()
    for component_tasks in task_queue:
        for component_task in component_tasks:
            build_order.append(print_fn(component_task))
            task_queue.resolve(component_task)
    print(build_order)


_LIST_TOOL = (_print_list, "Print a sequential order of components.")

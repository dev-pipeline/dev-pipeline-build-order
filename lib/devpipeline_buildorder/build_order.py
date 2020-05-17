#!/usr/bin/python3
"""This modules generates a build ordered list of targets."""

import argparse

import devpipeline_core.command
import devpipeline_core.plugin
import devpipeline_core.resolve
import devpipeline_configure.load


_ORDER_OUTPUTS = devpipeline_core.plugin.query_plugins(
    "devpipeline.build_order.methods"
)


_MAJOR = 0
_MINOR = 5
_PATCH = 0

_STRING = "{}.{}.{}".format(_MAJOR, _MINOR, _PATCH)


def _configure(parser):
    devpipeline_core.command.setup_target_parser(parser)
    parser.add_argument(
        "--method", help="The method used to display build order.", default="list"
    )
    parser.add_argument(
        "--tasks",
        help="A comma-separated list of tasks to consider.  There will "
        "be an implicit dependency created on earler tasks (this "
        "matches the behavior of other commands).",
        default="build",
    )
    devpipeline_core.command.add_version_info(parser, _STRING)

    # self.add_argument(
    # "--list-methods",
    # action="store_true",
    # default=argparse.SUPPRESS,
    # help="List the available methods instead of printing dependency information.",
    # )


def _execute(arguments):
    def _list_methods():
        for key in sorted(_ORDER_OUTPUTS):
            print("{} - {}".format(key, _ORDER_OUTPUTS[key][1]))

    def _display(targets, full_config):
        build_order = _ORDER_OUTPUTS.get(arguments.method)
        if not build_order:
            raise Exception("Invalid method: {}".format(arguments.method))
        build_order[0](targets, full_config, arguments.tasks.split(","))

    if "list_methods" in arguments:
        _list_methods()
    else:
        devpipeline_core.command.process_targets(
            arguments, _display, devpipeline_configure.load.update_cache
        )


def main(args=None, config_fn=devpipeline_configure.load.update_cache):
    # pylint: disable=missing-docstring
    build_orderer = BuildOrderer(config_fn)
    devpipeline_core.command.execute_command(build_orderer, args)


_BUILD_ORDER_COMMAND = (
    "Generate dependency information about project components.",
    _configure,
    _execute,
)

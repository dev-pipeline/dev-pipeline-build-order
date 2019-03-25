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


def _list_methods():
    for key in sorted(_ORDER_OUTPUTS):
        print("{} - {}".format(key, _ORDER_OUTPUTS[key][1]))


_MAJOR = 0
_MINOR = 5
_PATCH = 0

_STRING = "{}.{}.{}".format(_MAJOR, _MINOR, _PATCH)


class BuildOrderer(devpipeline_core.command.TargetCommand):

    """This class outputs an ordered list of the packages to satisfy dependencies."""

    def __init__(self, config_fn):
        super().__init__(
            config_fn=config_fn,
            prog="dev-pipeline build-order",
            description="Determinte all dependencies of a set of targets and "
            "the order they should be built in.",
        )
        self.add_argument(
            "--method", help="The method used to display build order.", default="list"
        )
        self.add_argument(
            "--tasks",
            help="A comma-separated list of tasks to consider.  There will "
            "be an implicit dependency created on earler tasks (this "
            "matches the behavior of other commands).",
            default="build",
        )
        self.add_argument(
            "--list-methods",
            action="store_true",
            default=argparse.SUPPRESS,
            help="List the available methods instead of printing dependency information.",
        )
        self.set_version(_STRING)

    def process(self, arguments):
        if "list_methods" in arguments:
            _list_methods()
        else:
            super().process(arguments)

    def process_targets(self, targets, full_config, arguments):
        del self

        build_order = _ORDER_OUTPUTS.get(arguments.method)
        if not build_order:
            raise Exception("Invalid method: {}".format(arguments.method))
        build_order[0](targets, full_config, arguments.tasks.split(","))


def main(args=None, config_fn=devpipeline_configure.load.update_cache):
    # pylint: disable=missing-docstring
    build_orderer = BuildOrderer(config_fn)
    devpipeline_core.command.execute_command(build_orderer, args)


_BUILD_ORDER_COMMAND = (
    main,
    "Generate dependency information about project components.",
)

if __name__ == "__main__":
    main()

#!/usr/bin/python3
"""This modules generates a build ordered list of targets."""

import devpipeline_core.config.config
import devpipeline_core.command
import devpipeline_core.plugin
import devpipeline_core.resolve


def _print_list(targets, components):
    build_order = devpipeline_core.resolve.order_dependencies(targets, components)
    print(build_order)


_ORDER_OUTPUTS = None


def _initialize_outputs():
    global _ORDER_OUTPUTS

    if not _ORDER_OUTPUTS:
        _ORDER_OUTPUTS = devpipeline_core.plugin.query_plugins('devpipeline.build_order.methods')


class BuildOrderer(devpipeline_core.command.TargetTool):

    """This class outputs an ordered list of the packages to satisfy dependencies."""

    def __init__(self):
        super().__init__(executors=False,
                         prog="dev-pipeline build-order",
                         description="Determinte all dependencies of a set of "
                                     "targets and the order they should be "
                                     "built in.")
        self.add_argument("--method",
                          help="The method used to display build order.",
                          default="list")
        self.helper_fn = None

    def setup(self, arguments):
        _initialize_outputs()
        self.helper_fn = _ORDER_OUTPUTS.get(arguments.method)
        if not self.helper_fn:
            raise Exception("Invalid method: {}".format(arguments.method))

    def process(self):
        self.helper_fn(self.targets, self.components)


def main(args=None):
    # pylint: disable=missing-docstring
    build_orderer = BuildOrderer()
    devpipeline_core.command.execute_tool(build_orderer, args)


if __name__ == '__main__':
    main()

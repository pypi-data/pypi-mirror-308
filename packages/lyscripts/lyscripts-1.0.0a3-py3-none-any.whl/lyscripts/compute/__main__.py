"""Run the compute module as a script."""

import argparse

from lyscripts import RichDefaultHelpFormatter, exit_cli
from lyscripts.compute import posteriors, prevalences, priors, risks


def main(args: argparse.Namespace):
    """Run the main script."""
    parser = argparse.ArgumentParser(
        prog="lyscripts predict",
        description=__doc__,
        formatter_class=RichDefaultHelpFormatter,
    )
    parser.set_defaults(run_main=exit_cli)
    subparsers = parser.add_subparsers()

    # the individual scripts add `ArgumentParser` instances and their arguments to
    # this `subparsers` object
    priors._add_parser(subparsers, help_formatter=parser.formatter_class)
    posteriors._add_parser(subparsers, help_formatter=parser.formatter_class)
    prevalences._add_parser(subparsers, help_formatter=parser.formatter_class)
    risks._add_parser(subparsers, help_formatter=parser.formatter_class)

    args = parser.parse_args()
    args.run_main(args, parser)


if __name__ == "__main__":
    main()

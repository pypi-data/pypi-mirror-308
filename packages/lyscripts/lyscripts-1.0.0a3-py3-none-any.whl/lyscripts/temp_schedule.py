r"""Generate inverse temperature schedules for thermodynamic integration.

Thermodynamic integration is quite sensitive to the specific schedule which is used.
I noticed in my models, that within the interval $[0, 0.1]$, the increase in the
expected log-likelihood is very steep. Hence, the inverse temperature $\\beta$ must be
more densely spaced in the beginning.

This can be achieved by using a power sequence: Generate $n$ linearly spaced points in
the interval $[0, 1]$ and then transform each point by computing $\\beta_i^k$ where
$k$ could e.g. be 5.
"""
import argparse
import logging
from collections.abc import Callable
from pathlib import Path

import numpy as np
import yaml

logger = logging.getLogger(__name__)


def _add_parser(
    subparsers: argparse._SubParsersAction,
    help_formatter,
):
    """Add an `ArgumentParser` to the subparsers action."""
    parser = subparsers.add_parser(
        Path(__file__).name.replace(".py", ""),
        description=__doc__,
        help=__doc__,
        formatter_class=help_formatter,
    )
    _add_arguments(parser)


def _add_arguments(parser: argparse.ArgumentParser):
    """Add arguments needed to run this script to a `subparsers` instance."""
    parser.add_argument(
        "--method",
        choices=SCHEDULES.keys(),
        default=list(SCHEDULES.keys())[0],
        help="Choose the method to distribute the inverse temperature.",
    )
    parser.add_argument(
        "--num",
        default=32,
        type=int,
        help="Number of inverse temperatures in the schedule",
    )
    parser.add_argument(
        "--pow",
        default=4,
        type=float,
        help="If a power schedule is chosen, use this as power",
    )

    parser.set_defaults(run_main=main)


def tolist(func: Callable) -> Callable:
    """Decorate func to make sure the returned value is a list of floats."""

    def inner(*args) -> np.ndarray | list[float]:
        res = func(*args)
        if isinstance(res, np.ndarray):
            return res.tolist()
        return res

    return inner


@tolist
def geometric_schedule(n: int, *_a) -> np.ndarray:
    """Create a geometric sequence of `n` numbers from 0. to 1."""
    log_seq = np.logspace(0.0, 1.0, n)
    shifted_seq = log_seq - 1.0
    geom_seq = shifted_seq / 9.0
    return geom_seq


@tolist
def linear_schedule(n: int, *_a) -> np.ndarray:
    """Create a linear sequence of `n` numbers from 0. to 1."""
    return np.linspace(0.0, 1.0, n)


@tolist
def power_schedule(n: int, power: float, *_a) -> np.ndarray:
    """Create a power sequence of `n` numbers from 0. to 1."""
    lin_seq = np.linspace(0.0, 1.0, n)
    return lin_seq**power


SCHEDULES = {
    "geometric": geometric_schedule,
    "linear": linear_schedule,
    "power": power_schedule,
}


def main(args: argparse.Namespace):
    """Generate a temperature schedule."""
    func = SCHEDULES[args.method]
    schedule = func(args.num, args.pow)
    yaml_output = yaml.dump({"temp_schedule": schedule})
    logger.info(f"Created {args.method} sequence of length {args.num}")
    logger.debug(yaml_output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    _add_arguments(parser)

    args = parser.parse_args()
    args.run_main(args)

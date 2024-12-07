"""Script to run doctests in the modules of `lyscripts`."""

import doctest

from lyscripts import utils
from lyscripts.compute import prevalences, risks
from lyscripts.plot import corner, histograms, thermo_int

if __name__ == "__main__":
    doctest.testmod(utils, verbose=True)
    doctest.testmod(histograms, verbose=True)
    doctest.testmod(corner, verbose=True)
    doctest.testmod(thermo_int, verbose=True)
    doctest.testmod(prevalences, verbose=True)
    doctest.testmod(risks, verbose=True)

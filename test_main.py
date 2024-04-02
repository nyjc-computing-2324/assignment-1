from importlib import reload
import subprocess
import sys
import unittest

import main


# limit number of retries
MAX_RETRIES = 5
retries = 0


def fetch_autograding() -> None:
    subprocess.run(["git", "submodule", "update", "--init", "--remote"])
    
def autograding_successfully_imported() -> bool:
    """Check if autograding module is successfully imported.

    If a submodule is imported (e.g. autograding.case), autograding may be imported
    as a namespace module.
    Namespace modules have __file__ attribute set tot None, so we can use that to check
    if autograding was imported as a module and not just a namespace module.
    """
    return (
        "autograding" in locals()
        and locals().get("autograding").__file__
    )

# Force refresh of autograding module from upstream
fetch_autograding()

# autograding submodule might not be successfully fetched on init
# if unsuccessful, we have to fetch it manually
while not autograding_successfully_imported():
    try:
        import autograding
        reload(autograding)
        from autograding.case import FuncCall, InOut, RecursiveCall
    except (ImportError, ModuleNotFoundError):
        fetch_autograding()
        retries += 1
    else:
        break
    if retries >= MAX_RETRIES:
        sys.exit("[import autograding] Too many retries, exiting")


class TestSF(autograding.TestInputOutput):
    def setUp(self):
        self.testcases = [
            InOut(input="56", output="The duration is 0 hours, 0 minutes, and 56 seconds."),
            InOut(input="2846", output="The duration is 0 hours, 47 minutes, and 26 seconds."),
            InOut(input="3694", output="The duration is 1 hours, 1 minutes, and 34 seconds."),
        ]


if __name__ == '__main__':
    unittest.main()

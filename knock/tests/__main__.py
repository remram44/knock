import os
import sys
import unittest


top_level = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
start_dir = os.path.join(top_level, 'knock/tests')
if not top_level in sys.path:
    sys.path.append(top_level)


import knock.main
knock.main.setup()


sys.path.append(start_dir)


class Program(unittest.TestProgram):
    def createTests(self):
        if self.testNames is None:
            self.test = self.testLoader.discover(
                    start_dir=start_dir,
                    pattern='test_*.py',
                    top_level_dir=top_level)
        else:
            self.test = self.testLoader.loadTestsFromNames(self.testNames)

Program()

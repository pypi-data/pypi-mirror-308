import json
import pathlib
import unittest

import pivmetalib

__this_dir__ = pathlib.Path(__file__).parent


class TestVersion(unittest.TestCase):

    def test_version(self):
        this_version = 'x.x.x'
        setupcfg_filename = __this_dir__ / '../setup.cfg'
        with open(setupcfg_filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if 'version' in line:
                    this_version = line.split(' = ')[-1].strip()
        self.assertEqual(pivmetalib.__version__, this_version)

    def test_codemeta(self):
        """checking if the version in codemeta.json is the same as the one of the toolbox"""

        with open(__this_dir__ / '../codemeta.json', 'r') as f:
            codemeta = json.loads(f.read())

        assert codemeta['version'] == pivmetalib.__version__

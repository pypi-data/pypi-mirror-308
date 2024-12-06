import pathlib
import unittest

import pivtestdata as ptd

__this_dir__ = pathlib.Path(__file__).parent


class TestPIVTec(unittest.TestCase):

    def test_version(self):
        this_version = 'x.x.x'
        setupcfg_filename = __this_dir__ / '../setup.cfg'
        with open(setupcfg_filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if 'version' in line:
                    this_version = line.split(' = ')[-1].strip()
        self.assertEqual(ptd.__version__, this_version)

    def test_filesizes(self):
        self.assertEqual(ptd.pivtec.vortex_pair.file_size, 11646143)

    def test_delete_all(self):
        ptd.delete_all_downloaded_files()
        self.assertFalse(ptd.user_dir.exists())

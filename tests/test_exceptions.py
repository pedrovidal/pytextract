import unittest
import os
import subprocess
import uuid

from . import base


class ExceptionTestCase(base.GenericUtilities, unittest.TestCase):
    """This class contains a bunch of tests to make sure that pytextract
    fails in expected ways.
    """

    def test_unsupported_extension_cli(self):
        """Make sure unsupported extension exits with non-zero status"""
        filename = self.get_temp_filename(extension="extension")
        command = "pytextract %(filename)s 2> /dev/null" % locals()
        self.assertEqual(1, subprocess.call(command, shell=True))
        os.remove(filename)

    def test_unsupported_extension_python(self):
        """Make sure unsupported extension raises the correct error"""
        filename = self.get_temp_filename(extension="extension")
        import pytextract
        from pytextract.exceptions import ExtensionNotSupported
        with self.assertRaises(ExtensionNotSupported):
            pytextract.process(filename)
        os.remove(filename)

    def test_missing_filename_cli(self):
        """Make sure missing files exits with non-zero status"""
        filename = self.get_temp_filename()
        os.remove(filename)
        command = "pytextract %(filename)s 2> /dev/null" % locals()
        self.assertEqual(1, subprocess.call(command, shell=True))

    def test_missing_filename_python(self):
        """Make sure missing files raise the correct error"""
        filename = self.get_temp_filename()
        os.remove(filename)
        import pytextract
        from pytextract.exceptions import MissingFileError
        with self.assertRaises(MissingFileError):
            pytextract.process(filename)

    def test_shell_parser_run(self):
        """get a useful error message when a dependency is missing"""
        from pytextract.parsers import utils
        from pytextract.parsers import exceptions
        parser = utils.ShellParser()
        try:
            # There shouldn't be a command on the path matching a random uuid
            parser.run([str(uuid.uuid4())])
        except exceptions.ShellError as e:
            self.assertTrue(e.is_not_installed())
        else:
            self.assertTrue(False, "Expected ShellError")

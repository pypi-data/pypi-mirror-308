import unittest
from src.cli import main
import sys
from tempfile import TemporaryFile

class TestCLI(unittest.TestCase):

    def setUp(self):
        # TemporaryFile to capture stdout output
        self.held_output = TemporaryFile(mode='w+')
        sys.stdout = self.held_output

    def tearDown(self):
        # Reset redirection and close TemporaryFile
        sys.stdout = sys.__stdout__
        self.held_output.close()

    def run_test_with_args(self, args, output_txt_file):
        # Clear the TemporaryFile before each test
        self.held_output.seek(0)
        self.held_output.truncate(0)

        sys.argv = ["cbrext"] + args
        main()

        # Move to the beginning of the TemporaryFile to read the content
        self.held_output.seek(0)
        output = self.held_output.read().strip()

        # Read the expected output from a text file
        with open(output_txt_file, "r") as file:
            expected_output = file.read()

        # Check if the output matches the expected output
        self.assertIn(expected_output, output, f"Output does not match for option {args}")

    def test_cli_pcap(self):
        args = ["tests/pcaps/filtered_4F_0.pcap"]
        output_txt_file = "tests/out_cli/4F_0.pcap.txt"
        self.run_test_with_args(args, output_txt_file)

    # TODO: too long stdout output
    # def test_cli_directory(self):
    #     args = ["-d", "tests/pcaps"]
    #     output_txt_file = "tests/out_cli/-d-tests-pcaps.txt"
    #     self.run_test_with_args(args, output_txt_file)

if __name__ == '__main__':
    unittest.main()

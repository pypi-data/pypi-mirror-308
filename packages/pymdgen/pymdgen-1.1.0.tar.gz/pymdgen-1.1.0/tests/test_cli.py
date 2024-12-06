import subprocess

# from helpers import write_expected

from pymdgen.cli import run


def test_cli(expected_docs_md):
    output = subprocess.check_output(["pymdgen", "pymdgen.test_module"])
    if isinstance(output, bytes):
        output = output.decode("unicode_escape")

    assert output == expected_docs_md + "\n"


def test_run(expected_docs_list):
    output = run(["pymdgen.test_module"], False, 3)
    assert output == expected_docs_list

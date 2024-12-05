import pytest
import os.path
from erp5_coverage_plugin import PythonScriptParser


@pytest.fixture()
def parser():
  parser = PythonScriptParser(
    filename=os.path.join(
      os.path.dirname(__file__), 'test_data', 'python_script.py'))

  parser.parse_source()
  return parser


def test_statements(parser):
  assert parser.statements == {3, 4, 5, 7, 13}

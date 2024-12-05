import contextlib
import json
import os

from Products.PythonScripts.PythonScript import PythonScript
from Products.PythonScripts.tests.testPythonScript import DummyFolder
from Testing.makerequest import makerequest
import coverage
import pytest


@pytest.fixture()
def file_system_script(tmp_path):
  p = tmp_path / 'script.py'
  p.write_text(
    '''\
if "a" == "a" and "b" == "c":
  _ = 1 / 0 # will not be covered

_ = 1 + 1
# comment

return 'returned value'
''')
  yield p


@contextlib.contextmanager
def _coverage_process(file_system_script, branch):
  cwd = os.getcwd()
  os.chdir(file_system_script.parent)
  cp = coverage.Coverage(include=['./*'], branch=branch)
  cp.set_option('run:plugins', ['erp5_coverage_plugin'])
  cp.start()
  yield cp
  cp.stop()
  os.chdir(cwd)


@pytest.fixture()
def coverage_process(file_system_script):
  with _coverage_process(file_system_script, branch=False) as cp:
    yield cp


@pytest.fixture()
def coverage_process_with_branch_coverage(file_system_script, request):
  with _coverage_process(file_system_script, branch=True) as cp:
    yield cp


@pytest.fixture()
def python_script(file_system_script):
  ps = PythonScript('test_script')
  # Important note: for this plugin to work, something must set the property on python
  # script
  ps._erp5_coverage_filename = str(file_system_script.absolute())

  ps.ZPythonScript_edit('', file_system_script.read_text())
  yield ps.__of__(makerequest(DummyFolder('folder')))


@pytest.fixture()
def python_script_with_callback(file_system_script):
  file_system_script.write_text(
    '''\
result_storage = []
def callback_function(result):
  result_storage.append(result)
callback_script(callback_function)
return result_storage
''')
  source_code_folder = file_system_script.parent
  callback_file_system_script = source_code_folder / 'callback.py'
  callback_file_system_script.write_text(
    '''\
callback_function("returned value")
  ''')

  test_script = PythonScript('test_script')
  callback_script = PythonScript('callback_script')

  # Important note: for this plugin to work, something must set the property on python
  # script
  test_script._erp5_coverage_filename = str(file_system_script.absolute())
  callback_script._erp5_coverage_filename = str(callback_file_system_script.absolute())

  test_script.ZPythonScript_edit('', file_system_script.read_text())
  callback_script.ZPythonScript_edit(
    'callback_function', callback_file_system_script.read_text())
  folder = makerequest(DummyFolder('folder'))
  yield test_script.__of__(folder), callback_script.__of__(folder)


def test_python_script(coverage_process, python_script, capsys):
  assert python_script._exec({}, [], {}) == 'returned value'
  coverage_process.stop()
  assert coverage_process.report() > 0
  assert capsys.readouterr().out == '''\
Name        Stmts   Miss  Cover
-------------------------------
script.py       4      1    75%
-------------------------------
TOTAL           4      1    75%
'''


def test_python_script_with_branch_coverage(
    coverage_process_with_branch_coverage, python_script, capsys, tmp_path):
  assert python_script._exec({}, [], {}) == 'returned value'
  coverage_process_with_branch_coverage.stop()
  assert coverage_process_with_branch_coverage.report() > 0
  assert capsys.readouterr().out == '''\
Name        Stmts   Miss Branch BrPart  Cover
---------------------------------------------
script.py       4      1      2      1    67%
---------------------------------------------
TOTAL           4      1      2      1    67%
'''
  outfile = tmp_path / 'out.json'
  assert coverage_process_with_branch_coverage.json_report(outfile=outfile) > 0
  script_py_report = json.loads(outfile.read_text())['files']['script.py']
  script_py_report.pop('summary')
  script_py_report.pop('classes', None)
  script_py_report.pop('functions', None)
  assert script_py_report == {
    'excluded_lines': [],
    'executed_branches': [[1, 4]],
    'executed_lines': [1, 4, 7],
    'missing_branches': [[1, 2]],
    'missing_lines': [2],
  }


def test_python_script_callback(
    coverage_process, python_script_with_callback, capsys):
  test_python_script, callback_script = python_script_with_callback
  assert test_python_script._exec(
    {'callback_script': callback_script}, [], {}) == ['returned value']
  coverage_process.stop()
  assert coverage_process.report() > 0
  assert capsys.readouterr().out == '''\
Name          Stmts   Miss  Cover
---------------------------------
callback.py       1      0   100%
script.py         5      0   100%
---------------------------------
TOTAL             6      0   100%
'''


def test_python_script_callback_with_branch_coverage(
    coverage_process_with_branch_coverage, python_script_with_callback,
    capsys):
  test_python_script, callback_script = python_script_with_callback
  assert test_python_script._exec(
    {'callback_script': callback_script}, [], {}) == ['returned value']
  coverage_process_with_branch_coverage.stop()
  assert coverage_process_with_branch_coverage.report() > 0
  assert capsys.readouterr().out == '''\
Name          Stmts   Miss Branch BrPart  Cover
-----------------------------------------------
callback.py       1      0      0      0   100%
script.py         5      0      2      0   100%
-----------------------------------------------
TOTAL             6      0      2      0   100%
'''

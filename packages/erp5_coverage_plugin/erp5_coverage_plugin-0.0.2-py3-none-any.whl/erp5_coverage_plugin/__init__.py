#coding: utf-8
from __future__ import print_function, unicode_literals

import os

import coverage


class PythonScriptParser(coverage.parser.PythonParser):
  """Python parser understanding Zope's python script implicit function.

  parses the code with an extra function definition on first line and
  then substract 1 to the lines numbers.
  """
  def __init__(self, text=None, filename=None, exclude=None):
    super(PythonScriptParser, self).__init__(text=text, filename=filename, exclude=exclude)
    if filename:
      try:
        self.text = coverage.python.get_python_source(self.filename)
      except OSError as err:
        raise coverage.misc.NoSource(
          "No source for code: '{self.filename}': {err}".format(self=self, err=err))
    
    self.text = 'def _():\n  %s' % (
      '\n  '.join(line for line in self.text.splitlines())   
    )
    self.lines = self.text.split('\n')[1:]

  def _raw_parse(self):
    super(PythonScriptParser, self)._raw_parse()
    self._multiline = {
      k-1: v-1 for (k, v) in self._multiline.items()
    }
    # remove the "def ():\n" we added to compile as a function
    self.raw_excluded.discard(0)
    self.raw_docstrings.discard(0)
    self.raw_statements.discard(0)
    self._analyze_ast()

    self.raw_excluded = {v-1 for v in self.raw_excluded}
    self.raw_docstrings = {v-1 for v in self.raw_docstrings}
    self.raw_statements = {v-1 for v in self.raw_statements}

  def parse_source(self):
    super(PythonScriptParser, self).parse_source()
    self.statements.discard(0)

  def arcs(self):
    last_line = max(self.raw_statements)
    arcs = set()
    for l1, l2 in super(PythonScriptParser, self).arcs():
      if l1 == 1 and l2 == -1: # remove the arc from function def
        continue
      if l1 not in (-1, 1, last_line):
        l1 = l1 - 1
      if l2 not in (-1, 1, last_line):
        l2 = l2 - 1
      arcs.add((l1, l2))
    return arcs


class PythonScriptFileReporter(coverage.python.PythonFileReporter):

  @property
  def parser(self):
    """Overloaded to create a PythonScriptParser instead of PythonParser."""
    if self._parser is None:
      self._parser = PythonScriptParser(
        filename=self.filename,
        # TODO: this plugin does not support excludes
        #exclude=self.coverage._exclude_regex('exclude'),
      )
      self._parser.parse_source()
    return self._parser

  def no_branch_lines(self):
    return set()


class AbstractFileTracerPlugin(
    coverage.plugin.CoveragePlugin,
    coverage.plugin.FileTracer):

  _base_names = NotImplemented

  def __init__(self, options):
    self._options = options
    
  def file_tracer(self, filename):
    if os.path.basename(filename).split(':')[0] in self._base_names:
      return self
    return None


class TALESExpressionFileTracerPlugin(AbstractFileTracerPlugin):
  """This plugin is not really implemented, but prevent errors trying
  to cover TALES Expressions.
  """
  _base_names = ('PythonExpr', )

  def file_reporter(self, filename):
    class NoFileReporter(coverage.plugin.FileReporter):
      def source(self):
        raise coverage.misc.NoSource("no source for TALES Expressions")
      def lines(self):
        return set()
    return NoFileReporter(filename)

  def source_filename(self):
    return ''


class PythonScriptFileTracerPlugin(AbstractFileTracerPlugin):
  _base_names = {
    'ERP5 Python Script',
    'ERP5 Workflow Script',
    'Script (Python)',
  }

  def file_reporter(self, filename):
    return PythonScriptFileReporter(filename)

  def has_dynamic_source_filename(self):
    return True

  def dynamic_source_filename(self, filename, frame):
    for f in frame, frame.f_back, frame.f_back.f_back:
      if '__traceback_supplement__' in f.f_globals:
        filename = getattr(f.f_globals['__traceback_supplement__'][1], '_erp5_coverage_filename', None)
        if filename:
          return filename
    return None


def coverage_init(reg, options):
  reg.add_file_tracer(PythonScriptFileTracerPlugin(options))
  reg.add_file_tracer(TALESExpressionFileTracerPlugin(options))

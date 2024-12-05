[`coverage.py`](https://coverage.readthedocs.io/) plugin to collect coverage from business templates.

# How it works ?

## Python Scripts

### Collecting

This depend on business template installation setting the `_erp5_coverage_filename`
property on the script instance in ZODB. This property is a string, the
full path of the python script.

### Reporting

During reporting, coverage needs to know the set of lines number containing code,
to compare it with the line number that were actually executed.
Because python scripts are compiled as a function, they can not be parsed
by the default Python reporter, we use a simple reporter which wraps the
code in a function definition to compile and collect the line numbers and then
subtract 1 to the line numbers.


## ZODB Components

This also depends on business template installation setting the
`_erp5_coverage_filename` property on the script instance in ZODB and the dynamic
module to have it set to its `__file__`, then coverage can load it like a
traditional python module.


## Page Templates, TALES Expressions

Not supported, no coverage is collected.

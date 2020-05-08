# Min-entropy Tools

**A set of tools, based on NIST SP800-90B, to measure min-entropy of a data source.**

This is a fork of [a Python toolkit](https://github.com/dj-on-github/SP800_90b_tests) for NIST SP800-90B, and is intended to measure some simple entropy metrics from a given data source. The basis of the tool is the NIST SP800-90B spec: for an authoritative version, see the [ official NIST code.](https://github.com/usnistgov/SP800-90B_EntropyAssessment) 


**Design Goals**
- Handle >256 unique values. Both the cpp and py toolkit handle up to 8-bit values; this tool should be able to handle arbitrary-sized inputs.
- Performant on input sizes up to 1GB
- Modularity: Usable as a library or a CLI tool


**CLI Options** are preserved from the original repo:

```
$ ./sp800_90b_tests.py -h
usage: sp800_90b_tests.py [-h] [--be] [-t TESTNAME] [-l SYMBOL_LENGTH]
                          [--list_tests] [--test_iid]
                          [filename]

Test data to establish an entropy estimate, using NIST SP800-90B algorithms.

positional arguments:
  filename              Filename of binary file to test

optional arguments:
  -h, --help            show this help message and exit
  --be                  Treat data as big endian bits within bytes. Defaults
                        to little endian
  -t TESTNAME, --testname TESTNAME
                        Select the test to run. Defaults to running all tests.
                        Use --list_tests to see the list
  -l SYMBOL_LENGTH, --symbol_length SYMBOL_LENGTH
                        Indicate the length of each symbol in bits
  -s SYMBOLS            Specify the number of symbols to take from the file
  --list_tests          Display the list of tests
  --test_iid            Run Tests of IID Assumption (section 5)
  -v, --verbose         Output more information
  
```

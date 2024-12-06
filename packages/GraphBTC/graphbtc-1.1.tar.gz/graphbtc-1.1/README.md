[![Coverage Status](https://coveralls.io/repos/github/markbentivegna/BitcoinPy/badge.svg?branch=main)](https://coveralls.io/github/markbentivegna/BitcoinPy?branch=main)

# BitcoinPy

This Python module contains several Bitcoin utilities, notable the Bitcoin parser described in BitcoinGraph. This scrapes the entire Bitcoin blockchain and memory pool. 

# Background

This project contains all of the Bitcoin parsing capabilities described in detail in the BitcoinGraph white paper. This is the most comprehensive and robust open-sourced Python solution for scraping the entire Bitcoin blockchain, including the memory pool. 

# Features

* Scrape entire Bitcoin blockchain 
* Parse memory pool and all pre-validated transactions for real-time insights
* Decode Bitcoin Script language to read locking and unlocking scripts
* Parallel read buffers for optimal performance
* Unit test cases with over 95% code coverage
* Regression tests that encapsulate all edge cases of the blockchain
* Comprehensive documentation included in BitcoinGraph white paper

# Installation

```
pip install BitcoinPy
```

# Testing

All unit tests targeting specific objects are contained in the `test/unit` directory. 

Regression test cases are much more thorough and comprehensive and scrape various portions of the blockchain to ensure that code changes don't break anything.

```
coverage run -m pytest && coverage xml
```

XML coverage reports are generated and integrated with Coveralls to ensure integrity of underlying codebase.

# Development

This project currently supports Python 3.8-3.10. Contributions are welcome!

```
git clone https://github.com/markbentivegna/BitcoinPy.git
virtualenv -p python .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```


# Examples

There are two main ways of leveraging this project. One can clone the repository and use `blockchain_parser.py` as a CLI tool or download the Python package and integrate it directly into one's project. 

For CLI tool, please do the following:

```
pip install -r requirements.txt
python blockchain_parser.py CLI_ARGS
```

The output of `BitcoinPy.parse_blockchain()` will contain the blockchain contents of the specified parameters.

Run `python blockchain_parser.py -h` for more details of CLI arguments.

For integration into a separate project, please install the package via `pip` as described above. See below for example code snippet:

```
from BitcoinPy import BlockchainParser
blockchain_parser = BlockchainParser(f"PATH_TO_RAW_BLOCKS_FILE", START_INDEX, END_INDEX, include_mempool=True)
blockchain_contents = []
for i in range(START_INDEX, END_INDEX):
    blockchain_contents.append(blockchain_parser.parse_blk_file(i))
```

In BitcoinGraph, we insert the contents of the blockchain into a heavily optimized, low-latency database and then used for large-scale graph analytics. You are more than welcome to use the contents for whatever purpose you like!

# License


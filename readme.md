# Search

Search is a simple text search to look for various words within files on a give folder.

## Getting Started

Search is a very simple Python script. Just run it using your Python installation and have fun :)

### Prerequisites

Search requires standard Python 2.7.X + termcolor module


### Installing

For Python installation:

```
https://www.python.org/downloads/
```

For Termcolor installation with pip:

```
pip install termcolor
```

## Usage

### Simple Usage

```
python Search.py /var/log
```

### Usage with debug enabled

```
python Search.py /var/log debug
```

### Usage with experimental functions

```
modify control variable exp inside the script (line 21)
```


## Deployment

This script indexes the contents of the files in memory. Depending on the number of unique words found on the files, memory consumption can be as large as GBs. During some tests, with around 50 millions of unique entries, it was required about 9GB of memory and from 2min to 2min30s to conclude the indexing (Core i7 vPro Quadcore)
On Windows machines, termcolor does not work properly.

## Versioning

No system versioning in place yet

## Authors

* **Ismael Goncalves** -  [Sharingsec](https://sharingsec.blogspot.com)

## License

TBD

## Acknowledgments

* Professor Dan Jurafsky & Chris Manning from Stanford University for NLP Lectures
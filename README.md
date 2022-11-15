# progs
Python modules for handling core-collapse supernova progenitors.

The main purpose is to provide a generalised method of loading data from different sets of existing progenitor models.
These models are provided in a variety of formats, so I'd like to be able to easily load data from them without needing to think about the underlying data structure.

# Supported progenitor sets
- [`sukhbold_2016`](https://wwwmpa.mpa-garching.mpg.de/ccsnarchive/data/SEWBJ_2015/data/progenitor_models.tar.gz)
- Woosley & Heger 2002

# Setup
Two environment variables need to be set in your shell (e.g. in your `.bashrc`):
* `PROGS` - path to where you installed this code, e.g. `export PROGS=${HOME}/codes/progs`
* `PROGENITORS` - path to where you keep progenitor models, e.g. `export PROGENITORS=${HOME}/data/progenitors`

Append to your shell python path in order to import in python, e.g. `export PYTHONPATH=${PROGS}:${PYTHONPATH}`

# Getting Started
Download the Sukhbold 2016 set linked above and extract it into your `PROGENITORS` directory as a folder named `sukhbold_2016`:

```
$PROGENITORS
│
└───sukhbold_2016
|   |   s9.0_presn
|   │   s9.5_presn
|   │   ...
```

Then to load a progenitor model in python:

```
from progs.prog import Prog

model = Prog(mass=12.0, series='sukhbold_2016')
```

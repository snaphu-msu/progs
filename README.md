# progs
Python modules for handling core-collapse supernova progenitors.

The main purpose is to provide a generalised method of loading data from different sets of existing progenitor models.
These models are provided in a variety of formats, so I'd like to be able to easily load data from them without needing to think about the underlying data structure.

Supported progenitor sets:

- [`sukhbold_2016`](https://wwwmpa.mpa-garching.mpg.de/ccsnarchive/data/SEWBJ_2015/data/progenitor_models.tar.gz)
- Woosley & Heger 2002


# Python Dependencies
* python 3.8
* astropy
* matplotlib
* numpy
* pandas
* xarray

Use the included `environment.yml` file to easily set up a working [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands) environment:

```
conda env create -f environment.yml
conda activate progs
```


# Getting Started
Download the Sukhbold 2016 set linked above and extract the contents into the `progenitor_sets` directory under a folder named `sukhbold_2016`:

```
progenitor_sets
│
└───sukhbold_2016
|   |   s9.0_presn
|   │   s9.5_presn
|   │   ...
```

Then to load a progenitor model in python:

```
from progs.prog import Prog

model = Prog(mass='9.0', series='sukhbold_2016')
```

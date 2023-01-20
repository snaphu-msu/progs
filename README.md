# progs
Python modules for handling core-collapse supernova progenitors.

The main purpose is to provide a generalised method of loading data from different sets of existing progenitor models.
These models are provided in a variety of formats, so I'd like to be able to easily load data from them without needing to think about the underlying data structure.

Supported progenitor sets:

- [`sukhbold_2016`](https://wwwmpa.mpa-garching.mpg.de/ccsnarchive/data/SEWBJ_2015/data/progenitor_models.tar.gz) - [Sukhbold et al. (2016)](https://ui.adsabs.harvard.edu/abs/2018ApJ...860...93S/abstract)
- [`sukhbold_2018`](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/VOEXDE) - [Sukhbold et al. (2018)](https://ui.adsabs.harvard.edu/abs/2016ApJ...821...38S/abstract)
- [`sn1987a`](https://2sn.org/SN1987A/87A_presn/) - [Menon & Heger (2017)](https://ui.adsabs.harvard.edu/abs/2017MNRAS.469.4649M/abstract)


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
Download the Sukhbold 2016 set linked above and extract the contents into the `data` directory under a folder named `sukhbold_2016`:

```
data
│
└───sukhbold_2016
|   |   s9.0_presn
|   │   s9.5_presn
|   │   ...
```

Then to load a progenitor model in python:

```
from progs import ProgModel

model = ProgModel(zams='9.0', progset_name='sukhbold_2016')
```

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

Use the included `environment.yml` file to set up a working [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands) environment:

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

## Single model
Load a specific progenitor model

```
from progs import ProgModel
model = ProgModel(zams='12.0', progset_name='sukhbold_2016')
```

The radial stellar profile is stored in `model.profile`:

``` 
           mass        radius      velocity       density  ...  compactness    luminosity  
0      0.002183  4.310247e+06 -4.049142e+06  1.293904e+10  ...     0.050639  3.504802e+49  
1      0.004335  5.434843e+06 -5.104893e+06  1.270032e+10  ...     0.079767  5.616596e+49  
2      0.006957  6.383686e+06 -5.994816e+06  1.249277e+10  ...     0.108977  7.807254e+49  
3      0.010149  7.265809e+06 -6.820940e+06  1.227866e+10  ...     0.139688  1.019597e+50  
...         ...           ...           ...           ...  ...          ...           ...  
1142  10.905083  4.412274e+13 -3.062704e+02  8.553002e-11  ...     0.000025  5.750828e+37  
1143  10.905101  4.414139e+13 -3.726215e+02  7.828117e-11  ...     0.000025  5.662965e+37  
1144  10.905120  4.416261e+13 -4.243568e+02  7.152728e-11  ...     0.000025  5.556802e+37  
1145  10.905131  4.417666e+13 -4.431164e+02  6.614074e-11  ...     0.000025  5.405292e+37  

[1146 rows x 36 columns]
```
See `config/sukhbold_2016.ini` for column definitions.

Scalar quantities are stored in `model.scalars`:

```
{'presn_mass': 10.905131314018288,
 'presn_radius': 44176664349173.93,
 'presn_temperature': 2496.9102763233523,
 'presn_luminosity': 5.405292355608813e+37,
 'xi_1.75': 0.2113883617902056,
 'xi_2.5': 0.022063351890412038,
 'coremass_He': 3.1217002675140373,
 'coremass_CO': 2.0916700214852075,
 'coremass_Fe': 1.4056675104203924}
```

Create quick profile plots of composition and physical quantities

```
model.plot('entropy')
model.plot_composition()
```

## Full model set
Or the full progenitor set:
```
from progs import ProgSet
pset = ProgSet(progset_name='sukhbold_2016')
```

Which stores a table of `scalars` from all models in `pset.scalars`:
```
       zams  presn_mass  presn_radius  presn_temperature  ...  coremass_CO  coremass_Fe
0      9.00    8.748467  2.865175e+13       2.577388e+03  ...     1.402958     1.320369
1      9.25    8.980991  2.810216e+13       2.588700e+03  ...     1.453464     1.292710
2      9.50    9.210556  2.865834e+13       2.596303e+03  ...     1.503286     1.304485
3      9.75    9.448257  3.094173e+13       2.577251e+03  ...     1.558010     1.303106
..      ...         ...           ...                ...  ...          ...          ...
196   70.00    6.410148  4.222433e+10       7.581580e+06  ...     6.410148     1.507171
197   80.00    6.370163  4.186143e+10       7.538151e+06  ...     6.370163     1.485098
198  100.00    6.037972  3.800036e+10       8.453200e+06  ...     6.037972     1.541309
199  120.00    6.161807  3.570717e+11       9.803012e+05  ...     6.161807     1.568219

[200 rows x 10 columns]
```

which you can also plot
```
pset.plot_scalars('coremass_Fe')
```
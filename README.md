# progs
Python modules for handling core-collapse supernova progenitors.

The main purpose is to provide a generalised method of loading data from different sets of existing progenitor models.
These models are provided in a variety of formats, so I'd like to be able to easily load data from them without needing to think about the underlying data structure.

# Setup
Two environment variables need to be set in your shell (e.g. in your `.bashrc`):
* `PROGS` - path to where you installed this code, e.g. `export PROGS=${HOME}/codes/progs`
* `PROGENITORS` - path to where you keep progenitor models, e.g. `export PROGENITORS=${HOME}/data/progenitors`

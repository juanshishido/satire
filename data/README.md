# Getting the Data

This repository ignores the files in `data/`

Necessay files can be downloaded
[here](http://people.eng.unimelb.edu.au/tbaldwin/resources/satire/) (this
*automatically* starts to download `satire.tgz`)

Instead, if you have the Make utility installed, run `make` from here

(You could also run the script using something like `sh get_data.sh` or
`source get_data.sh`)

---

The repository should be organized in the following way:

```
├── data/
│   ├── test/
│   │   ├── test-*
│   ├── training/
│   │   ├── training-*
│   ├── test-class
│   ├── training-class
```

`test/` contains 1,595 files and `training/` contains 2,639 files

Note: the number of labels in `training-class` is only 2,638

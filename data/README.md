# Getting the Data

This repository ignores the files in `data/`

To download the necessary files, do the following from this directory:

```
$ make
```

(Alternatively, you could run the script using something like
`sh get_data.sh` or `source get_data.sh`)

The repository should be organized in the following way (and will be if data
is accessed using the methods mentioned above):

```
├── data/
│   ├── test/
│   │   ├── test-*
│   ├── training/
│   │   ├── training-*
│   ├── test-class
│   ├── training-class
│   ├── profane.txt
```

`test/` contains 1,595 files and `training/` contains 2,639 files

Note: the number of labels in `training-class` is only 2,638

`profane.txt` is a list of profane words gathered from the Comprehensive Perl
Archive Network (more information can be found
([here](http://search.cpan.org/~tbone/Regexp-Profanity-US-1.4/US.pm))

As a last resort, the data can be downloaded
[here](http://people.eng.unimelb.edu.au/tbaldwin/resources/satire/) (this
*automatically* starts to download `satire.tgz`)


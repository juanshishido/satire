#!/bin/bash

if [[ -d 'test/' && -d 'training/' ]]; then
    echo "Data has already been downloaded"
else
    wget http://people.eng.unimelb.edu.au/tbaldwin/resources/satire/satire.tgz
    tar xvzf satire.tgz
    rm satire.tgz
    rm satire/eval.prl
    rm satire/README
    mv satire/* .
    rmdir satire
fi

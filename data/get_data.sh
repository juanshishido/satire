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

if [[ -d 'wikinews' ]]; then
    echo "WikiNews Data has already been downloaded"
else
    wget http://www.eecs.berkeley.edu/~rsinha/dds/wikinews.tar
    tar xvf wikinews.tar
    rm wikinews.tar
fi

if [[ -d 'oniondata/' ]]; then
    echo "Onion Data has already been downloaded"
else
    wget http://www.eecs.berkeley.edu/~rsinha/dds/oniondata.tar.gz
    tar xvzf oniondata.tar.gz
    rm oniondata.tar.gz
fi

if test -a 'profane.txt'; then
    echo "The profanity list has already been downloaded"
else
    wget http://search.cpan.org/CPAN/authors/id/T/TB/TBONE/Regexp-Profanity-US-1.4.tar.gz
    tar xvzf Regexp-Profanity-US-1.4.tar.gz
    rm Regexp-Profanity-US-1.4.tar.gz
    cat Regexp-Profanity-US-1.4/profane-definite.txt Regexp-Profanity-US-1.4/profane-ambiguous.txt | sed '/^$/d' > profane.txt
    rm -rf Regexp-Profanity-US-1.4
fi

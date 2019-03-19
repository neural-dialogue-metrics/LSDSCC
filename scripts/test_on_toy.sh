#!/usr/bin/env bash

PERL_SCRIPT=/home/cgsdfc/Metrics/LSDSCC/scripts/multi-bleu.pl

${PERL_SCRIPT} \
    /home/cgsdfc/Metrics/LSDSCC/testdata/toy/ref1.txt \
    /home/cgsdfc/Metrics/LSDSCC/testdata/toy/ref2.txt \
    /home/cgsdfc/Metrics/LSDSCC/testdata/toy/ref3.txt \
    </home/cgsdfc/Metrics/LSDSCC/testdata/toy/trains1.txt

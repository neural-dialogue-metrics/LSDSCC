#!/usr/bin/env bash

PERL_SCRIPT=/home/cgsdfc/Metrics/LSDSCC/scripts/multi-bleu.pl

${PERL_SCRIPT} \
    /home/cgsdfc/Metrics/LSDSCC/testdata/system/references.txt \
    </home/cgsdfc/Metrics/LSDSCC/testdata/system/HRED_BeamSearch_5.txt

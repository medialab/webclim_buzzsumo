#!/bin/bash

minet ct summary url "data/buzzsumo_domain_name/infowars.csv" \
    --platforms facebook --start-date 2000-01-01 -s url >\
    "data/crowdtangle_url/infowars.csv"
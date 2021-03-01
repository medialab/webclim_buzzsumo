#!/bin/bash

domain_name="nytimes"

minet ct summary url "data/buzzsumo_domain_name/$domain_name.csv" \
    --platforms facebook --start-date 2000-01-01 >\
    "data/crowdtangle_url/$domain_name.csv"

domain_name="breitbart"

minet ct summary url "data/buzzsumo_domain_name/$domain_name.csv" \
    --platforms facebook --start-date 2000-01-01 >\
    "data/crowdtangle_url/$domain_name.csv"


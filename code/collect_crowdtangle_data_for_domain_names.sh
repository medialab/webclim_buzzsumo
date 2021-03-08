#!/bin/bash

minet ct search "infowars.com" --search-field include_query_strings\
 --platform facebook  --start-date 2017-01-01 >\
 "data/crowdtangle_domain_name/infowars.csv"
#!/bin/bash

minet ct search "cnn.com" --search-field include_query_strings\
 --platform facebook  --start-date 2019-01-01 --end-date 2020-12-31 >\
 "data/crowdtangle_domain_name/cnn_posts.csv"
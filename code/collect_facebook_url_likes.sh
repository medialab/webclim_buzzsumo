#!/bin/bash

domain_name="infowars"

minet fb url-likes url "data/buzzsumo_domain_name/$domain_name.csv" \
    -s "url,published_date" >\
    "data/facebook_url_like/$domain_name.csv"
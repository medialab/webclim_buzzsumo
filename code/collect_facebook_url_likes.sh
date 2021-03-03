#!/bin/bash

domain_name="nypost"

minet fb url-likes url "data/buzzsumo_domain_name/$domain_name.csv" >\
    "data/facebook_url_like/$domain_name.csv"
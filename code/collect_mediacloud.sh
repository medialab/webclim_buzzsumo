#!/bin/bash

# lminet mc search -m 18515 '*' --publish-year 2017 > data/mediacloud/infowars_2017.csv
# lminet mc search -m 18515 '*' --publish-year 2018 > data/mediacloud/infowars_2018.csv
# lminet mc search -m 18515 '*' --publish-year 2019 > data/mediacloud/infowars_2019.csv
# lminet mc search -m 18515 '*' --publish-year 2020 > data/mediacloud/infowars_2020.csv
# lminet mc search -m 18515 '*' --publish-year 2021 > data/mediacloud/infowars_2021.csv

# cd data/mediacloud
# awk '(NR == 1) || (FNR > 1)' *.csv > infowars.csv

minet fb url-likes url data/mediacloud/infowars.csv \
    -s "url,publish_date" > data/mediacloud/infowars_fb_likes.csv

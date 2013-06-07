#!/bin/sh
# agesic - CKAN 1.8 to 2.x migration script

# default config
CKANUSER=ckanuser
CKANDB=datosabiertos
CKANAPIBASELOCATION=http://localhost:8000/api
HTTPDSERVICESTOP="apache2 stop"
HTTPDSERVICESTART="apache2 start"

# override default configuration if a local one is defined
if [ -f ~/ckan18to2x.rc ]; then
    . ~/ckan18to2x.rc
fi

sudo service $HTTPDSERVICESTOP
sudo -u postgres dropdb $CKANDB
sudo -u postgres createdb -O $CKANUSER $CKANDB
zcat ~/datosabiertos.sql.gz | psql -q -U $CKANUSER $CKANDB
paster db upgrade
sudo service $HTTPDSERVICESTART
python ../ckanext-agesic/ckan18to2x.py $CKANAPIBASELOCATION
psql -U $CKANUSER -f ../ckanext-agesic/post_script_queries.sql $CKANDB
../ckanext-agesic/delete_group 79776e4c-9162-4134-99a5-e65063f64e3e | psql -U $CKANUSER $CKANDB
paster search-index rebuild

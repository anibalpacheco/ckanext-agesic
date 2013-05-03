CKANUSER=ckanuser
CKANDB=datosabiertos
HTTPDSERVICE=apache2

sudo service $HTTPDSERVICE stop
sudo -u postgres dropdb $CKANDB
sudo -u postgres createdb -O $CKANUSER $CKANDB
zcat ~/datosabiertos.sql.gz | psql -q -U $CKANUSER $CKANDB
paster db upgrade
sudo service $HTTPDSERVICE start
python ../ckanext-agesic/ckan18to2x.py
psql -U $CKANUSER -f ../ckanext-agesic/post_script_queries.sql $CKANDB
../ckanext-agesic/delete_group 79776e4c-9162-4134-99a5-e65063f64e3e | psql -U $CKANUSER $CKANDB
paster search-index rebuild

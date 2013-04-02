sudo service httpd stop
sudo -u postgres dropdb datosabiertos
sudo -u postgres createdb -O ckan datosabiertos
psql -f ~/datosabiertos.sql datosabiertos
paster db upgrade
sudo service httpd start
python ~/ckan-agesic-utils/ckan18to2x.py 
psql -f ~/ckan-agesic-utils/post_script_queries.sql datosabiertos
~/ckan-agesic-utils/delete_group 79776e4c-9162-4134-99a5-e65063f64e3e|psql datosabiertos
paster search-index rebuild

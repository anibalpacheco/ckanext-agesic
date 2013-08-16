Plugin de AGESIC para CKAN
==========================

AGESIC - Aníbal Pacheco, Sebastián Filippini

Este proyecto contiene
----------------------

* Plugin de CKAN para su customización
* Scripts para la actualización de CKAN de 1.8 a 2.x

Para compilar el CSS se utiliza LESS
-----------------------------------

* Si LESS se instaló como paquete de node.js en el proyecto ckan:

```
$ ckan/node_modules/less/bin/lessc ckanext-agesic/ckanext/agesic/public/css/agesic.less ckanext-agesic/ckanext/agesic/templates/agesic.css
```

* Si LESS se instaló system-wide:

```
$ cd ckanext/agesic
$ lessc public/css/agesic.less templates/agesic.css
```

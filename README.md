# Plugin de AGESIC para CKAN

AGESIC - Aníbal Pacheco, Sebastián Filippini

## Este proyecto contiene

* Plugin de CKAN para su customización
* Scripts para la actualización de CKAN de 1.8 a 2.x
* Parches a aplicar en CKAN-master

## Para compilar el CSS se utiliza LESS

* Si LESS se instaló como paquete de node.js en el proyecto ckan:

```
$ ckan/node_modules/less/bin/lessc ckanext-agesic/ckanext/agesic/public/css/agesic.less ckanext-agesic/ckanext/agesic/templates/agesic.css
```

* Si LESS se instaló system-wide:

```
$ cd ckanext/agesic
$ lessc public/css/agesic.less templates/agesic.css
```

## Branches y parches a utilizar en CKAN

Utilizar los siguientes branches y parches en conjunto:

* 1550-what-file-did-i-upload
* 1617-detached-instance
* https://github.com/anibalpacheco/ckan/tree/1670-broken-api-docs-link
* Branch ```agesic``` del repositorio https://git.agesic.gub.uy/agesic/ckan/
* En ambiente de producción además aplicar el siguiente parche:

```
index e1c60cc..83ccf9c 100644
--- a/ckan/public/base/javascript/client.js
+++ b/ckan/public/base/javascript/client.js
@@ -102,7 +102,7 @@
      * Returns a jQuery xhr promise.
      */
     getLocaleData: function (locale, success, error) {
-      var url = this.url('/api/i18n/' + (locale || ''));
+      var url = this.url('https://catalogodatos.gub.uy/api/i18n/' + (locale || ''));
       return jQuery.getJSON(url).then(success, error);
     },
```

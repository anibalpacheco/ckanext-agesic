# -*- coding: utf-8 -*-
# Notice: The apikey used in earliers revisions of this script was changed.

import sys
from email.utils import unquote
import ckanclient

# connect to api
ckan = ckanclient.CkanClient(base_location=sys.argv[1], api_key='api-key-here')

# set organization images
organization_images = {
    'junta-departamental-de-florida':
        'http://www.juntaflorida.gub.uy/desarrollo/jdf/imagenes/departamento%20abierto%20logo.jpg',
    'ministerio-de-salud-publica':
        'http://new.paho.org/uru/images/stories/msp1.jpg',
    'ministerio-de-turismo-y-deportes':
        'http://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Ministerio_de_Turismo_y_Deporte_de_Uruguay.jpg/640px-Ministerio_de_Turismo_y_Deporte_de_Uruguay.jpg',
    'municipio-de-maldonado':
        'http://municipiomaldonado.gub.uy/imagenes/logo.png',
    'intendencia-montevideo':
        'http://www.montevideo.gub.uy/sites/default/themes/custom/imm/logo.gif',
    'acce':
      'http://www.agesic.gub.uy/innovaportal/file/1171/1/compras_estatales.jpg',
    'agesic': 'http://upload.wikimedia.org/wikipedia/commons/d/de/Agesic.jpg',
    'agev': 'http://agev.opp.gub.uy/interfase/logo_agev.gif',
    'ine': 'http://www.ine.gub.uy/imagenes/logo%20ine.png',
    'onsc': 'http://www.onsc.gub.uy/onsc1/images/Cab_Logo.png',
    'mvotma': 'http://www.dinama.gub.uy/playas/images/logo_mvotma.png',
    'unasev':
        'https://twimg0-a.akamaihd.net/profile_images/2343091374/mxecij92h8z409q6w762.jpeg',
    'defensa-del-consumidor': '',
    'fing': '',
    'ursea': '',
}

for group_name, image_url in organization_images.iteritems():
    group = ckan.group_entity_get(group_name)
    if not group['image_url']:
        group['image_url'] = image_url
    if not group['is_organization']:
        group['is_organization'] = True
    group['description'] += '.'
    ckan.group_entity_put(group)

# creation of new groups
groups = {
    'transporte': 'Transporte',
    'turismo': 'Turismo',
    'vivienda': 'Vivienda',
    'cultura': 'Cultura',
    'deporte': 'Deporte',
    'desarrollo-social': 'Desarrollo Social',
    'economia': 'Economía',
    'educacion': 'Educación',
    'industria': 'Industria',
    'infraestructura': 'Infraestructura',
    'medio-ambiente': 'Medio Ambiente',
    'salud': 'Salud',
    'seguridad': 'Seguridad',
    'trabajo': 'Trabajo'
}

for name, title in groups.iteritems():
    ckan.group_register_post({'name': name, 'title': title})

# asociate datasets to groups based on category custom field
for package_id in ckan.package_register_get():
    group_name = unquote(
        ckan.package_entity_get(package_id)['extras'].get('category'))
    if group_name:
        group_name_to_get = group_name.replace('_', '-')
        group = ckan.group_entity_get(group_name_to_get)
        if package_id not in group['packages']:
            group['packages'].append(package_id)
            ckan.group_entity_put(group)

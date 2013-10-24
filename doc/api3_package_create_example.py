import pprint, json, urllib2

request = urllib2.Request('http://ckan/api/3/action/package_create')

request.add_header('Authorization', 'api-key-here')

pprint.pprint(json.loads(urllib2.urlopen(request, json.dumps(
    {'name': "created-via-api"})).read()))

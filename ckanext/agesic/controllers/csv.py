# TODO: provide a CSV to be downloaded using response
#       see this for an example:
# https://github.com/okfn/ckanext-qa/blob/master/ckanext/qa/controller.py#L87

import ckan.new_authz as new_authz
from ckan.lib.base import BaseController #, response
from ckan.lib.base import abort
from ckan.common import _
from ckan.common import c
from ckan.model import Session, Package, Group


class CsvController(BaseController):

    def current_package_list_with_resources(self):
        if not new_authz.is_sysadmin(c.user):
            abort(401, _('Unauthorized to list all datasets'))
        content = '<table>'
        for header in ['name', 'title', 'organizations', 'categories', 'id',
                'resource name', 'format', 'state']:
            content += "<th>%s</th>" % header.title()
        for p in Session.query(Package):
            organizations, categories = [], []
            for g in p.as_dict()['groups']:
                group = Session.query(Group).filter(Group.name == g).first()
                if group.is_organization:
                    organizations.append(g)
                else:
                    categories.append(g)
            for r in p.resources:
                content += '<tr>'
                for td in [p.name, p.title, ', '.join(organizations),
                        ', '.join(categories), r.id, r.name, r.format, r.state]:
                    content += "<td>%s</td>" % td
        return content + '</table>'
